from django.db import models

from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.snippets.models 	 import register_snippet
from wagtail.core.models		 import Orderable
from modelcluster.fields		 import ParentalKey
from modelcluster.models 		 import ClusterableModel

from wagtail.images.edit_handlers import ImageChooserPanel


# FOOTER MODEL

class FooterItem(Orderable):
	link_title      = models.CharField(blank = True, null = True, max_length = 50)
	link_popisek    = models.CharField(blank = True, null = True, max_length = 200)
	link_url        = models.CharField(blank = True, max_length = 500)
	link_page       = models.ForeignKey("wagtailcore.Page", blank = True, null = True, related_name = "+", on_delete = models.CASCADE)
	open_in_new_tab = models.BooleanField(default = False, blank = True)
	link_image      = models.ForeignKey("wagtailimages.Image", blank = True, null = True, on_delete = models.SET_NULL, related_name = "+")
	show_when       = models.CharField(max_length=15, choices=[
			('always', ("Always")), ('logged_in', ("When logged in")), ('not_logged_in', ("When not logged in"))
		], default='always', )

	page = ParentalKey("Footer", related_name = "footer_polozky")

	panels = [
		FieldPanel("link_title"),
		FieldPanel("link_popisek"),
		FieldPanel("link_url"),
		PageChooserPanel("link_page"),
		FieldPanel("open_in_new_tab"),
		ImageChooserPanel("link_image"),
		FieldPanel("show_when"),
	]

	
	@property
	def title(self):
		if self.link_page and not self.link_title:
			return self.link_page.title
		elif self.link_title:
			return self.link_title
		else:
			return "Missing Title"


	@property
	def popisek(self):
		if self.link_popisek:
			return self.link_popisek
		else:
			return ""


	@property
	def link(self):
		if self.link_page:
			return self.link_page
		elif self.link_url:
			return self.link_url
		else:
			return "#"



	@property
	def image(self):
		if self.link_image:
			return self.link_image
		else:
			return "#"
	



@register_snippet    # je jedno jestli to použiji jako dekorátor nebo funkci
class Footer(ClusterableModel):
	# MAIN MENU ClusterableModel MODEL
	title = models.CharField(max_length = 100)
	slug  = AutoSlugField(populate_from = "title", editable = True) # stejné jako models.SlugField()

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
			FieldPanel("slug")],
			heading = "Footer"),
		InlinePanel("footer_polozky", label = "Položka v footeru")
	]

	def __str__(self):
		return self.title



