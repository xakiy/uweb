# analytics/wagtail_hooks.py

from django.urls import include, path
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from .views import pagevisits_report_view
from . import urls


@hooks.register('register_admin_urls')
def register_analytics_url():
    return [
        path('', include(urls)),
    ]

@hooks.register('register_admin_menu_item')
def register_analytics_menu_item():
    return MenuItem(
        'Pagevisits',
        '/admin/pagevisits-dashboard/',
        icon_name='resubmit', # Built-in Wagtail chart/sync loop indicator icon
        order=9000
    )
