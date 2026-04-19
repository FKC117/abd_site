from django.db import migrations, models


def seed_products(apps, schema_editor):
    Product = apps.get_model("analyticabd", "Product")

    Product.objects.get_or_create(
        slug="saiha",
        defaults={
            "name": "Saiha",
            "short_tagline": "Chat-based data analysis platform",
            "description": "Saiha is a conversational analytics product that helps users talk with their data, explore insights, and move from raw datasets to useful decisions.",
            "tags": "AI, Analytics, Chat-based, Data",
            "site_url": "https://example.com/saiha",
            "cta_label": "Visit Saiha",
            "is_featured": True,
            "order": 1,
            "is_active": True,
        },
    )


def unseed_products(apps, schema_editor):
    Product = apps.get_model("analyticabd", "Product")
    Product.objects.filter(slug="saiha").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("analyticabd", "0002_seed_landing_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="landingpage",
            name="products_body",
            field=models.TextField(default="Each product card is managed from the admin with its own logo, tags, summary, CTA label, and destination URL."),
        ),
        migrations.AddField(
            model_name="landingpage",
            name="products_title",
            field=models.CharField(default="Products under the ABD Site umbrella", max_length=140),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("short_tagline", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("tags", models.CharField(blank=True, help_text="Comma-separated tags, for example: AI, Analytics, Chat-based", max_length=255)),
                ("site_url", models.URLField(help_text="Where visitors should be sent when they click the product.")),
                ("cta_label", models.CharField(default="Visit Product", max_length=60)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="products/")),
                ("is_featured", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(seed_products, unseed_products),
    ]
