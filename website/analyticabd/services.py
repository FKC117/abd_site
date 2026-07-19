import base64
import hashlib
import hmac
import json
import os
import secrets
import logging
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib import error as urlerror
from urllib import parse, request

from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import ApiRequestNonce, PaymentApiClient, PaymentEvent, PaymentIntent


payment_logger = logging.getLogger("payment")


class SignatureError(Exception):
    pass


class PaymentConfigurationError(Exception):
    pass


class EPSRequestError(Exception):
    pass


def get_payment_service_base_url():
    return os.getenv("PAYMENT_SERVICE_BASE_URL", "https://analyticabd.xyz").rstrip("/")


def get_signature_ttl_seconds():
    return int(os.getenv("PAYMENT_SIGNATURE_TTL_SECONDS", "300"))


def get_payment_intent_ttl_minutes():
    return int(os.getenv("PAYMENT_INTENT_TTL_MINUTES", "30"))


def json_dumps(data: Any) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=True)


def build_string_to_sign(method: str, path: str, timestamp: str, nonce: str, body_bytes: bytes) -> str:
    body_hash = hashlib.sha256(body_bytes or b"").hexdigest()
    return "\n".join([method.upper(), path, timestamp, nonce, body_hash])


def compute_signature(secret: str, method: str, path: str, timestamp: str, nonce: str, body_bytes: bytes) -> str:
    message = build_string_to_sign(method, path, timestamp, nonce, body_bytes)
    digest = hmac.new(secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def verify_signed_request(request_obj) -> PaymentApiClient:
    client_id = request_obj.headers.get("X-Client-Id", "").strip()
    timestamp = request_obj.headers.get("X-Timestamp", "").strip()
    nonce = request_obj.headers.get("X-Nonce", "").strip()
    signature = request_obj.headers.get("X-Signature", "").strip()
    if not all([client_id, timestamp, nonce, signature]):
        raise SignatureError("Missing one or more required signature headers.")

    try:
        ts_int = int(timestamp)
    except ValueError as exc:
        raise SignatureError("Invalid timestamp header.") from exc

    now_ts = int(timezone.now().timestamp())
    if abs(now_ts - ts_int) > get_signature_ttl_seconds():
        raise SignatureError("Signature timestamp is outside the allowed window.")

    client = PaymentApiClient.objects.filter(client_id=client_id, is_active=True).first()
    if not client:
        raise SignatureError("Unknown or inactive payment client.")

    expected = compute_signature(client.shared_secret, request_obj.method, request_obj.path, timestamp, nonce, request_obj.body or b"")
    if not hmac.compare_digest(expected, signature):
        raise SignatureError("Invalid request signature.")

    payment_logger.info("signed_request_verified client_id=%s path=%s timestamp=%s", client.client_id, request_obj.path, timestamp)
    try:
        ApiRequestNonce.objects.create(client=client, nonce=nonce)
    except IntegrityError as exc:
        raise SignatureError("Replay detected: nonce has already been used.") from exc
    return client


def validate_return_url(raw_url: str, client: PaymentApiClient) -> str:
    if not raw_url:
        return ""
    if not client.allowed_return_origin:
        return raw_url
    parsed = parse.urlparse(raw_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    if origin != client.allowed_return_origin.rstrip("/"):
        raise ValueError("Return URL origin is not allowed for this client.")
    return raw_url


def get_eps_config() -> dict[str, Any]:
    config = {
        "api_base_url": os.getenv("EPS_API_BASE_URL", "https://sandboxpgapi.eps.com.bd").rstrip("/"),
        "merchant_id": os.getenv("EPS_MERCHANT_ID", "").strip(),
        "username": os.getenv("EPS_USERNAME", "").strip(),
        "password": os.getenv("EPS_PASSWORD", "").strip(),
        "hash_key": os.getenv("EPS_HASH_KEY", "").strip(),
        "store_id": os.getenv("EPS_STORE_ID", "").strip(),
        "transaction_type_id": int(os.getenv("EPS_TRANSACTION_TYPE_ID", "10")),
        "timeout_seconds": int(os.getenv("EPS_TIMEOUT_SECONDS", "30")),
        "version": os.getenv("EPS_VERSION", "1").strip() or "1",
    }
    missing = [name for name in ("merchant_id", "username", "password", "hash_key", "store_id") if not config[name]]
    if missing:
        raise PaymentConfigurationError(f"Missing EPS configuration values: {', '.join(missing)}")
    return config


def compute_eps_hash(value: str, hash_key: str) -> str:
    digest = hmac.new(hash_key.encode("utf-8"), value.encode("utf-8"), hashlib.sha512).digest()
    return base64.b64encode(digest).decode("utf-8")


def http_json_request(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None, headers: dict[str, str] | None = None, timeout: int = 30) -> tuple[int, dict[str, Any]]:
    body = None
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    if payload is not None:
        body = json_dumps(payload).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")

    req = request.Request(url, data=body, headers=req_headers, method=method.upper())
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urlerror.HTTPError as exc:
        raw = exc.read().decode("utf-8") if hasattr(exc, "read") else ""
        return exc.code, json.loads(raw) if raw else {"error": raw or str(exc)}
    except urlerror.URLError as exc:
        raise EPSRequestError(str(exc)) from exc


def get_eps_token(config: dict[str, Any]) -> str:
    url = f"{config['api_base_url']}/v1/Auth/GetToken"
    headers = {"x-hash": compute_eps_hash(config["username"], config["hash_key"])}
    payload = {"userName": config["username"], "password": config["password"]}
    status_code, data = http_json_request(url, method="POST", payload=payload, headers=headers, timeout=config["timeout_seconds"])
    if status_code >= 400 or not data.get("token"):
        payment_logger.warning("eps_token_failed username=%s status_code=%s response=%s", config["username"], status_code, data)
        raise EPSRequestError(f"EPS token request failed: {data}")
    payment_logger.info("eps_token_received username=%s", config["username"])
    return data["token"]


def build_callback_url(intent: PaymentIntent, callback_name: str) -> str:
    return f"{get_payment_service_base_url()}{reverse(f'analyticabd:payment_{callback_name}')}?payment_intent={intent.public_id}"


def initialize_eps_payment(intent: PaymentIntent) -> dict[str, Any]:
    config = get_eps_config()
    token = get_eps_token(config)
    url = f"{config['api_base_url']}/v1/EPSEngine/InitializeEPS"
    payload = {
        "merchantId": config["merchant_id"],
        "storeId": config["store_id"],
        "merchantTransactionId": intent.merchant_transaction_id,
        "CustomerOrderId": intent.internal_order_id,
        "transactionTypeId": config["transaction_type_id"],
        "financialEntityId": 0,
        "transitionStatusId": 0,
        "totalAmount": float(intent.amount),
        "ipAddress": intent.metadata.get("client_ip", "127.0.0.1"),
        "version": config["version"],
        "successUrl": build_callback_url(intent, "success"),
        "failUrl": build_callback_url(intent, "fail"),
        "cancelUrl": build_callback_url(intent, "cancel"),
        "customerName": intent.customer_name or "Customer",
        "customerEmail": intent.customer_email or "",
        "customerAddress": intent.metadata.get("customer_address", "Address not provided"),
        "customerAddress2": "",
        "customerCity": intent.metadata.get("customer_city", "Dhaka"),
        "customerState": intent.metadata.get("customer_state", "Dhaka"),
        "customerPostcode": intent.metadata.get("customer_postcode", "1200"),
        "customerCountry": intent.metadata.get("customer_country", "BD"),
        "customerPhone": intent.customer_phone or "",
        "shipmentName": intent.customer_name or "Customer",
        "shipmentAddress": intent.metadata.get("customer_address", "Address not provided"),
        "shipmentAddress2": "",
        "shipmentCity": intent.metadata.get("customer_city", "Dhaka"),
        "shipmentState": intent.metadata.get("customer_state", "Dhaka"),
        "shipmentPostcode": intent.metadata.get("customer_postcode", "1200"),
        "shipmentCountry": intent.metadata.get("customer_country", "BD"),
        "valueA": intent.public_id,
        "valueB": intent.client.client_id,
        "valueC": intent.internal_order_id,
        "valueD": intent.product_code,
        "shippingMethod": "NO",
        "noOfItem": "1",
        "productName": intent.product_code,
        "productProfile": intent.purpose,
        "productCategory": "AnalyticaBD",
        "ProductList": [{
            "ProductName": intent.product_code,
            "NoOfItem": "1",
            "ProductProfile": intent.purpose,
            "ProductCategory": "AnalyticaBD",
            "ProductPrice": str(intent.amount),
        }],
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "x-hash": compute_eps_hash(intent.merchant_transaction_id, config["hash_key"]),
    }
    status_code, data = http_json_request(url, method="POST", payload=payload, headers=headers, timeout=config["timeout_seconds"])
    if status_code >= 400:
        payment_logger.warning("eps_initialize_failed merchant_transaction_id=%s status_code=%s response=%s", intent.merchant_transaction_id, status_code, data)
        raise EPSRequestError(f"EPS initialize request failed: {data}")
    payment_logger.info("eps_initialize_response merchant_transaction_id=%s response=%s", intent.merchant_transaction_id, data)
    return data


def verify_eps_payment(intent: PaymentIntent) -> dict[str, Any]:
    config = get_eps_config()
    token = get_eps_token(config)
    url = f"{config['api_base_url']}/v1/EPSEngine/CheckMerchantTransactionStatus?{parse.urlencode({'merchantTransactionId': intent.merchant_transaction_id})}"
    headers = {
        "Authorization": f"Bearer {token}",
        "x-hash": compute_eps_hash(intent.merchant_transaction_id, config["hash_key"]),
    }
    status_code, data = http_json_request(url, method="GET", headers=headers, timeout=config["timeout_seconds"])
    if status_code >= 400:
        payment_logger.warning("eps_verify_request_failed merchant_transaction_id=%s status_code=%s response=%s", intent.merchant_transaction_id, status_code, data)
        raise EPSRequestError(f"EPS verify request failed: {data}")
    payment_logger.info("eps_verify_response merchant_transaction_id=%s response=%s", intent.merchant_transaction_id, data)
    return data


def serialize_intent(intent: PaymentIntent) -> dict[str, Any]:
    return {
        "payment_intent_id": intent.public_id,
        "client_id": intent.client.client_id,
        "internal_order_id": intent.internal_order_id,
        "purpose": intent.purpose,
        "product_code": intent.product_code,
        "amount": str(intent.amount),
        "currency": intent.currency,
        "status": intent.status,
        "merchant_transaction_id": intent.merchant_transaction_id,
        "eps_transaction_id": intent.eps_transaction_id,
        "financial_entity": intent.financial_entity,
        "checkout_url": f"{get_payment_service_base_url()}{reverse('analyticabd:payment_checkout', args=[intent.public_id])}",
        "redirect_url": intent.redirect_url,
        "verified_at": intent.verified_at.isoformat() if intent.verified_at else None,
        "expires_at": intent.expires_at.isoformat() if intent.expires_at else None,
        "last_error": intent.last_error,
    }


def notify_client(intent: PaymentIntent) -> None:
    client = intent.client
    if not client.webhook_url:
        return
    payload = {
        "event_id": f"evt_{secrets.token_hex(8)}",
        "payment_intent_id": intent.public_id,
        "internal_order_id": intent.internal_order_id,
        "merchant_transaction_id": intent.merchant_transaction_id,
        "eps_transaction_id": intent.eps_transaction_id,
        "status": intent.status,
        "amount": str(intent.amount),
        "currency": intent.currency,
        "financial_entity": intent.financial_entity,
        "verified_at": intent.verified_at.isoformat() if intent.verified_at else None,
    }
    body_bytes = json_dumps(payload).encode("utf-8")
    timestamp = str(int(timezone.now().timestamp()))
    nonce = secrets.token_hex(16)
    parsed = parse.urlparse(client.webhook_url)
    signature = compute_signature(client.shared_secret, "POST", parsed.path, timestamp, nonce, body_bytes)
    headers = {
        "Content-Type": "application/json",
        "X-Client-Id": "analyticabd-payment-service",
        "X-Timestamp": timestamp,
        "X-Nonce": nonce,
        "X-Signature": signature,
    }
    status_code, data = http_json_request(client.webhook_url, method="POST", payload=payload, headers=headers, timeout=15)
    PaymentEvent.objects.create(payment_intent=intent, event_type="client_webhook", source="analyticabd", payload={"request": payload, "response": data}, status_code=status_code)
    payment_logger.info("client_webhook_response public_id=%s internal_order_id=%s status_code=%s response=%s", intent.public_id, intent.internal_order_id, status_code, data)


def parse_amount(raw_amount: Any) -> Decimal:
    try:
        amount = Decimal(str(raw_amount))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError("Invalid amount value.") from exc
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return amount.quantize(Decimal("0.01"))


def parse_verified_at(raw_value: str | None):
    if not raw_value:
        return timezone.now()
    parsed = parse_datetime(raw_value)
    return parsed or timezone.now()
