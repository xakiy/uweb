from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class BlogIndexPage(Page):

    class Meta:
        verbose_name = "Koleksi Artikel"
        verbose_name_plural = "Koleksi-koleksi"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request):
        # ordered in reverse-chronological order
        context = super().get_context(request)
        context["blogpages"] = BlogPage.objects.live().order_by("-date")
        return context


class BlogPage(Page):

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel-artikel"

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
