from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from django.utils.text import slugify


class EventPage(Page):
    event_title = models.CharField(max_length=255)
    event_description = RichTextField()
    # NEW: Start Time (e.g., 2023-10-25 10:00:00 UTC)
    start_time = models.DateTimeField()
    # NEW: Duration in minutes (e.g., 120 for 2 hours)
    duration_minutes = models.IntegerField(default=60, help_text="Duration in minutes")
    # Optional: Location
    location = models.CharField(max_length=255, blank=True)
    max_attendees = models.IntegerField(default=100)
    is_open = models.BooleanField(default=True)

    # Custom fields for the event
    content_panels = Page.content_panels + [
        FieldPanel('event_title'),
        FieldPanel('event_description'),
        FieldPanel('start_time'),
        FieldPanel('duration_minutes'),
        FieldPanel('location'),
        FieldPanel('max_attendees'),
    ]

    def save(self, *args, **kwargs):
        # Ensure duration is positive
        if self.duration_minutes <= 0:
            self.duration_minutes = 60
        super().save(*args, **kwargs)

    def is_past(self):
        """Check if the event has started."""
        return timezone.now() >= self.start_time

    def get_end_time(self):
        """Calculate the end time based on duration."""
        from django.utils import timezone
        # Calculate end time from start_time + duration
        # Note: In a real app, handle timezone offsets carefully
        delta = timezone.timedelta(minutes=self.duration_minutes)
        return self.start_time + delta

    def __str__(self):
        return f"{self.event_title} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"


class AnonymousUser(models.Model):
    """Separate table for tracking event attendees"""
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    event_interests = models.JSONField(default=list)  # Track which events they're interested in
    last_visited = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anonymous - {self.email}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    event = models.ForeignKey(EventPage, on_delete=models.CASCADE, related_name='reservations')
    anonymous_user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20) # For WhatsApp/Telegram
    id_document_type = models.CharField(max_length=50) # e.g., Passport, ID Card
    id_document_url = models.URLField(help_text="Secure upload URL or internal path") # Use a private storage backend
    verification_code = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.event}"

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        super().save(*args, **kwargs)

    def generate_verification_code(self):
        import secrets
        return secrets.token_urlsafe(5)
