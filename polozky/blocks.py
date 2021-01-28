from wagtail.core		   import blocks
from wagtail.images.blocks import ImageChooserBlock
# STREAMFIELDS LIVE IN HERE


class PolozkaBlock(blocks.StructBlock):
	obrazek 	   = ImageChooserBlock(required = True, help_text = "Obrázek položky")
	nazev 		   = blocks.CharBlock( required = True, help_text = "Název položky")
	cena		   = blocks.FloatBlock(required = True, help_text = "Cena položky")
	obchod		   = blocks.CharBlock( required = True, help_text = "Obchod položky")
	pridat_do_kose = blocks.URLBlock(  required = True, help_text = "Přidat do koše")

	class Meta:
		template = "polozky/polozka_block.html"
		icon     = "form"
		label    = "Vytvoření položky"
