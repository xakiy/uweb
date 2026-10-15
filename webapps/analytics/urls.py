from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.analytics_dashboard, name="dashboard"),
    path("page/<int:page_id>/", views.page_analytics, name="page_analytics"),
    path("api/page/<int:page_id>/", views.api_page_views, name="api_page_views"),
]
