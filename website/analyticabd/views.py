import json
from datetime import timedelta
from urllib.parse import urlencode

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import ContactLead, LandingFAQ, LandingFeature, LandingPage, LandingStat, LandingStep, LandingTestimonial, PaymentEvent, PaymentIntent, Product, SiteBranding
from .services import EPSRequestError, PaymentConfigurationError, SignatureError, get_payment_intent_ttl_minutes, initialize_eps_payment, notify_client, parse_amount, serialize_intent, validate_return_url, verify_eps_payment, verify_signed_request


def home(request):
    errors = {}
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        company = request.POST.get("company", "").strip()
        phone = request.POST.get("phone", "").strip()
        interest = request.POST.get("interest", "").strip()
        message = request.POST.get("message", "").strip()
        if not name:
            errors["name"] = "Please enter your name."
        if not email:
            errors["email"] = "Please enter your email."
        if not message:
            errors["message"] = "Please tell us what you need."
        if not errors:
            ContactLead.objects.create(name=name, email=email, company=company, phone=phone, interest=interest, message=message)
            return redirect("/?submitted=1#contact")
    context = {
        "branding": SiteBranding.load(),
        "landing": LandingPage.load(),
        "stats": LandingStat.objects.filter(is_active=True),
        "products": Product.objects.filter(is_active=True, is_featured=True),
        "features": LandingFeature.objects.filter(is_active=True),
        "steps": LandingStep.objects.filter(is_active=True),
        "testimonials": LandingTestimonial.objects.filter(is_active=True),
        "faqs": LandingFAQ.objects.filter(is_active=True),
        "contact_success": request.GET.get("submitted") == "1",
        "contact_errors": errors,
        "contact_data": request.POST if request.method == "POST" else {},
    }
    return render(request, "analyticabd/home.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def create_payment_intent(request):
    try:
        client = verify_signed_request(request)
    except SignatureError as exc:
        return JsonResponse({"detail": str(exc)}, status=401)
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON body."}, status=400)

    internal_order_id = str(payload.get("internal_order_id", "")).strip()
    purpose = str(payload.get("purpose", "subscription")).strip().lower()
    product_code = str(payload.get("product_code", "")).strip()
    currency = str(payload.get("currency", "BDT")).strip().upper() or "BDT"
    if not internal_order_id:
        return JsonResponse({"detail": "internal_order_id is required."}, status=400)
    if purpose not in {"subscription", "topup"}:
        return JsonResponse({"detail": "purpose must be subscription or topup."}, status=400)
    if not product_code:
        return JsonResponse({"detail": "product_code is required."}, status=400)
    if currency not in {"BDT", "USD"}:
        return JsonResponse({"detail": "currency must be BDT or USD."}, status=400)
    try:
        amount = parse_amount(payload.get("amount"))
        success_return_url = validate_return_url(str(payload.get("success_return_url", "")).strip(), client)
        fail_return_url = validate_return_url(str(payload.get("fail_return_url", "")).strip(), client)
        cancel_return_url = validate_return_url(str(payload.get("cancel_return_url", "")).strip(), client)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    intent, created = PaymentIntent.objects.get_or_create(
        client=client,
        internal_order_id=internal_order_id,
        defaults={
            "purpose": purpose,
            "product_code": product_code,
            "amount": amount,
            "currency": currency,
            "customer_name": str(payload.get("customer_name", "")).strip(),
            "customer_email": str(payload.get("customer_email", "")).strip(),
            "customer_phone": str(payload.get("customer_phone", "")).strip(),
            "success_return_url": success_return_url,
            "fail_return_url": fail_return_url,
            "cancel_return_url": cancel_return_url,
            "metadata": {
                "client_ip": request.META.get("REMOTE_ADDR", "127.0.0.1"),
                "customer_address": str(payload.get("customer_address", "Address not provided")).strip(),
                "customer_city": str(payload.get("customer_city", "Dhaka")).strip() or "Dhaka",
                "customer_state": str(payload.get("customer_state", "Dhaka")).strip() or "Dhaka",
                "customer_postcode": str(payload.get("customer_postcode", "1200")).strip() or "1200",
                "customer_country": str(payload.get("customer_country", "BD")).strip() or "BD",
                "extra": payload.get("metadata", {}),
            },
            "expires_at": timezone.now() + timedelta(minutes=get_payment_intent_ttl_minutes()),
        },
    )
    if not created:
        return JsonResponse(serialize_intent(intent), status=200)

    PaymentEvent.objects.create(payment_intent=intent, event_type="intent_created", source=client.client_id, payload=payload, status_code=201)
    try:
        initialize_response = initialize_eps_payment(intent)
        intent.status = "initialized"
        intent.redirect_url = initialize_response.get("RedirectURL", "")
        intent.eps_transaction_id = initialize_response.get("TransactionId", "")
        intent.raw_initialize_response = initialize_response
        intent.last_error = initialize_response.get("ErrorMessage", "") or ""
        intent.save(update_fields=["status", "redirect_url", "eps_transaction_id", "raw_initialize_response", "last_error", "updated_at"])
        PaymentEvent.objects.create(payment_intent=intent, event_type="eps_initialized", source="eps", payload=initialize_response, status_code=200)
    except (PaymentConfigurationError, EPSRequestError) as exc:
        intent.status = "failed"
        intent.last_error = str(exc)
        intent.save(update_fields=["status", "last_error", "updated_at"])
        PaymentEvent.objects.create(payment_intent=intent, event_type="eps_initialize_failed", source="eps", payload={"error": str(exc)}, status_code=500)
        return JsonResponse({"detail": str(exc), **serialize_intent(intent)}, status=502)
    return JsonResponse(serialize_intent(intent), status=201)


@csrf_exempt
@require_GET
def payment_intent_status(request, public_id):
    try:
        client = verify_signed_request(request)
    except SignatureError as exc:
        return JsonResponse({"detail": str(exc)}, status=401)
    intent = get_object_or_404(PaymentIntent, public_id=public_id, client=client)
    return JsonResponse(serialize_intent(intent))


@require_GET
def payment_checkout(request, public_id):
    intent = get_object_or_404(PaymentIntent, public_id=public_id)
    if intent.status == "initialized" and intent.redirect_url:
        return redirect(intent.redirect_url)
    return render(request, "analyticabd/payment_checkout.html", {"intent": intent})


def _finalize_intent_from_eps(intent: PaymentIntent, callback_type: str, query_payload: dict[str, str]):
    PaymentEvent.objects.create(payment_intent=intent, event_type=f"eps_callback_{callback_type}", source="browser_redirect", payload=query_payload, status_code=200)
    try:
        verify_response = verify_eps_payment(intent)
    except (PaymentConfigurationError, EPSRequestError) as exc:
        intent.status = "verification_failed"
        intent.last_error = str(exc)
        intent.save(update_fields=["status", "last_error", "updated_at"])
        PaymentEvent.objects.create(payment_intent=intent, event_type="eps_verify_failed", source="eps", payload={"error": str(exc)}, status_code=500)
        return intent, False, str(exc)

    intent.raw_verify_response = verify_response
    intent.eps_status = str(verify_response.get("Status", "")).strip()
    intent.financial_entity = str(verify_response.get("FinancialEntity", "")).strip()
    verified = (
        str(verify_response.get("MerchantTransactionId", "")).strip() == intent.merchant_transaction_id
        and str(verify_response.get("Status", "")).strip().lower() == "success"
        and str(verify_response.get("TotalAmount", "")).strip() in {str(intent.amount), f"{intent.amount:.2f}"}
    )
    if verified:
        intent.status = "succeeded"
        intent.verified_at = timezone.now()
    elif callback_type == "cancel":
        intent.status = "cancelled"
    else:
        intent.status = "failed"
    intent.save(update_fields=["raw_verify_response", "eps_status", "financial_entity", "status", "verified_at", "updated_at"])
    PaymentEvent.objects.create(payment_intent=intent, event_type="eps_verified", source="eps", payload=verify_response, status_code=200)
    if intent.status == "succeeded":
        try:
            notify_client(intent)
        except Exception as exc:
            PaymentEvent.objects.create(payment_intent=intent, event_type="client_webhook_failed", source="analyticabd", payload={"error": str(exc)}, status_code=500)
    return intent, verified, ""


@require_GET
def payment_success(request):
    public_id = request.GET.get("payment_intent", "").strip()
    if not public_id:
        return HttpResponseBadRequest("Missing payment_intent parameter.")
    intent = get_object_or_404(PaymentIntent, public_id=public_id)
    intent, verified, error_message = _finalize_intent_from_eps(intent, "success", dict(request.GET.items()))
    if intent.success_return_url:
        return redirect(f"{intent.success_return_url}?{urlencode({'payment_intent_id': intent.public_id, 'status': intent.status, 'merchant_transaction_id': intent.merchant_transaction_id})}")
    return render(request, "analyticabd/payment_result.html", {"intent": intent, "verified": verified, "error_message": error_message})


@require_GET
def payment_fail(request):
    public_id = request.GET.get("payment_intent", "").strip()
    if not public_id:
        return HttpResponseBadRequest("Missing payment_intent parameter.")
    intent = get_object_or_404(PaymentIntent, public_id=public_id)
    intent, verified, error_message = _finalize_intent_from_eps(intent, "fail", dict(request.GET.items()))
    if intent.fail_return_url:
        return redirect(f"{intent.fail_return_url}?{urlencode({'payment_intent_id': intent.public_id, 'status': intent.status, 'merchant_transaction_id': intent.merchant_transaction_id})}")
    return render(request, "analyticabd/payment_result.html", {"intent": intent, "verified": verified, "error_message": error_message})


@require_GET
def payment_cancel(request):
    public_id = request.GET.get("payment_intent", "").strip()
    if not public_id:
        return HttpResponseBadRequest("Missing payment_intent parameter.")
    intent = get_object_or_404(PaymentIntent, public_id=public_id)
    intent, verified, error_message = _finalize_intent_from_eps(intent, "cancel", dict(request.GET.items()))
    if intent.cancel_return_url:
        return redirect(f"{intent.cancel_return_url}?{urlencode({'payment_intent_id': intent.public_id, 'status': intent.status, 'merchant_transaction_id': intent.merchant_transaction_id})}")
    return render(request, "analyticabd/payment_result.html", {"intent": intent, "verified": verified, "error_message": error_message})
