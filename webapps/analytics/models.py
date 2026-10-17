from django.db import models
from django.utils import timezone
from wagtail.models import Page


class PageVisit(models.Model):
    """
    Tracks each visit to a Wagtail Page.
    Uses session_id for deduplication (each session's first visit per page per day counts as one).
    Stores a snapshot of the page URL and title at visit time for historical accuracy.
    """

    page = models.ForeignKey(
        Page,
        on_delete=models.PROTECT,
        related_name="page_visits",
        verbose_name="Page",
    )
    session_id = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="Session ID",
        help_text="Unique session identifier for deduplication.",
    )
    url = models.CharField(
        max_length=2048,
        verbose_name="URL",
        help_text="URL snapshot at time of visit.",
    )
    page_title = models.CharField(
        max_length=255,
        verbose_name="Page Title",
        help_text="Page title snapshot at time of visit.",
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name="Timestamp",
    )
    user_agent = models.TextField(
        blank=True,
        default="",
        verbose_name="User Agent",
        help_text="Browser/device info from the visitor.",
    )

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["page", "-timestamp"]),
            models.Index(fields=["timestamp"]),
        ]
        verbose_name = "Page Visit"
        verbose_name_plural = "Page Visits"
        permissions = [
            ("view_analytics", "Can view analytics dashboard"),
        ]

    def __str__(self):
        return f"{self.page_title} — {self.timestamp}"

    @property
    def visit_date(self):
        return self.timestamp.date()
