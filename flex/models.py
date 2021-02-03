from django.db import models

from wagtail.core.models 		 import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields 		 import StreamField

from stream import blocks

from wagtail.core import blocks as streamfielBLOCKS



# FLEXIBLE PAGE

class FlexPage(Page):
	template = "flex/flex_page.html"

	content = StreamField(
		[
			("title_and_text",  blocks.TitleAndTextBlock()),
			("full_richtext",   blocks.RichtextBlock()),
			("simple_richtext", blocks.SimpleRichtextBlock()),
			("cards",           blocks.CardBlock()),
			("cta",             blocks.CTABlock()),
			("button_block",    blocks.ButtonBlock()),
			("char_block",		streamfielBLOCKS.CharBlock(required = True, help_text = "Help Text", 
				min_length = 5, max_length = 50, template = "stream/char_block.html")), # deep dive to streamfield - custom charblock
		],
		null = True,
		blank = True,
	)

	subtitle = models.CharField(max_length = 100, null = True, blank = True)

	content_panels = Page.content_panels + [
		FieldPanel("subtitle"),
		StreamFieldPanel("content"),
	]

	class Meta:
		verbose_name = "Flex Page"
		verbose_name_plural = "Flex Pages"
