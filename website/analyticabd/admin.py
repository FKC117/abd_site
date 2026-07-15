from django.contrib import admin

from .models import (
    ApiRequestNonce,
    ContactLead,
    LandingFAQ,
    LandingFeature,
    LandingPage,
    LandingStat,
    LandingStep,
    LandingTestimonial,
    PaymentApiClient,
    PaymentEvent,
    PaymentIntent,
    Product,
    SiteBranding,
)


@admin.register(SiteBranding)
class SiteBrandingAdmin(admin.ModelAdmin):
    list_display = ("site_name", "nav_label", "contact_email", "updated_at")

    def has_add_permission(self, request):
        if SiteBranding.objects.exists():
            return False
        return True


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at")

    def has_add_permission(self, request):
        if LandingPage.objects.exists():
            return False
        return True


@admin.register(LandingStat)
class LandingStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(LandingFeature)
class LandingFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(LandingStep)
class LandingStepAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(LandingTestimonial)
class LandingTestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "company", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(LandingFAQ)
class LandingFAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "short_tagline", "site_url", "is_featured", "order", "is_active")
    list_editable = ("is_featured", "order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "interest", "created_at")
    search_fields = ("name", "email", "company", "interest")
    readonly_fields = ("name", "email", "company", "phone", "interest", "message", "created_at")


@admin.register(PaymentApiClient)
class PaymentApiClientAdmin(admin.ModelAdmin):
    list_display = ("client_id", "display_name", "allowed_return_origin", "webhook_url", "is_active", "updated_at")
    search_fields = ("client_id", "display_name", "allowed_return_origin", "webhook_url")
    list_filter = ("is_active",)


@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "client",
        "internal_order_id",
        "purpose",
        "status",
        "callback_status",
        "eps_status",
        "amount",
        "currency",
        "merchant_transaction_id",
        "callback_eps_transaction_id",
        "eps_transaction_id",
        "callback_received_at",
        "verified_at",
        "created_at",
    )
    list_filter = ("purpose", "status", "callback_status", "eps_status", "currency", "client", "created_at", "verified_at")
    search_fields = (
        "public_id",
        "internal_order_id",
        "merchant_transaction_id",
        "callback_eps_transaction_id",
        "eps_transaction_id",
        "client__client_id",
        "customer_name",
        "customer_email",
    )
    readonly_fields = ("public_id", "merchant_transaction_id", "callback_received_at", "created_at", "updated_at", "verified_at")
    date_hierarchy = "created_at"


@admin.register(PaymentEvent)
class PaymentEventAdmin(admin.ModelAdmin):
    list_display = ("payment_intent", "event_type", "source", "status_code", "created_at")
    list_filter = ("event_type", "source", "status_code")
    search_fields = ("payment_intent__public_id", "payment_intent__merchant_transaction_id", "event_type")
    readonly_fields = ("payment_intent", "event_type", "source", "payload", "status_code", "created_at")


@admin.register(ApiRequestNonce)
class ApiRequestNonceAdmin(admin.ModelAdmin):
    list_display = ("client", "nonce", "created_at")
    search_fields = ("client__client_id", "nonce")
    readonly_fields = ("client", "nonce", "created_at")
