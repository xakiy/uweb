# webapps/analytics/views.py

from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from .models import PagevisitLog

@staff_member_required
def pagevisits_report_view(request):
    now = timezone.now()
    start_date = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)

    # --- 1. Graph Data (Last 7 Days Breakdown) ---
    raw_data = (
        PagevisitLog.objects.filter(timestamp__gte=start_date)
        .values('timestamp__date')
        .annotate(views=Count('id'))
        .order_by('timestamp__date')
    )

    data_map = {}
    for item in raw_data:
        date_key = item['timestamp__date']
        str_key = date_key.strftime('%Y-%m-%d') if hasattr(date_key, 'strftime') else str(date_key)
        data_map[str_key] = item['views']

    chart_data = []
    max_views = 1

    for i in range(7):
        day = (start_date + timedelta(days=i)).date()
        day_str = day.strftime('%Y-%m-%d')
        views = data_map.get(day_str, 0)
        if views > max_views:
            max_views = views

        chart_data.append({
            'label': day.strftime('%a (%b %d)'),
            'views': views,
        })

    for day in chart_data:
        day['percentage'] = int((day['views'] / max_views) * 100)

    # --- 2. 🛠️ NEW: Unique Links Aggregate (Top Pages Breakdown) ---
    top_links = (
        PagevisitLog.objects.values('path')
        .annotate(total_views=Count('id'))
        .order_by('-total_views') # Highest traffic links first
    )

    context = {
        'title': 'Visitor Pagevisits',
        'chart_data': chart_data,
        'total_week_views': sum(d['views'] for d in chart_data),
        'top_links': top_links, # 👈 Passed down into the template list
    }
    return render(request, 'pagevisits/admin/pagevisits_report.html', context)
