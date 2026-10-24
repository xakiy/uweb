from django.db import models
from django.utils import timezone
from wagtail.models import Page


class PageVisit(models.Model):
    """
    Tracks each visit to a Wagtail Page.
    Uses session_id for deduplication (each session's first visit per page per day counts as one).
    Stores a snapshot of the page URL and title at visit time for historical accuracy.
    """

    class Meta:
        verbose_name = "Page Visit"
        verbose_name_plural = "Page Visits"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["page_id", "-timestamp"]),
            models.Index(fields=["session_id", "page_id", "visit_date"]),
        ]
        unique_together = [("session_id", "page_id", "visit_date")]
        permissions = [
            ("view_analytics", "Can view analytics dashboard"),
        ]

    session_id = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Session ID",
        help_text="Unique session identifier for deduplication.",
    )
    url = models.CharField(
        default="",
        max_length=2048,
        verbose_name="URL",
        help_text="URL snapshot at time of visit.",
    )
    page_title = models.CharField(
        default="",
        max_length=255,
        verbose_name="Page Title",
        help_text="Page title snapshot at time of visit.",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Timestamp",
    )
    visit_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Visit Date",
        help_text="Date portion of timestamp, used for deduplication.",
    )
    user_agent = models.TextField(
        blank=True,
        default="",
        verbose_name="User Agent",
        help_text="Browser/device info from the visitor.",
    )

    page_id = models.IntegerField(null=True, blank=True, default="")

    @property
    def page(self):
        if not self.page_id:
            return None
        try:
            # Query explicitly against the correct database alias
            return Page.objects.using('default').get(id=self.page_id)
        except Page.DoesNotExist:
            return None

    @page.setter
    def page(self, obj):
        self.page_id = obj.id

    def __str__(self):
        return f"{self.page_title} — {self.timestamp}"

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = timezone.now()
        if self.visit_date is None:
            self.visit_date = self.timestamp.date()
        super().save(*args, **kwargs)
