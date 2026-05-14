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
    Page,
    Task,
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
)
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)


class HomePage(Page):
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
        return "Copyright text"

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

    panels = [
        FieldPanel("site_suffix"),
        FieldPanel("site_logo"),
        FieldPanel("site_description"),
        FieldPanel("site_address")
    ]