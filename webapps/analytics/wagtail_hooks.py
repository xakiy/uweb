from wagtail.admin.menu import MenuItem
from wagtail import hooks


class AnalyticsMenuItem(MenuItem):
    """Add analytics dashboard link to the Wagtail admin menu."""

    def __init__(self):
        super().__init__(
            "Analytics",
            "/analytics/dashboard/",
            name="analytics-dashboard",
            icon_name="resubmit",
            order=10000,  # Place at the end of the menu
        )

    def is_visible(self, request):
        return request.user.has_perm("analytics.view_analytics")


hooks.register("register_admin_menu_item", AnalyticsMenuItem)
