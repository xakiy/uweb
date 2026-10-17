import json

from django.contrib.auth.decorators import permission_required
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_http_methods
from wagtail.models import Page


def dashboard(request):
    """Admin dashboard for page visit analytics."""
    return render(request, "analytics/dashboard.html")


@permission_required("analytics.view_analytics", raise_exception=True)
def chart_data(request):
    """JSON API endpoint for chart data."""
    start_date = parse_date(request.GET.get("start_date")) or timezone.now().date()
    end_date = parse_date(request.GET.get("end_date")) or timezone.now().date()
    granularity = request.GET.get("granularity", "daily")

    # Validate date range
    if start_date > end_date:
        return JsonResponse({"error": "start_date must be <= end_date"}, status=400)

    # Get the analytics database
    from django.db import connection

    with connection.cursor() as cursor:
        # Daily/weekly/monthly aggregation
        if granularity == "weekly":
            date_func = "STRFTIME('%Y-W%W', timestamp)"
        elif granularity == "monthly":
            date_func = "STRFTIME('%Y-%m', timestamp)"
        else:
            date_func = "DATE(timestamp)"

        # Daily visits chart data
        cursor.execute(
            f"""
            SELECT {date_func} as period, COUNT(DISTINCT session_id) as visits
            FROM analytics_pagevisit
            WHERE DATE(timestamp) BETWEEN ? AND ?
            GROUP BY {date_func}
            ORDER BY period
            """,
            [str(start_date), str(end_date)],
        )
        visits_data = [
            {"period": row[0], "visits": row[1]}
            for row in cursor.fetchall()
        ]

        # Top 10 pages by visits
        cursor.execute(
            """
            SELECT page_title, COUNT(DISTINCT session_id) as visits
            FROM analytics_pagevisit
            WHERE DATE(timestamp) BETWEEN ? AND ?
            GROUP BY page_title
            ORDER BY visits DESC
            LIMIT 10
            """,
            [str(start_date), str(end_date)],
        )
        top_pages = [
            {"title": row[0], "visits": row[1]}
            for row in cursor.fetchall()
        ]

        # Visits by day of week
        cursor.execute(
            """
            SELECT CASE CAST(strftime('%w', timestamp) AS INTEGER)
                WHEN 0 THEN 'Sunday'
                WHEN 1 THEN 'Monday'
                WHEN 2 THEN 'Tuesday'
                WHEN 3 THEN 'Wednesday'
                WHEN 4 THEN 'Thursday'
                WHEN 5 THEN 'Friday'
                WHEN 6 THEN 'Saturday'
            END as day_name,
            COUNT(DISTINCT session_id) as visits
            FROM analytics_pagevisit
            WHERE DATE(timestamp) BETWEEN ? AND ?
            GROUP BY strftime('%w', timestamp)
            ORDER BY day_name
            """,
            [str(start_date), str(end_date)],
        )
        day_of_week = [
            {"day": row[0], "visits": row[1]}
            for row in cursor.fetchall()
        ]

        # Visits by hour of day
        cursor.execute(
            """
            SELECT CAST(strftime('%H', timestamp) AS INTEGER) as hour,
            COUNT(DISTINCT session_id) as visits
            FROM analytics_pagevisit
            WHERE DATE(timestamp) BETWEEN ? AND ?
            GROUP BY strftime('%H', timestamp)
            ORDER BY hour
            """,
            [str(start_date), str(end_date)],
        )
        hour_of_day = [
            {"hour": row[0], "visits": row[1]}
            for row in cursor.fetchall()
        ]

    return JsonResponse({
        "visits": visits_data,
        "top_pages": top_pages,
        "day_of_week": day_of_week,
        "hour_of_day": hour_of_day,
        "start_date": str(start_date),
        "end_date": str(end_date),
    })
