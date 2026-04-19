from django.shortcuts import render

from .models import (
    LandingFAQ,
    LandingFeature,
    LandingPage,
    LandingStat,
    LandingStep,
    LandingTestimonial,
    Product,
    SiteBranding,
)


def home(request):
    context = {
        "branding": SiteBranding.load(),
        "landing": LandingPage.load(),
        "stats": LandingStat.objects.filter(is_active=True),
        "products": Product.objects.filter(is_active=True, is_featured=True),
        "features": LandingFeature.objects.filter(is_active=True),
        "steps": LandingStep.objects.filter(is_active=True),
        "testimonials": LandingTestimonial.objects.filter(is_active=True),
        "faqs": LandingFAQ.objects.filter(is_active=True),
    }
    return render(request, "analyticabd/home.html", context)
