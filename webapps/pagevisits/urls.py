# analytics/urls.py

from django.urls import path
from .views import pagevisits_report_view

app_name = 'pagevisits'

urlpatterns = [
    # This mounts to /admin/pagevisits-dashboard/ automatically via the Wagtail hook
    path('pagevisits-dashboard/', pagevisits_report_view, name='pagevisits_dashboard'),
]
