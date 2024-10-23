from django.db import models

from wagtail.models import Page
from wagtail.fields import (
    RichTextField,
    StreamField,
)
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail import blocks
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from wagtail.snippets.models import register_snippet

@register_snippet
class Notice(models.Model):
    heading = models.CharField(max_length=255)
    message = RichTextField()

class HomeIndexPage(Page):
    max_count = 1;

    heading = models.CharField(blank=True,max_length=120)
    menubox = RichTextField(blank=True)
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('menubox'),
        FieldPanel('body'),
    ]

class ProductBlock(blocks.StructBlock):
    url = blocks.URLBlock()
    price = blocks.DecimalBlock(decimal_places=2)
    sku = blocks.CharBlock()
    photo = ImageChooserBlock(required=False)
    description = blocks.RichTextBlock()
    class Meta:
        template = 'home/blocks/product.html'

class ProductTableBlock(blocks.StructBlock):
    heading = blocks.CharBlock()
    description = blocks.RichTextBlock()
    products = blocks.ListBlock(ProductBlock)
    class Meta:
        template = 'home/blocks/product_table.html'

class HomePage(Page):
    heading = models.CharField(blank=True,max_length=120)
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('product_table', ProductTableBlock()),
        ('notice', SnippetChooserBlock(Notice)),
        ('raw_html', blocks.RawHTMLBlock()),
    ])
    
    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('body'),
    ]

class ContactField(AbstractFormField):
    page = ParentalKey('ContactUsPage', on_delete=models.CASCADE, related_name='form_fields')

class ContactUsPage(AbstractEmailForm):
    max_count = 1;

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]