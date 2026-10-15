from django import template
from django.utils import timezone
from datetime import timedelta
from wagtail.models import Page

from ..models import PageView

register = template.Library()


@register.simple_tag
def get_page_view_count(page, days=30):
    """Get view count for a page in the last N days."""
    start_date = timezone.now() - timedelta(days=days)
    return PageView.objects.filter(page=page, timestamp__gte=start_date).count()


@register.simple_tag
def get_page_unique_visitors(page, days=30):
    """Get unique visitor count for a page in the last N days."""
    start_date = timezone.now() - timedelta(days=days)
    return (
        PageView.objects.filter(page=page, timestamp__gte=start_date)
        .values("session_id")
        .distinct()
        .count()
    )


@register.inclusion_tag("analytics/widgets/recent_views.html")
def recent_views(limit=5):
    """Show recent page views."""
    views = PageView.objects.select_related("page").order_by("-timestamp")[:limit]
    return {"views": views}
