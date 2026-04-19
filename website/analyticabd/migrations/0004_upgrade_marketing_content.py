from django.db import migrations


def upgrade_marketing_content(apps, schema_editor):
    SiteBranding = apps.get_model("analyticabd", "SiteBranding")
    LandingPage = apps.get_model("analyticabd", "LandingPage")
    LandingStat = apps.get_model("analyticabd", "LandingStat")
    LandingFeature = apps.get_model("analyticabd", "LandingFeature")
    LandingStep = apps.get_model("analyticabd", "LandingStep")
    LandingTestimonial = apps.get_model("analyticabd", "LandingTestimonial")
    LandingFAQ = apps.get_model("analyticabd", "LandingFAQ")
    Product = apps.get_model("analyticabd", "Product")

    branding, _ = SiteBranding.objects.get_or_create(pk=1)
    branding.site_name = branding.site_name or "ABD Site"
    branding.nav_label = "Company behind focused, high-utility digital products"
    branding.hero_badge = "Built to turn complex work into clear digital experiences"
    branding.footer_text = (
        "ABD Site builds practical software products for teams that need clarity, speed, and reliable workflows."
    )
    if not branding.contact_email:
        branding.contact_email = "hello@abdsite.com"
    branding.save()

    landing, _ = LandingPage.objects.get_or_create(pk=1)
    landing.hero_title = "ABD Site creates digital products that simplify serious work."
    landing.hero_subtitle = (
        "We build focused software products for organizations that deal with complexity every day. "
        "Our products are designed to feel clean, fast, and dependable, whether the problem is data analysis, "
        "operational workflow, or decision support."
    )
    landing.primary_cta_label = "Explore Products"
    landing.primary_cta_url = "#products"
    landing.secondary_cta_label = "Why ABD Site"
    landing.secondary_cta_url = "#features"
    landing.hero_panel_title = "One company, product-first execution"
    landing.hero_panel_body = (
        "ABD Site is the parent brand. Each product under it solves a specific business problem with its own identity, "
        "own destination, and its own focused user experience."
    )
    landing.products_title = "Products built under the ABD Site umbrella"
    landing.products_body = (
        "This landing page introduces the parent company while giving every product a strong, independent presence. "
        "Each product can carry its own logo, positioning, tags, and external site link directly from the admin."
    )
    landing.features_title = "Why the parent-brand approach matters"
    landing.features_body = (
        "A strong company site should do more than look good. It should explain what the company builds, create trust, "
        "and route visitors to the right product with confidence."
    )
    landing.process_title = "How ABD Site turns ideas into products"
    landing.testimonial_title = "How teams respond to the experience"
    landing.faq_title = "Questions a visitor may ask before choosing a product"
    landing.cta_title = "Need a parent-brand site that can introduce products and send visitors exactly where they need to go?"
    landing.cta_body = (
        "ABD Site is built to present the company clearly, highlight products like Saiha powerfully, and let your team "
        "manage core marketing content directly from Django admin."
    )
    landing.cta_label = "Manage Content"
    landing.cta_url = "/admin/"
    landing.save()

    LandingStat.objects.all().delete()
    for order, item in enumerate(
        [
            {
                "value": "1",
                "label": "Parent brand",
                "description": "ABD Site gives your company one polished digital home for presenting every product clearly.",
            },
            {
                "value": "∞",
                "label": "Expandable product portfolio",
                "description": "Add new products over time without redesigning the entire marketing structure.",
            },
            {
                "value": "100%",
                "label": "Admin-managed messaging",
                "description": "Company copy, product cards, testimonials, FAQs, and calls to action can all be updated from admin.",
            },
            {
                "value": "1 click",
                "label": "Product redirection",
                "description": "Send visitors from the parent site directly to the right product website with a clear CTA.",
            },
        ],
        start=1,
    ):
        LandingStat.objects.create(
            value=item["value"],
            label=item["label"],
            description=item["description"],
            order=order,
            is_active=True,
        )

    LandingFeature.objects.all().delete()
    for order, item in enumerate(
        [
            {
                "icon": "BR",
                "title": "Brand clarity from the first screen",
                "description": "Visitors immediately understand that ABD Site is the company behind a family of focused products, not just a single tool.",
            },
            {
                "icon": "PR",
                "title": "Independent product positioning",
                "description": "Products like Saiha can have their own logos, taglines, descriptions, tags, and destination URLs while still benefiting from the trust of the parent brand.",
            },
            {
                "icon": "AD",
                "title": "Admin-driven growth",
                "description": "As the company launches more products, the site can grow through content updates in Django admin instead of repeated template rewrites.",
            },
        ],
        start=1,
    ):
        LandingFeature.objects.create(
            icon=item["icon"],
            title=item["title"],
            description=item["description"],
            order=order,
            is_active=True,
        )

    LandingStep.objects.all().delete()
    for order, item in enumerate(
        [
            {
                "title": "Identify a real operational pain point",
                "description": "ABD Site focuses on products that solve practical problems for real teams, not generic software ideas without business depth.",
            },
            {
                "title": "Build a focused product around that problem",
                "description": "Each product is shaped around a specific outcome, with clear positioning, streamlined UX, and a direct value proposition.",
            },
            {
                "title": "Launch it under a stronger company story",
                "description": "The parent brand creates trust, while the product page and CTA send users into the exact experience they came for.",
            },
        ],
        start=1,
    ):
        LandingStep.objects.create(
            title=item["title"],
            description=item["description"],
            order=order,
            is_active=True,
        )

    LandingTestimonial.objects.all().delete()
    for order, item in enumerate(
        [
            {
                "quote": "What stood out first was the clarity. We understood the company, the product, and the next step in seconds.",
                "author_name": "Nadia Rahman",
                "author_role": "Operations Lead",
                "company": "Data Studio",
            },
            {
                "quote": "The parent-brand structure makes product expansion feel intentional. Saiha looks strong on its own without losing the trust of the main company.",
                "author_name": "Imran Hossain",
                "author_role": "Product Manager",
                "company": "Insight Labs",
            },
            {
                "quote": "The marketing message feels premium, but the admin workflow stays practical. That balance is rare and incredibly useful.",
                "author_name": "Farzana Akter",
                "author_role": "Founder",
                "company": "Analytic Practice",
            },
        ],
        start=1,
    ):
        LandingTestimonial.objects.create(
            quote=item["quote"],
            author_name=item["author_name"],
            author_role=item["author_role"],
            company=item["company"],
            order=order,
            is_active=True,
        )

    LandingFAQ.objects.all().delete()
    for order, item in enumerate(
        [
            {
                "question": "What is ABD Site?",
                "answer": "ABD Site is the parent company website that introduces the company, communicates its product strategy, and showcases the products it builds.",
            },
            {
                "question": "What is Saiha?",
                "answer": "Saiha is one of the products under ABD Site. It is a chat-based data analysis platform where users interact with data conversationally to generate insights and decisions.",
            },
            {
                "question": "Can each product have its own external website?",
                "answer": "Yes. Each product can store its own destination URL in admin, and the landing page can send visitors directly to that product site.",
            },
            {
                "question": "Can the content be updated without editing code?",
                "answer": "Yes. Core content such as hero text, stats, product cards, testimonials, and FAQs is designed to be managed from Django admin.",
            },
        ],
        start=1,
    ):
        LandingFAQ.objects.create(
            question=item["question"],
            answer=item["answer"],
            order=order,
            is_active=True,
        )

    saiha, _ = Product.objects.get_or_create(
        slug="saiha",
        defaults={
            "name": "Saiha",
            "short_tagline": "Chat-based data analysis platform",
            "description": "Saiha helps users talk with their data naturally, turning complex datasets into clearer analysis workflows and faster decisions.",
            "tags": "AI, Analytics, Data, Chat-based",
            "site_url": "https://example.com/saiha",
            "cta_label": "Visit Saiha",
            "is_featured": True,
            "order": 1,
            "is_active": True,
        },
    )
    saiha.name = "Saiha"
    saiha.short_tagline = "Chat-based data analysis platform"
    saiha.description = (
        "Saiha is built for teams that want to interact with data conversationally instead of wrestling with rigid analytical workflows. "
        "It turns the experience of analysis into a guided discussion, helping users move from raw datasets to questions, findings, and decisions with far less friction."
    )
    saiha.tags = "AI, Analytics, Data, Chat-based, Decision Support"
    if not saiha.site_url:
        saiha.site_url = "https://example.com/saiha"
    saiha.cta_label = "Visit Saiha"
    saiha.is_featured = True
    saiha.order = 1
    saiha.is_active = True
    saiha.save()


def downgrade_marketing_content(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("analyticabd", "0003_parent_brand_products"),
    ]

    operations = [
        migrations.RunPython(upgrade_marketing_content, downgrade_marketing_content),
    ]
