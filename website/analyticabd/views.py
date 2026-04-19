from django.shortcuts import redirect, render

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
            ContactLead.objects.create(
                name=name,
                email=email,
                company=company,
                phone=phone,
                interest=interest,
                message=message,
            )
            return redirect("/#contact-success")

    context = {
        "branding": SiteBranding.load(),
        "landing": LandingPage.load(),
        "stats": LandingStat.objects.filter(is_active=True),
        "products": Product.objects.filter(is_active=True, is_featured=True),
        "features": LandingFeature.objects.filter(is_active=True),
        "steps": LandingStep.objects.filter(is_active=True),
        "testimonials": LandingTestimonial.objects.filter(is_active=True),
        "faqs": LandingFAQ.objects.filter(is_active=True),
        "contact_success": request.get_full_path().endswith("#contact-success"),
        "contact_errors": errors,
        "contact_data": request.POST if request.method == "POST" else {},
    }
    return render(request, "analyticabd/home.html", context)
