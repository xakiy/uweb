from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "webapps.analytics"
    label = "analytics"
    verbose_name = "Analytics"

    def ready(self):
        import webapps.analytics.signals  # noqa: F401
