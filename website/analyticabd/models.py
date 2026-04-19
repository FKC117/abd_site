from django.db import models


class SiteBranding(models.Model):
    site_name = models.CharField(max_length=120, default="ABD Site")
    nav_label = models.CharField(max_length=120, default="Parent company for digital products")
    hero_badge = models.CharField(max_length=120, default="Products built for serious operational work")
    footer_text = models.CharField(max_length=255, default="ABD Site builds and launches focused digital products, including analytics-first platforms like Saiha.")
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Branding"
        verbose_name_plural = "Site Branding"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteBranding.objects.exists():
            return
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class LandingPage(models.Model):
    hero_title = models.CharField(
        max_length=220,
        default="We build products that turn difficult workflows into simple, usable digital experiences.",
    )
    hero_subtitle = models.TextField(
        default="ABD Site is the parent company behind practical software products. From analytics platforms like Saiha to future vertical tools, we design, ship, and manage products that solve real business problems."
    )
    primary_cta_label = models.CharField(max_length=60, default="Explore Products")
    primary_cta_url = models.CharField(max_length=255, default="#products")
    secondary_cta_label = models.CharField(max_length=60, default="Contact Us")
    secondary_cta_url = models.CharField(max_length=255, default="#contact")
    hero_panel_title = models.CharField(max_length=120, default="What ABD Site represents")
    hero_panel_body = models.TextField(
        default="A parent brand that can present multiple products clearly, route visitors to each product site, and manage all landing content from Django admin."
    )
    products_title = models.CharField(max_length=140, default="Products under the ABD Site umbrella")
    products_body = models.TextField(
        default="Each product card is managed from the admin with its own logo, tags, summary, CTA label, and destination URL."
    )
    features_title = models.CharField(max_length=120, default="How the parent brand communicates trust")
    features_body = models.TextField(
        default="The landing page introduces the company, explains the product strategy, and gives each product its own clear place to stand out."
    )
    process_title = models.CharField(max_length=120, default="How ABD Site presents products")
    testimonial_title = models.CharField(max_length=120, default="How teams describe the experience")
    faq_title = models.CharField(max_length=120, default="Common questions about the company and its products")
    cta_title = models.CharField(max_length=180, default="Want to showcase your products from one polished parent-brand site?")
    cta_body = models.TextField(
        default="Use the Django admin to manage company messaging, featured products, logos, tags, testimonials, and FAQs without editing templates."
    )
    cta_label = models.CharField(max_length=60, default="Open Admin")
    cta_url = models.CharField(max_length=255, default="/admin/")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Landing Page"
        verbose_name_plural = "Landing Page"

    def __str__(self):
        return "Landing Page Content"

    def save(self, *args, **kwargs):
        if not self.pk and LandingPage.objects.exists():
            return
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class LandingStat(models.Model):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=40)
    description = models.CharField(max_length=140, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value} {self.label}"


class LandingFeature(models.Model):
    icon = models.CharField(max_length=40, default="sparkles")
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class LandingStep(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class LandingTestimonial(models.Model):
    quote = models.TextField()
    author_name = models.CharField(max_length=120)
    author_role = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.author_name


class LandingFAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.question


class Product(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    short_tagline = models.CharField(max_length=180)
    description = models.TextField()
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags, for example: AI, Analytics, Chat-based",
    )
    site_url = models.URLField(help_text="Where visitors should be sent when they click the product.")
    cta_label = models.CharField(max_length=60, default="Visit Product")
    logo = models.ImageField(upload_to="products/", blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
