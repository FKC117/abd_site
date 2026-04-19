from django.db import migrations


def refresh_ai_company_marketing(apps, schema_editor):
    SiteBranding = apps.get_model("analyticabd", "SiteBranding")
    LandingPage = apps.get_model("analyticabd", "LandingPage")
    LandingStat = apps.get_model("analyticabd", "LandingStat")
    LandingFeature = apps.get_model("analyticabd", "LandingFeature")
    LandingStep = apps.get_model("analyticabd", "LandingStep")
    LandingTestimonial = apps.get_model("analyticabd", "LandingTestimonial")
    LandingFAQ = apps.get_model("analyticabd", "LandingFAQ")
    Product = apps.get_model("analyticabd", "Product")

    branding, _ = SiteBranding.objects.get_or_create(pk=1)
    branding.site_name = "ABD Site"
    branding.nav_label = "AI, ML, and agentic systems company"
    branding.hero_badge = "Building AI-driven systems for analytics, healthcare, and research"
    branding.footer_text = (
        "ABD Site develops AI-driven products across data analysis, machine learning, "
        "healthcare automation, and research intelligence."
    )
    if not branding.contact_email:
        branding.contact_email = "hello@abdsite.com"
    branding.save()

    landing, _ = LandingPage.objects.get_or_create(pk=1)
    landing.hero_title = "ABD Site builds AI-driven systems that turn complex work into actionable intelligence."
    landing.hero_subtitle = (
        "We are an IT company focused on applied AI, machine learning, and agentic systems. "
        "Our products are built to support data-heavy decision making, clinical workflow automation, "
        "predictive intelligence, and research execution at scale."
    )
    landing.primary_cta_label = "Explore Our Products"
    landing.primary_cta_url = "#products"
    landing.secondary_cta_label = "See Our Capabilities"
    landing.secondary_cta_url = "#features"
    landing.hero_panel_title = "What ABD Site is building"
    landing.hero_panel_body = (
        "From Saiha, our conversational data analysis product, to upcoming machine learning and "
        "healthcare automation systems, ABD Site is building a portfolio of products grounded in "
        "AI-first execution and real-world utility."
    )
    landing.products_title = "AI products and systems under development"
    landing.products_body = (
        "Each product under ABD Site addresses a real operational problem. Some are live, some are in development, "
        "and all are positioned around AI-assisted analysis, automation, prediction, and decision support."
    )
    landing.features_title = "What makes ABD Site different"
    landing.features_body = (
        "We do not build vague AI experiences. We build targeted systems that help professionals analyze data, "
        "predict risk, automate workflows, and convert knowledge into decisions."
    )
    landing.process_title = "How we turn AI ideas into working systems"
    landing.testimonial_title = "How the market should understand our direction"
    landing.faq_title = "What people need to know about ABD Site and its products"
    landing.cta_title = "Looking for an AI partner that can build products, prediction systems, and data-driven workflows?"
    landing.cta_body = (
        "ABD Site is positioned to deliver practical AI systems across analytics, healthcare automation, "
        "predictive modeling, and research support. Use the admin to keep this parent-brand narrative sharp as the portfolio grows."
    )
    landing.cta_label = "Open Content Admin"
    landing.cta_url = "/admin/"
    landing.save()

    LandingStat.objects.all().delete()
    stats = [
        (
            "AI-first",
            "Product strategy",
            "Every ABD Site product is designed around applied AI, not superficial automation.",
        ),
        (
            "ML-ready",
            "Prediction systems",
            "We are building machine learning products for high-impact use cases including breast cancer prediction.",
        ),
        (
            "Agentic",
            "Workflow orchestration",
            "Our systems are moving toward agentic AI that can coordinate tasks, reasoning, and user support.",
        ),
        (
            "End-to-end",
            "Research and clinical workflows",
            "Our portfolio spans patient consultation support, prescription generation, data analysis, and publication-oriented research assistance.",
        ),
    ]
    for order, (value, label, description) in enumerate(stats, start=1):
        LandingStat.objects.create(
            value=value,
            label=label,
            description=description,
            order=order,
            is_active=True,
        )

    LandingFeature.objects.all().delete()
    features = [
        (
            "AI",
            "Applied AI systems, not generic hype",
            "ABD Site focuses on AI products that solve concrete workflow, analysis, prediction, and automation problems.",
        ),
        (
            "ML",
            "Machine learning for high-value predictions",
            "We are building ML-driven solutions for healthcare and risk prediction where fast, informed decisions matter.",
        ),
        (
            "AG",
            "Agentic AI as an operational layer",
            "Our direction includes agentic systems that can assist, coordinate, interpret, and automate complex user journeys.",
        ),
    ]
    for order, (icon, title, description) in enumerate(features, start=1):
        LandingFeature.objects.create(
            icon=icon,
            title=title,
            description=description,
            order=order,
            is_active=True,
        )

    LandingStep.objects.all().delete()
    steps = [
        (
            "Start with a serious domain problem",
            "We focus on domains where AI can create measurable value, including analytics, healthcare workflow, prediction, and research.",
        ),
        (
            "Design a focused AI product around that problem",
            "Each ABD Site product is shaped around a narrow but important need, which makes the value proposition stronger and the user journey clearer.",
        ),
        (
            "Scale into an intelligent product portfolio",
            "The parent brand lets us launch multiple AI-driven products while preserving a consistent market story and a trusted technical identity.",
        ),
    ]
    for order, (title, description) in enumerate(steps, start=1):
        LandingStep.objects.create(
            title=title,
            description=description,
            order=order,
            is_active=True,
        )

    LandingTestimonial.objects.all().delete()
    testimonials = [
        (
            "The positioning is strong because it connects AI capability to real use cases instead of abstract promises.",
            "Nadia Rahman",
            "Operations Lead",
            "Data Studio",
        ),
        (
            "Saiha makes the direction immediately understandable, and the healthcare and research products show the portfolio has depth.",
            "Imran Hossain",
            "Product Strategist",
            "Insight Labs",
        ),
        (
            "This reads like a company building serious AI systems, not just another software site using AI as a buzzword.",
            "Farzana Akter",
            "Founder",
            "Analytic Practice",
        ),
    ]
    for order, (quote, author_name, author_role, company) in enumerate(testimonials, start=1):
        LandingTestimonial.objects.create(
            quote=quote,
            author_name=author_name,
            author_role=author_role,
            company=company,
            order=order,
            is_active=True,
        )

    LandingFAQ.objects.all().delete()
    faqs = [
        (
            "What does ABD Site build?",
            "ABD Site builds AI-driven systems across conversational analytics, machine learning prediction, healthcare automation, and research support.",
        ),
        (
            "What is Saiha?",
            "Saiha is the first major product under ABD Site. It is a chat-based data analysis platform where users can interact with data conversationally and move toward insights faster.",
        ),
        (
            "Is ABD Site only focused on analytics?",
            "No. Analytics is a key area, but the company is also building ML prediction systems, doctor prescription generation workflows, and research-oriented AI products.",
        ),
        (
            "What kind of AI direction is the company taking?",
            "ABD Site is focused on applied AI, machine learning, and agentic AI systems that help users analyze, automate, predict, and act with greater confidence.",
        ),
    ]
    for order, (question, answer) in enumerate(faqs, start=1):
        LandingFAQ.objects.create(
            question=question,
            answer=answer,
            order=order,
            is_active=True,
        )

    product_data = [
        {
            "slug": "saiha",
            "name": "Saiha",
            "short_tagline": "Chat-based data analysis platform",
            "description": (
                "Saiha is ABD Site's flagship conversational analytics product. It lets users talk with their data, "
                "ask analytical questions naturally, and move from raw datasets to meaningful findings through a guided AI-driven experience."
            ),
            "tags": "AI, Analytics, Chat-based, Data Intelligence, Decision Support",
            "site_url": "https://example.com/saiha",
            "cta_label": "Visit Saiha",
            "order": 1,
        },
        {
            "slug": "breast-cancer-prediction",
            "name": "Breast Cancer Prediction System",
            "short_tagline": "Machine learning for earlier, smarter risk assessment",
            "description": (
                "A machine learning product under development to support breast cancer prediction and risk-oriented decision support. "
                "The goal is to help transform clinical data into more proactive and data-informed medical insight."
            ),
            "tags": "Machine Learning, Healthcare AI, Prediction, Clinical Intelligence",
            "site_url": "https://example.com/breast-cancer-prediction",
            "cta_label": "View Product",
            "order": 2,
        },
        {
            "slug": "prescription-automation",
            "name": "Prescription Automation Engine",
            "short_tagline": "AI-assisted prescription and consultation workflow automation",
            "description": (
                "An AI-driven system being built to automate parts of patient consultation and doctor prescription generation. "
                "It is designed to reduce repetitive workflow effort while supporting cleaner, faster clinical documentation."
            ),
            "tags": "Healthcare Automation, AI Workflow, Prescription Generation, Clinical Systems",
            "site_url": "https://example.com/prescription-automation",
            "cta_label": "View Product",
            "order": 3,
        },
        {
            "slug": "research-intelligence",
            "name": "Research Intelligence Suite",
            "short_tagline": "AI support for analysis, interpretation, and publication workflows",
            "description": (
                "A research-focused AI product aimed at helping teams with data analysis, interpretation support, "
                "research workflow acceleration, and publication-oriented output generation."
            ),
            "tags": "Research AI, Data Analysis, Publication Support, Academic Intelligence",
            "site_url": "https://example.com/research-intelligence",
            "cta_label": "View Product",
            "order": 4,
        },
    ]

    existing_slugs = set()
    for item in product_data:
        product, _ = Product.objects.get_or_create(slug=item["slug"])
        product.name = item["name"]
        product.short_tagline = item["short_tagline"]
        product.description = item["description"]
        product.tags = item["tags"]
        if not product.site_url:
            product.site_url = item["site_url"]
        product.cta_label = item["cta_label"]
        product.is_featured = True
        product.order = item["order"]
        product.is_active = True
        product.save()
        existing_slugs.add(item["slug"])

    Product.objects.exclude(slug__in=existing_slugs).update(is_featured=False)


def reverse_refresh_ai_company_marketing(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("analyticabd", "0005_merge_20260419_1747"),
    ]

    operations = [
        migrations.RunPython(refresh_ai_company_marketing, reverse_refresh_ai_company_marketing),
    ]
