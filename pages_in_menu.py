from django.core.management.base import BaseCommand
from django.utils 				 import timezone

from polozka.models				import PolozkaListingPage, PolozkaPage
from wagtail.core.models		import Page



class Command(BaseCommand):
	help = "Pages in menu"

	def handle(self, *args, **kwargs):
		print("OTEVŘENO")

		pages_inmenu = PolozkaListingPage.objects.live().in_menu()

		for item in pages_inmenu:
			if item.get_children():
				children = item.get_children()
				# print(children.full_url())

				for i in children:
					print()

					print(i)
					print(i.get_url_parts()) # return site_id, site_root_url, page_url_relative_to_site_url
					print(i.id)
					print(i.path)

					print()
				# 	# if str(i) == "Sýry":
					# 	print("nalezeno")
					# 	print(str(i))
					# print(item)
					# print(i)
					# print()

		picture = "https://img.kupi.cz/kupi/thumbs/mandarinky-5_170_340.jpg"
		name  = "polozka_ccm_02"
		price = 1221.02
		shop  = "obchod_ccm_02"

		nadrazena_stranka = Page.objects.get(id = 73)
		print(nadrazena_stranka)

		polozka_nova = PolozkaPage(title = "polozka_page_ccm_02", name = name, price = price, shop = shop, picture = picture)
		nadrazena_stranka.add_child(instance = polozka_nova)
		
		polozka_nova.save()

		print("ZAVŘENO")


