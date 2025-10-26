from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from recurrence.fields import RecurrenceField
import datetime


class Organization(models.Model):
    """Represents a business, restaurant, sanctuary, or other organization."""

    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('cafe', 'Cafe'),
        ('bakery', 'Bakery'),
        ('grocery', 'Grocery Store'),
        ('shop', 'Shop'),
        ('sanctuary', 'Animal Sanctuary'),
        ('salon', 'Salon/Spa'),
        ('organization', 'Non-profit Organization'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    # Contact Information
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Social Media
    facebook = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True, help_text="Instagram handle (without @)")
    twitter = models.CharField(max_length=100, blank=True, help_text="Twitter/X handle (without @)")

    # Location
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    # Media
    logo = models.ImageField(upload_to='organizations/logos/', blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Image(models.Model):
    """Generic image model that can be associated with different content types."""
    image = models.ImageField(upload_to='images/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, help_text="Alternative text for accessibility")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.caption or f"Image {self.id}"


class News(models.Model):
    """Blog-style news posts about restaurant openings, closings, product releases, etc."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    summary = models.TextField(max_length=500, help_text="Brief summary for preview cards")

    # Relationships
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_posts'
    )
    images = models.ManyToManyField(Image, blank=True, related_name='news_posts')

    # Metadata
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    # SEO
    source_url = models.URLField(blank=True, help_text="Link to original source if applicable")

    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bulletin:news_detail', kwargs={'slug': self.slug})


class Event(models.Model):
    """One-off events like festivals, markets, meetups, etc."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    summary = models.TextField(max_length=500, help_text="Brief summary for preview cards")

    # Date and Time
    start_date = models.DateField()
    end_date = models.DateField(help_text="For multi-day events, same as start_date for single-day")
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    # Location
    venue_name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, default='IL')
    zip_code = models.CharField(max_length=10, blank=True)

    # Relationships
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="Hosting organization"
    )
    images = models.ManyToManyField(Image, blank=True, related_name='events')

    # Additional Info
    website = models.URLField(blank=True)
    registration_url = models.URLField(blank=True, help_text="Link to RSVP or buy tickets")
    cost = models.CharField(max_length=100, blank=True, help_text="e.g., 'Free', '$10', '$5-$15'")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_date', 'start_time']

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot be before start date.'})

    def get_absolute_url(self):
        return reverse('bulletin:event_detail', kwargs={'slug': self.slug})

    def is_upcoming(self):
        """Check if event is in the future."""
        return self.end_date >= timezone.now().date()

    def is_past(self):
        """Check if event has already happened."""
        return self.end_date < timezone.now().date()

    def is_multiday(self):
        """Check if event spans multiple days."""
        return self.end_date > self.start_date


class Special(models.Model):
    """Temporary limited edition offerings from businesses."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    summary = models.TextField(max_length=500, help_text="Brief summary for preview cards")

    # Date Range
    start_date = models.DateField()
    end_date = models.DateField()

    # Relationships
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='specials'
    )
    images = models.ManyToManyField(Image, blank=True, related_name='specials')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.organization.name}"

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot be before start date.'})
        if self.start_date < timezone.now().date():
            raise ValidationError({'start_date': 'Start date cannot be in the past.'})

    def get_absolute_url(self):
        return reverse('bulletin:special_detail', kwargs={'slug': self.slug})

    def is_active(self):
        """Check if special is currently active."""
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Promotion(models.Model):
    """Recurring or one-time sales and deals from businesses."""

    RECURRENCE_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom Pattern'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    summary = models.TextField(max_length=500, help_text="Brief summary for preview cards")

    # Recurrence Pattern
    recurrence_type = models.CharField(max_length=20, choices=RECURRENCE_TYPE_CHOICES)
    recurrence_pattern = RecurrenceField(
        null=True,
        blank=True,
        help_text="Define when this promotion recurs"
    )

    # Time constraints
    valid_from = models.DateField(help_text="First date this promotion is valid")
    valid_until = models.DateField(null=True, blank=True, help_text="Last date (leave blank for ongoing)")

    # Time of day (optional)
    start_time = models.TimeField(null=True, blank=True, help_text="What time does promotion start?")
    end_time = models.TimeField(null=True, blank=True, help_text="What time does promotion end?")

    # Relationships
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='promotions'
    )
    images = models.ManyToManyField(Image, blank=True, related_name='promotions')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.organization.name}"

    def clean(self):
        if self.valid_until and self.valid_until < self.valid_from:
            raise ValidationError({'valid_until': 'End date cannot be before start date.'})

    def get_absolute_url(self):
        return reverse('bulletin:promotion_detail', kwargs={'slug': self.slug})

    def is_active_on_date(self, check_date=None):
        """Check if promotion is active on a given date."""
        if check_date is None:
            check_date = timezone.now().date()

        # Check if date is within valid range
        if check_date < self.valid_from:
            return False
        if self.valid_until and check_date > self.valid_until:
            return False

        # Check recurrence pattern
        if self.recurrence_pattern:
            # Convert date to datetime for recurrence checking
            check_datetime = timezone.make_aware(
                datetime.datetime.combine(check_date, datetime.time.min)
            )
            return check_datetime in self.recurrence_pattern

        return True


class Resource(models.Model):
    """Lists and guides about local vegan resources."""

    RESOURCE_TYPE_CHOICES = [
        ('guide', 'Guide'),
        ('list', 'List'),
        ('directory', 'Directory'),
        ('article', 'Article'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    content = models.TextField()
    summary = models.TextField(max_length=500, help_text="Brief summary for preview cards")

    # Relationships
    organizations = models.ManyToManyField(
        Organization,
        blank=True,
        related_name='resources',
        help_text="Organizations featured in this resource"
    )
    images = models.ManyToManyField(Image, blank=True, related_name='resources')

    # Metadata
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bulletin:resource_detail', kwargs={'slug': self.slug})
