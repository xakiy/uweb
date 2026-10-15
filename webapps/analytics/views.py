from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from wagtail.models import Page

from .models import PageView, VisitSummary


def analytics_dashboard(request):
    """Main analytics dashboard."""
    # Get time range
    days = int(request.GET.get("days", 30))
    start_date = timezone.now() - timedelta(days=days)

    # Total stats
    total_views = PageView.objects.filter(timestamp__gte=start_date).count()
    unique_sessions = (
        PageView.objects.filter(timestamp__gte=start_date)
        .values("session_id")
        .distinct()
        .count()
    )

    # Top pages
    top_pages = (
        PageView.objects.filter(timestamp__gte=start_date)
        .values("page_id", "page_title", "page_url")
        .annotate(view_count=Count("id"))
        .order_by("-view_count")[:10]
    )

    # Daily views
    daily_views = (
        PageView.objects.filter(timestamp__gte=start_date)
        .dates("timestamp", "day")
        .annotate(view_count=Count("id"))
    )

    context = {
        "total_views": total_views,
        "unique_sessions": unique_sessions,
        "top_pages": top_pages,
        "daily_views": daily_views,
        "days": days,
    }
    return render(request, "analytics/dashboard.html", context)


def page_analytics(request, page_id):
    """Analytics for a specific page."""
    try:
        page = Page.objects.get(pk=page_id)
    except Page.DoesNotExist:
        return render(request, "analytics/page_analytics.html", {"error": "Page not found"})

    days = int(request.GET.get("days", 30))
    start_date = timezone.now() - timedelta(days=days)

    views = PageView.objects.filter(page=page, timestamp__gte=start_date)
    total_views = views.count()
    unique_sessions = views.values("session_id").distinct().count()

    # Daily breakdown
    daily = (
        views.dates("timestamp", "day")
        .annotate(count=Count("id"))
    )

    # Top referrers
    referrers = (
        views.exclude(referrer="")
        .values("referrer")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    context = {
        "page": page,
        "total_views": total_views,
        "unique_sessions": unique_sessions,
        "daily": daily,
        "referrers": referrers,
        "days": days,
    }
    return render(request, "analytics/page_analytics.html", context)


def api_page_views(request, page_id):
    """JSON API for page view counts."""
    try:
        page = Page.objects.get(pk=page_id)
    except Page.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404)

    days = int(request.GET.get("days", 30))
    start_date = timezone.now() - timedelta(days=days)

    count = PageView.objects.filter(page=page, timestamp__gte=start_date).count()
    return JsonResponse({"page_id": page_id, "title": page.title, "views": count})
