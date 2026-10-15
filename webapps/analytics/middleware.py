import uuid
from django.utils.deprecation import MiddlewareMixin


class PageViewMiddleware(MiddlewareMixin):
    """
    Middleware to track page views for Wagtail pages.
    This middleware runs after Wagtail has attached the page to the request.
    """

    def process_request(self, request):
        # Initialize session ID if not present
        if not request.session.get("session_id"):
            request.session["session_id"] = str(uuid.uuid4())
        request.session_id = request.session["session_id"]
        return None

    def process_response(self, request, response):
        # Only track successful page views
        if hasattr(request, "page") and response.status_code == 200:
            from .models import PageView

            PageView.objects.create(
                page=request.page,
                ip_address=self._get_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                session_id=getattr(request, "session_id", None),
                page_url=request.path,
                page_title=getattr(request.page, "title", ""),
                referrer=request.META.get("HTTP_REFERER", "")[:500],
            )

        return response

    def _get_ip(self, request):
        """Get client IP address, handling proxies."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
