from django.db import migrations


def seed_landing_content(apps, schema_editor):
    SiteBranding = apps.get_model("analyticabd", "SiteBranding")
    LandingPage = apps.get_model("analyticabd", "LandingPage")
    LandingStat = apps.get_model("analyticabd", "LandingStat")
    LandingFeature = apps.get_model("analyticabd", "LandingFeature")
    LandingStep = apps.get_model("analyticabd", "LandingStep")
    LandingTestimonial = apps.get_model("analyticabd", "LandingTestimonial")
    LandingFAQ = apps.get_model("analyticabd", "LandingFAQ")

    SiteBranding.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "ABD Site",
            "nav_label": "Parent company for digital products",
            "hero_badge": "Products built for serious operational work",
            "footer_text": "ABD Site builds and launches focused digital products, including analytics-first platforms like Saiha.",
            "contact_email": "hello@abdsite.com",
        },
    )

    LandingPage.objects.get_or_create(
        pk=1,
        defaults={
            "hero_title": "We build products that turn difficult workflows into simple, usable digital experiences.",
            "hero_subtitle": "ABD Site is the parent company behind practical software products. From analytics platforms like Saiha to future vertical tools, we design, ship, and manage products that solve real business problems.",
            "primary_cta_label": "Explore Products",
            "primary_cta_url": "#products",
            "secondary_cta_label": "Contact Us",
            "secondary_cta_url": "#contact",
            "hero_panel_title": "What ABD Site represents",
            "hero_panel_body": "A parent brand that can present multiple products clearly, route visitors to each product site, and manage all landing content from Django admin.",
            "features_title": "How the parent brand communicates trust",
            "features_body": "The landing page introduces the company, explains the product strategy, and gives each product its own clear place to stand out.",
            "process_title": "How ABD Site presents products",
            "testimonial_title": "How teams describe the experience",
            "faq_title": "Common questions about the company and its products",
            "cta_title": "Want to showcase your products from one polished parent-brand site?",
            "cta_body": "Use the Django admin to manage company messaging, featured products, logos, tags, testimonials, and FAQs without editing templates.",
            "cta_label": "Open Admin",
            "cta_url": "/admin/",
        },
    )

    stats = [
        ("2+", "Product-ready slots", "Showcase current and future products under one parent-company narrative."),
        ("1", "Parent brand", "ABD Site is the umbrella brand that organizes the product portfolio clearly."),
        ("100%", "Admin-managed product routing", "Each product can point to its own website directly from the admin panel."),
        ("0", "Hardcoded product cards needed", "You can add or update product entries without touching the template."),
    ]
    for order, (value, label, description) in enumerate(stats, start=1):
        LandingStat.objects.get_or_create(
            label=label,
            defaults={
                "value": value,
                "description": description,
                "order": order,
                "is_active": True,
            },
        )

    features = [
        ("BR", "Parent-brand positioning", "The homepage explains ABD Site as the company behind a family of products, not as a single product itself."),
        ("PR", "Product showcase cards", "Each product card supports a logo, tagline, tags, description, CTA, and its own destination URL."),
        ("AD", "Admin-first workflow", "Non-technical updates can be handled from the Django admin without digging through templates."),
    ]
    for order, (icon, title, description) in enumerate(features, start=1):
        LandingFeature.objects.get_or_create(
            title=title,
            defaults={
                "icon": icon,
                "description": description,
                "order": order,
                "is_active": True,
            },
        )

    steps = [
        ("Define the company story", "Set ABD Site positioning, hero content, and trust signals from the admin panel."),
        ("Add your products", "Create entries like Saiha with logos, tags, summaries, and external product links."),
        ("Launch confidently", "Present the company and redirect visitors to the right product sites from one clean landing page."),
    ]
    for order, (title, description) in enumerate(steps, start=1):
        LandingStep.objects.get_or_create(
            title=title,
            defaults={
                "description": description,
                "order": order,
                "is_active": True,
            },
        )

    testimonials = [
        ("We needed a parent-company site that could introduce Saiha properly and leave room for future products. This structure fits that perfectly.", "Nadia Rahman", "Operations Lead", "Data Studio"),
        ("The product cards make it easy to route visitors to the correct platform without confusing the company brand with the product brand.", "Imran Hossain", "Product Manager", "Insight Labs"),
        ("The best part is that product details, tags, links, and logos are all manageable from admin.", "Farzana Akter", "Founder", "Analytic Practice"),
    ]
    for order, (quote, author_name, author_role, company) in enumerate(testimonials, start=1):
        LandingTestimonial.objects.get_or_create(
            author_name=author_name,
            defaults={
                "quote": quote,
                "author_role": author_role,
                "company": company,
                "order": order,
                "is_active": True,
            },
        )

    faqs = [
        ("Can I update the landing page without editing HTML?", "Yes. The key sections are backed by Django models and editable from the admin."),
        ("Is SQLite the default database here?", "Yes. This project is configured to use Django's default SQLite database."),
        ("Can each product link to its own separate website?", "Yes. Each product record can store its own URL and redirect visitors there from the landing page."),
    ]
    for order, (question, answer) in enumerate(faqs, start=1):
        LandingFAQ.objects.get_or_create(
            question=question,
            defaults={
                "answer": answer,
                "order": order,
                "is_active": True,
            },
        )


def unseed_landing_content(apps, schema_editor):
    SiteBranding = apps.get_model("analyticabd", "SiteBranding")
    LandingPage = apps.get_model("analyticabd", "LandingPage")
    LandingStat = apps.get_model("analyticabd", "LandingStat")
    LandingFeature = apps.get_model("analyticabd", "LandingFeature")
    LandingStep = apps.get_model("analyticabd", "LandingStep")
    LandingTestimonial = apps.get_model("analyticabd", "LandingTestimonial")
    LandingFAQ = apps.get_model("analyticabd", "LandingFAQ")

    SiteBranding.objects.filter(pk=1).delete()
    LandingPage.objects.filter(pk=1).delete()
    LandingStat.objects.all().delete()
    LandingFeature.objects.all().delete()
    LandingStep.objects.all().delete()
    LandingTestimonial.objects.all().delete()
    LandingFAQ.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("analyticabd", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_landing_content, unseed_landing_content),
    ]
