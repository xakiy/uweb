from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.menu import MenuItem

from .models import PageView


class PageViewSnippetViewSet(SnippetViewSet):
    model = PageView
    menu_item = MenuItem("Page Views", "/admin/analytics/")
    icon = "chart"
    list_display = ["page_title", "timestamp", "ip_address"]
    search_fields = ["page_title", "timestamp"]


register_snippet(PageViewSnippetViewSet)


@hooks.register("before_serve_page")
def attach_page_to_request(page, request, *args, **kwargs):
    """Attach the page object to the request for middleware to track."""
    request.page = page
    return page
