from django.db import models

from wagtail.core.fields import RichTextField
from wagtail.search import index
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.core.blocks import StreamBlock
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

class RecipesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    def get_context(self, request):
        context = super().get_context(request)
        recipespages = self.get_children().live().order_by("-first_published_at")
        context["recipespages"] = recipespages
        return context


class RecipesPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "RecipesPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class RecipesPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=RecipesPageTag, blank=True)

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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("date"), FieldPanel("tags")], heading="Recipes information"
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]


class RecipesTagIndexPage(Page):
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get("tag")
        recipespages = RecipesPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["recipespages"] = recipespages
        return context


class RecipesPageGalleryImage(Orderable):
    page = ParentalKey(
        RecipesPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]

