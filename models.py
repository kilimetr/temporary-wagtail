from django.db import models

from wagtail.core.models import Page

from wagtail.admin.edit_handlers  import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin



class PolozkaPage(Page):
	template = "polozka/polozka_page.html"
	
	picture = models.URLField(max_length = 1000, blank = True, null = True, help_text = "Odkaz obrázku položky")
	name    = models.CharField(max_length = 100, blank = False, null = True, help_text = "Název položky")
	price   = models.FloatField(				 blank = False, null = True, help_text = "Cena položky")
	shop    = models.CharField(max_length = 100, blank = False, null = True, help_text = "Obchod kde se dá položka koupit")
	# add_to_cart = models.


	content_panels = Page.content_panels + [
		MultiFieldPanel([
			ImageChooserPanel("picture"),
			FieldPanel("name"),
			FieldPanel("price"),
			FieldPanel("shop"),
			],
			heading = "Polozka content"),
		]


	class Meta:
		verbose_name = "Polozka_vn"
		verbose_name_plural = "Polozka_vnp"



class PolozkaListingPage(RoutablePageMixin, Page):
	template = "polozka/polozka_listing_page.html"

	# max_count = 1

	custom_title = models.CharField(max_length = 100, blank = True, null = True, help_text = "Přepiš původní titulek")

	content_panels = Page.content_panels + [FieldPanel("custom_title"),]


	def get_sitemap_urls(self, request):
		sitemap = super().get_sitemap_urls(request)
		# sitemap.append({
			# "location": self.full_url + self.reverse_subpage("latest_posts"),
			# })

		return sitemap


	@property
	def get_child_pages(self):
		return self.get_children().public().live()
	


	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)

		context["polozka_items"] = PolozkaPage.objects.live().public()
		# polozkypages = self.get_child_pages().live()
		# context["polozkypages"] = polozkypages

		return context