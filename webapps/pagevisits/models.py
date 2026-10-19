# analytics/models.py

from django.db import models

class PagevisitLog(models.Model):

    class Meta:
        verbose_name = "Pagevisit Log"
        verbose_name_plural = "Pagevisit Logs"
        # Organizes the SQLite storage format to pull the newest hits first
        ordering = ['-timestamp']

    # db_index speeds up the chronological queries used by the dashboard chart
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    # db_index allows fast aggregation of your most popular pages
    path = models.CharField(max_length=255, db_index=True)

    # Stores where the user came from (e.g., google.com, twitter.com)
    referrer = models.CharField(max_length=255, blank=True, null=True)

    # Stores the raw browser details for filtering out crawlers/bots
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} — {self.path}"
