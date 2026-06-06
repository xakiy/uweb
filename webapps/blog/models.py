from django import forms
from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPageTag(TaggedItemBase):
    class Meta:
        verbose_name = "Tagar"
        verbose_name_plural = "Tagar-tagar"

    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndexPage(Page):
    class Meta:
        verbose_name = "Koleksi Artikel"
        verbose_name_plural = "Koleksi-koleksi"

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogpages = BlogPage.objects.filter(tags__name=tag)
        else:
            blogpages = BlogPage.objects.live().order_by("-date")

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel-artikel"

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    authors = ParentalManyToManyField('blog.Author', blank=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            "date",
            FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
            "tags"], heading="Blog information"),
        "intro", "body", "gallery_images"
    ]


class BlogPageGalleryImage(Orderable):
    class Meta:
        verbose_name = "Galeri Gambar"
        verbose_name_plural = "Koleksi Galeri Gambar"

    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]


@register_snippet
class Author(models.Model):
    class Meta:
        verbose_name = "Penulis"
        verbose_name_plural = "Para Penulis"

    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'