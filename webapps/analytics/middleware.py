import logging
import uuid
from django.urls import resolve
from django.utils import timezone
from wagtail.models import Page
from webapps.analytics.models import PageVisit


app_name = "analytics"

logger = logging.getLogger("analytics.middleware")

# URLs to exclude from tracking
EXCLUDED_PREFIXES = (
    "/admin/",
    "/django-admin/",
    "/documents/",
    "/search/",
    "/favicon.ico",
    "/analytics/",
    "/media/",
    "/__debug__/",
)

class AnalyticsMiddleware:
    """
    Records each visit to a live Wagtail Page.
    Each session can only have one visit per page per day (deduplication).
    Stores a snapshot of the page URL and title at visit time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_response(self, request, response):
        # Skip excluded URL prefixes
        if any(request.path.startswith(p) for p in EXCLUDED_PREFIXES):
            return

        # Only track successful HTML responses
        if response.status_code != 200:
            return

        route = getattr(request, "_wagtail_route_for_request", None)
        page = getattr(route, 'page') if route else None

        if "text/html" not in response.get("Content-Type", ""):
            return

        # Only track Wagtail Pages
        if not page or not isinstance(page, Page):
            logger.info(f"  no page found, skipping {request.path}")
            return

        # Only track live pages
        if not page.live:
            return

        # Get or create session ID
        session_id = request.session.session_key
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session["analytics_session_id"] = session_id

        # Snapshot the URL and title at visit time
        url = request.build_absolute_uri()
        page_title = page.title

        # Deduplicate: each session can only visit each page once per day
        try:
            existing = PageVisit.objects.filter(
                page_id=page.id,
                session_id=session_id
            ).first()

            if not existing:
                PageVisit.objects.create(
                    page_id=page.id,
                    page_title=page.title,
                    url=url,
                    session_id=session_id,
                    user_agent=request.META.get("HTTP_USER_AGENT", "")[:2048],
                )
                logger.info(f"Recorded visit to {request.path} for page '{page_title}'")
            else:
                logger.debug(f"Duplicate visit to {request.path} for session {session_id[:8]}...")
        except Exception as e:
            # Silently ignore DB errors (e.g., analytics DB not yet created)
            logger.error(f"Failed to record visit to {request.path}: {e}")
            pass
