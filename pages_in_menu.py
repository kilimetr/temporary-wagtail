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

		name  = "polozka_ccm"
		price = 1221
		shop  = "obchod_ccm"

		nadrazena_stranka = Page.objects.get(id = 73)
		print(nadrazena_stranka)

		polozka_nova = PolozkaPage.objects.create(name = name, price = price, shop = shop)
		nadrazena_stranka.add_child(polozka_nova)
		
		polozka_nova.save()

		print("ZAVŘENO")

# chyba
# django.core.exceptions.ValidationError: {'path': ['This field cannot be blank.'], 'depth': ['This field cannot be null.'], 
# 'title': ['This field cannot be blank.'], 'slug': ['This field cannot be blank.'], 'picture': ['This field cannot be blank.']}
