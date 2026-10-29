from wagtail.admin.panels import PageChooserPanel
from .models import EventPage
from wagtail import hooks

@hooks.register('register_page')
def register_event_page():
    return EventPage
