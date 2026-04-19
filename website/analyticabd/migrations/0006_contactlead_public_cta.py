from django.db import migrations, models


def update_public_ctas(apps, schema_editor):
    LandingPage = apps.get_model("analyticabd", "LandingPage")

    landing, _ = LandingPage.objects.get_or_create(pk=1)
    landing.secondary_cta_label = "Contact Us"
    landing.secondary_cta_url = "#contact"
    landing.cta_label = "Send Inquiry"
    landing.cta_url = "#contact"
    landing.save()


def reverse_public_ctas(apps, schema_editor):
    LandingPage = apps.get_model("analyticabd", "LandingPage")

    landing = LandingPage.objects.filter(pk=1).first()
    if landing:
        landing.secondary_cta_label = "See Our Capabilities"
        landing.secondary_cta_url = "#features"
        landing.cta_label = "Open Content Admin"
        landing.cta_url = "/admin/"
        landing.save()


class Migration(migrations.Migration):
    dependencies = [
        ("analyticabd", "0005_ai_company_marketing_refresh"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactLead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("company", models.CharField(blank=True, max_length=150)),
                ("phone", models.CharField(blank=True, max_length=50)),
                ("interest", models.CharField(blank=True, max_length=150)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.RunPython(update_public_ctas, reverse_public_ctas),
    ]
