from django.db import models

from django.conf import settings
from wagtail.admin.panels import FieldPanel
from modelcluster.models import ClusterableModel
from django.contrib.contenttypes.fields import GenericRelation
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PublishingPanel,
)
from wagtail.models import (
    Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    Task,
    TaskState,
    TranslatableMixin,
    WorkflowMixin,
)
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.search import index


class HomePage(Page):

    class Meta:
        verbose_name = "Laman"
        verbose_name_plural = "Laman-laman"

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


@register_setting(icon="cog")
class SocialMedia(ClusterableModel, BaseGenericSetting):
    email = models.URLField(verbose_name="E-mail", blank=True)
    facebook = models.URLField(verbose_name="Facebook URL", blank=True)
    github = models.URLField(verbose_name="GitHub URL", blank=True)
    instagram = models.URLField(verbose_name="Instagram URL", blank=True)
    mobile = models.CharField(verbose_name="Mobile No", max_length=20, blank=True)
    phone = models.CharField(verbose_name="Phone No", max_length=20, blank=True)
    telegram = models.CharField(verbose_name="Telegram No", max_length=20, blank=True)
    twitter = models.URLField(verbose_name="Twitter URL", blank=True)
    whatsapp = models.CharField(verbose_name="Whatsapp No", max_length=20, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("facebook"),
                FieldPanel("github"),
                FieldPanel("instagram"),
                FieldPanel("mobile"),
                FieldPanel("phone"),
                FieldPanel("telegram"),
                FieldPanel("twitter"),
                FieldPanel("whatsapp")
            ],
            "Social Media",
        )
    ]


class Person(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    ClusterableModel,
):
    """
    A Django model to store Person objects.
    It is registered using `register_snippet` as a function in wagtail_hooks.py
    to allow it to have a menu item within a custom menu item group.

    `Person` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    workflow_states = GenericRelation(
        "wagtailcore.WorkflowState",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="person",
        for_concrete_model=False,
    )

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="person",
        for_concrete_model=False,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("first_name"),
                        FieldPanel("last_name"),
                    ]
                )
            ],
            "Name",
        ),
        FieldPanel("job_title"),
        FieldPanel("image"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField("first_name"),
        index.SearchField("last_name"),
        index.FilterField("job_title"),
        index.AutocompleteField("first_name"),
        index.AutocompleteField("last_name"),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition("fill-50x50").img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ""

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [("blog_post", _("Blog post"))]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_preview_template(self, request, mode_name):
        from bakerydemo.blog.models import BlogPage

        if mode_name == "blog_post":
            return BlogPage.template
        return "base/preview/person.html"

    def get_preview_context(self, request, mode_name):
        from bakerydemo.blog.models import BlogPage

        context = super().get_preview_context(request, mode_name)
        if mode_name == self.default_preview_mode:
            return context

        page = BlogPage.objects.filter(blog_person_relationship__person=self).first()
        if page:
            # Use the page authored by this person if available,
            # and replace the instance from the database with the edited instance
            page.authors = [
                self if author.pk == self.pk else author for author in page.authors()
            ]
            # The authors() method only shows live authors, so make sure the instance
            # is included even if it's not live as this is just a preview
            if not self.live:
                page.authors.append(self)
        else:
            # Otherwise, get the first page and simulate the person as the author
            page = BlogPage.objects.first()
            page.authors = [self]

        context["page"] = page
        return context

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


class CopyrightText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,):
    """
    This provides editable text for the site copyright text. Again it is registered
    using `register_snippet` as a function in wagtail_hooks.py to be grouped
    together with the Person model inside the same main menu item. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """

    body = RichTextField()

    revisions = GenericRelation(
        "wagtailcore.Revision",
        content_type_field="base_content_type",
        object_id_field="object_id",
        related_query_name="copyright_text",
        for_concrete_model=False,
    )

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Copyright Text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"copyright_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name = "copyright text"
        verbose_name_plural = "copyrights text"


@register_setting(icon="site")
class SiteSettings(BaseSiteSetting):
    site_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        help_text="The suffix for the title meta tag e.g. ' | My Website'",
        default="My Website",
    )

    site_logo = models.ForeignKey(
        "wagtailimages.Image",
        verbose_name='Site Logo',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    site_description = models.CharField(
        verbose_name="Site Description",
        max_length=255,
        help_text="Description that help people to know what your site really is.",
        default="A great website."
    )

    site_address = models.TextField(
        verbose_name="Site Address",
        help_text="Your main office address.",
        blank=True
    )

    site_location_map = models.TextField(
        verbose_name="Map Location",
        help_text="Map pointing to your office.",
        blank=True
    )

    panels = [
        FieldPanel("site_suffix"),
        FieldPanel("site_logo"),
        FieldPanel("site_description"),
        FieldPanel("site_address"),
        FieldPanel("site_location_map"),
    ]