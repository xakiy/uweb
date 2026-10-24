import json

from django.contrib.auth.decorators import permission_required
from django.db.models import Case, CharField, Count, Value, When
from django.db.models.functions import Extract, TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from wagtail.models import Page
from .models import PageVisit


def dashboard(request):
    """Admin dashboard for page visit analytics."""
    return render(request, "analytics/dashboard.html")


@permission_required("analytics.view_analytics", raise_exception=True)
def chart_data(request):
    """JSON API endpoint for chart data."""
    start_date = parse_date(request.GET.get("start_date")) or timezone.now().date()
    end_date = parse_date(request.GET.get("end_date")) or timezone.now().date()

    # Validate date range
    if start_date > end_date:
        return JsonResponse({"error": "start_date must be <= end_date"}, status=400)

    # Top 10 pages by visits
    top_pages = (
        PageVisit.objects.annotate(
            visit_date_bucket=TruncDate('timestamp')
        ).filter(visit_date_bucket__range=(start_date, end_date))
        .values('page_title')
        .annotate(visit=Count('session_id', distinct=True))
        .order_by('-visit_date')[:10]
    )

    top_pages = [
        {"page_title": row["page_title"], "visits": row["visit"]}
        for row in top_pages
    ]

    # Daily visits chart data
    visits_data = (
        PageVisit.objects.annotate(
            visit_date_bucket=TruncDate('timestamp')
        )
        .filter(visit_date_bucket__range=(start_date, end_date))
        .values('visit_date')
        .annotate(visits=Count('session_id', distinct=True))
        .order_by('visit_date')
    )

    visits_data = [
        {"period": row["visit_date"].strftime('%Y-%m-%d'), "visits": row["visits"]}
        for row in visits_data
    ]

    # Visits by day of week
    day_of_week = (
        PageVisit.objects.annotate(
            visit_date_bucket=TruncDate('timestamp'),
            day_of_week=Case(
                When(visit_date_bucket__week_day=0, then=Value('Sunday')),
                When(visit_date_bucket__week_day=1, then=Value('Monday')),
                When(visit_date_bucket__week_day=2, then=Value('Tuesday')),
                When(visit_date_bucket__week_day=3, then=Value('Wednesday')),
                When(visit_date_bucket__week_day=4, then=Value('Thursday')),
                When(visit_date_bucket__week_day=5, then=Value('Friday')),
                When(visit_date_bucket__week_day=6, then=Value('Saturday')),
                output_field=CharField(),
            ),
        )
        .filter(visit_date_bucket__range=(start_date, end_date))
        .values('day_of_week')
        .annotate(visits=Count('session_id', distinct=True))
        .order_by('day_of_week')
    )

    day_of_week = [
        {"day": row["day_of_week"], "visits": row["visits"]}
        for row in day_of_week
    ]

    # Visits by hour of day
    hour_of_day = (
        PageVisit.objects.annotate(
            visit_date_bucket=TruncDate('timestamp'),
            hour=Extract('timestamp', 'hour'),
        )
        .filter(visit_date_bucket__range=(start_date, end_date))
        .values('hour')
        .annotate(visits=Count('session_id', distinct=True))
        .order_by('hour')
    )

    hour_of_day = [
        {"hour": row["hour"], "visits": row["visits"]}
        for row in hour_of_day
    ]

    return JsonResponse({
        "visits": visits_data,
        "top_pages": top_pages,
        "day_of_week": day_of_week,
        "hour_of_day": hour_of_day,
        "start_date": str(start_date),
        "end_date": str(end_date),
    })
