from django.urls import path

from .views import create_payment_intent, home, payment_cancel, payment_checkout, payment_fail, payment_intent_status, payment_success

app_name = "analyticabd"

urlpatterns = [
    path("", home, name="home"),
    path("api/v1/payment-intents/", create_payment_intent, name="create_payment_intent"),
    path("api/v1/payment-intents/<str:public_id>/", payment_intent_status, name="payment_intent_status"),
    path("pay/<str:public_id>/", payment_checkout, name="payment_checkout"),
    path("payments/eps/success/", payment_success, name="payment_success"),
    path("payments/eps/fail/", payment_fail, name="payment_fail"),
    path("payments/eps/cancel/", payment_cancel, name="payment_cancel"),
]
