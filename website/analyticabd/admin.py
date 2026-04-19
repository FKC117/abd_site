from django.contrib import admin

from .models import (
    ContactLead,
    LandingFAQ,
    LandingFeature,
    LandingPage,
    LandingStat,
    LandingStep,
    LandingTestimonial,
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
