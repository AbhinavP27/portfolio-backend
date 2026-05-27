from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HeroSection(TimeStampedModel):
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=300, blank=True)
    intro_text = models.TextField(blank=True)
    primary_button_label = models.CharField(max_length=60, default='View Projects')
    primary_button_url = models.CharField(max_length=255, default='#projects')
    secondary_button_label = models.CharField(max_length=60, default='Contact Me')
    secondary_button_url = models.CharField(max_length=255, default='#contact')
    profile_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    alternate_profile_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return 'Hero Section'


class AboutSection(TimeStampedModel):
    section_label = models.CharField(max_length=40, default='About')
    heading = models.CharField(max_length=255, default='Engineering premium products from concept to scale.')
    description = models.TextField(
        default=(
            'I specialize in end-to-end product engineering across React frontends and Django APIs. '
            'My focus is reliability, refined visual systems, and maintainable architecture that supports fast iteration.'
        )
    )

    def __str__(self):
        return 'About Section'


class Skill(TimeStampedModel):
    class Category(models.TextChoices):
        FRONTEND = 'frontend', 'Frontend'
        BACKEND = 'backend', 'Backend'
        TOOLS = 'tools', 'Tools'
        AI = 'ai', 'AI'

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=Category.choices)
    icon = models.CharField(max_length=60, blank=True)
    icon_file = models.FileField(upload_to='skill-icons/', blank=True, null=True)
    proficiency = models.PositiveSmallIntegerField(default=80)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return self.name


class Project(TimeStampedModel):
    class Category(models.TextChoices):
        STATIC = 'static', 'Static'
        DYNAMIC = 'dynamic', 'Dynamic'

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.DYNAMIC)
    summary = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    tech_stack = models.JSONField(default=list, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', '-featured', '-created_at']

    def __str__(self):
        return self.title


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=140, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.project.title} Image {self.id}'


class Experience(TimeStampedModel):
    company = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    achievements = models.JSONField(default=list, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-start_date', 'order']

    def __str__(self):
        return f'{self.position} @ {self.company}'


class Certificate(TimeStampedModel):
    title = models.CharField(max_length=150)
    issuer = models.CharField(max_length=120)
    issue_date = models.DateField()
    credential_id = models.CharField(max_length=120, blank=True)
    verification_url = models.URLField(blank=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-issue_date', 'order']

    def __str__(self):
        return self.title


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class ThemeSettings(TimeStampedModel):
    theme_name = models.CharField(max_length=80, default='Nebula Noir')
    accent_primary = models.CharField(max_length=20, default='#7C3AED')
    accent_secondary = models.CharField(max_length=20, default='#3B82F6')
    surface_tone = models.CharField(max_length=20, default='#070A13')
    glass_blur = models.PositiveSmallIntegerField(default=18)
    enable_particles = models.BooleanField(default=True)
    total_visitors = models.PositiveIntegerField(default=0)
    total_resume_downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.theme_name
