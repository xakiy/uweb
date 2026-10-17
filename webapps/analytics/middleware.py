import logging
import uuid

from django.utils import timezone
from wagtail.models import Page

logger = logging.getLogger("analytics.middleware")

# URLs to exclude from tracking
EXCLUDED_PREFIXES = (
    "/admin/",
    "/django-admin/",
    "/documents/",
    "/search/",
    "/favicon.ico",
    "/analytics/",
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
        logger.info(f"Middleware called for {request.path}, status={response.status_code}")
        # Only track successful HTML responses
        if response.status_code != 200:
            return

        content_type = response.get("Content-Type", "")
        if "text/html" not in content_type:
            return

        # Skip excluded URL prefixes
        if any(request.path.startswith(p) for p in EXCLUDED_PREFIXES):
            return

        # Only track Wagtail Pages
        # Try request.page first (set by some Wagtail views), then fall back to resolver_match
        page = getattr(request, "page", None)
        logger.info(f"  page from request.page={page}")
        if not page or not isinstance(page, Page):
            # Fall back to resolving the page from the URL
            from django.urls import resolve
            try:
                match = resolve(request.path)
                page = getattr(match.func, "page", None)
                logger.info(f"  page from resolver_match={page}")
            except Exception as e:
                page = None
                logger.info(f"  resolve failed: {e}")

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
        now = timezone.now()
        visit_date = now.date()

        # Deduplicate: each session can only visit each page once per day
        try:
            existing = page.page_visits.using("analytics").filter(
                session_id=session_id,
                timestamp__date=visit_date,
            ).first()

            if not existing:
                page.page_visits.using("analytics").create(
                    session_id=session_id,
                    url=url,
                    page_title=page_title,
                    timestamp=now,
                    user_agent=request.META.get("HTTP_USER_AGENT", "")[:2048],
                )
                logger.info(f"Recorded visit to {request.path} for page '{page_title}'")
            else:
                logger.debug(f"Duplicate visit to {request.path} for session {session_id[:8]}...")
        except Exception as e:
            # Silently ignore DB errors (e.g., analytics DB not yet created)
            logger.error(f"Failed to record visit to {request.path}: {e}")
            pass
