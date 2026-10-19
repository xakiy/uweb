# analytics/middleware.py

import threading
from django.utils import timezone
from .models import PagevisitLog

class LightweightPagevisitsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path

        # 1. Don't track admin views, static items, or the dashboard itself
        if not path.startswith('/admin/') and not path.startswith('/cms/') and not path.startswith('/favicon.ico'):

            # 2. Extract values safely on the MAIN thread before it closes
            tracking_data = {
                'path': path,
                'referrer': request.META.get('HTTP_REFERER', ''),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }

            # 3. Pass the static dictionary safely to the background task thread
            threading.Thread(target=self.save_log, args=(tracking_data,)).start()

        return response

    def save_log(self, tracking_data):
        user_agent = tracking_data['user_agent']

        # Bot filtration guard
        bots = ['bot', 'spider', 'crawler', 'scrape', 'curl', 'wget']
        if any(bot in user_agent.lower() for bot in bots):
            return

        # Write data to SQLite using the frozen dictionary values
        PagevisitLog.objects.create(
            path=tracking_data['path'],
            referrer=tracking_data['referrer'],
            user_agent=user_agent
        )
