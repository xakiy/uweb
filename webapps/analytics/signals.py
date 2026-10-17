from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.models import Page

from .models import PageVisit


@receiver(post_save, sender=Page)
def update_page_visit_url(sender, instance, **kwargs):
    """
    When a Wagtail Page is saved, update the URL and title in all related PageVisit records.
    This ensures historical visits always reflect the current state of the page.
    """
    try:
        PageVisit.objects.using("analytics").filter(
            page=instance
        ).update(
            url=instance.url,
            page_title=instance.title,
        )
    except Exception:
        # Silently ignore if analytics DB isn't ready yet
        pass
