from django.db import models

from wagtail.core.models import Page

from wagtail.admin.edit_handlers  import FieldPanel
from wagtail.core.fields		  import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.fields 		 import StreamField
from polozky 					 import blocks
from wagtail.core.models 		 import Orderable
from modelcluster.fields 		 import ParentalKey


class HomePage(Page):
	templates = "home/home_page.html"
	
	max_count = 1
	
	banner_title = models.CharField(max_length = 100, blank = False, null = True)
	banner_subtitle = RichTextField()
	banner_image = models.ForeignKey("wagtailimages.Image", blank = False, null = True, on_delete = models.SET_NULL, related_name = "+")

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel("banner_title"),
			FieldPanel("banner_subtitle"),
			ImageChooserPanel("banner_image"),
			],
			heading = "Bannery - zkouška"),

		MultiFieldPanel([
			InlinePanel("polozky")],
			heading = "Místo pro Položky"),
		]


	class Meta:
		verbose_name = "HP_vn"
		verbose_name_plural = "HP_vnp"



class HomePagePolozky(Orderable):
	page = ParentalKey("home.HomePage", related_name = "polozky")

	polozka = StreamField([
		("polozka_block", blocks.PolozkaBlock())], null = True, blank = True)
		
	content_panels = Page.content_panels + [StreamFieldPanel("polozka")]

	class Meta:
		verbose_name = "Polozka name"
		verbose_name_plural = "Polozka name plural"


