from django.db import models
from django.utils import timezone
from wagtail.models import Page
import uuid


class PageView(models.Model):
    """Track individual page visits for analytics."""

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="page_views",
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    session_id = models.UUIDField(null=True, blank=True, db_index=True)
    page_url = models.CharField(max_length=500, blank=True, default="")
    page_title = models.CharField(max_length=500, blank=True, default="")
    referrer = models.URLField(blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"

    def __str__(self):
        return f"{self.page_title or self.page_url} at {self.timestamp}"


class VisitSummary(models.Model):
    """Pre-computed daily/weekly/monthly summaries for faster queries."""

    PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="visit_summaries",
        null=True,
        blank=True,
    )
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default="daily")
    date = models.DateField(db_index=True)
    view_count = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-date"]
        unique_together = [("page", "period", "date")]
        verbose_name = "Visit Summary"
        verbose_name_plural = "Visit Summaries"

    def __str__(self):
        return f"{self.page_title or self.page_url} - {self.date} ({self.view_count} views)"
