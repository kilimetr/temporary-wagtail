# author Dominik Capkovic 
# contact: domcapkovic@gmail.com; https://www.linkedin.com/in/dominik-čapkovič-b0ab8575/
# GitHub: https://github.com/kilimetr



import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def discount_fun(text):
    pass

class Limango_Products_Items(Item):
    product_brand          = Field(input_processor = MapCompose(discount_fun), output_processor = TakeFirst())
    product_name           = Field()
    product_id             = Field()
    product_discount       = Field()
    product_price_full     = Field()
    product_price_sale     = Field()
    product_price_currency = Field()
    product_labels   	   = Field()
    product_label_type     = Field()
    product_label_value    = Field()

    product_image_link          = Field()
    product_image_dpr           = Field()
    product_image_format        = Field()
    # product_image_variant_count = Field()
    product_image_variant_id    = Field()

    # product_variant_count          = Field()
    product_variants               = Field()
    product_variant_id             = Field()
    product_variant_name           = Field() # size
    product_variant_price_sale     = Field()
    product_variant_price_currency = Field()
    product_variant_stock          = Field()
