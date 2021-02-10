from django.db import models

from wagtail.core.models import Page

from wagtail.admin.edit_handlers  import FieldPanel
from wagtail.core.fields		  import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


class HomePage(Page):
	templates = "home/home_page.html"
	
	# max_count = 1
	
	banner_title = models.CharField(max_length = 100, blank = False, null = True)
	banner_subtitle = RichTextField()
	banner_image = models.ForeignKey("wagtailimages.Image", blank = True, null = True, on_delete = models.SET_NULL, related_name = "+")

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel("banner_title"),
			FieldPanel("banner_subtitle"),
			ImageChooserPanel("banner_image"),
			],
			heading = "Bannery - zkouška"),
		]


	class Meta:
		verbose_name = "HP_vn"
		verbose_name_plural = "HP_vnp"





