"""
Database router for multi-database setup.
Routes ContentType and auth models to 'default' DB, everything else to 'analytics' DB.
"""


class AnalyticsRouter:
    """
    Route content types and auth models to the 'default' database.
    Route analytics app models to the 'analytics' database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "analytics":
            return "analytics"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "analytics":
            return "analytics"
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # analytics -> only on 'analytics'
        if app_label == "analytics":
            return db == "analytics"
        # All other apps -> only on 'default'
        return db == "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "analytics" or obj2._meta.app_label == "analytics":
            return False
        return None
