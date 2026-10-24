from django.contrib import admin
from .models import PageVisit


class PageVisitAdmin(admin.ModelAdmin):
    list_display = ("page_title", "url", "session_id", "timestamp")
    list_filter = ("timestamp", "page_id")
    search_fields = ("page_title", "url", "session_id")
    readonly_fields = ("page_id", "session_id", "url", "page_title", "timestamp", "user_agent")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)


admin.site.register(PageVisit, PageVisitAdmin)
