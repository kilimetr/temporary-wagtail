# author Dominik Capkovic 
# contact: domcapkovic@gmail.com; https://www.linkedin.com/in/dominik-čapkovič-b0ab8575/
# GitHub: https://github.com/kilimetr



import scrapy
import json
from math               import ceil
from scrapy.loader      import ItemLoader
from SCRAP_ESHOPS.items import Limango_Products_Items
# from XY import function RETURNS PART OF PAGE LINK as ODEZVA



class LimangoSpider(scrapy.Spider):
    name = "Limango"

    allowed_domains = ["www.limango.de"]

    # def start_requests(self):
    #     urls = [
    #         "https://www.limango.de/search/api/search/listing?limit=200&search=&offset={}&sort=popularity&size=&color=&brand=&category=&\
    #                     campaign=&gender=&style=&product=&merchantId=&price=&discount=&availability=&in=&tag=&shop-type=&referer=/shop/{}?&\
    #                     landing-page-id={}&testGroup=20210706_ProductGateway".format(0, ODEZVA[1], ODEZVA[1])
    #     ]

    #     for url in urls:
    #         yield scrapy.Request(url = url, callback = self.parse)

    start_urls      = ["https://www.limango.de/search/api/search/listing?limit=200&search=&offset=0&sort=popularity&size=&color=&brand=&\
                        category=&campaign=&gender=&style=&product=&merchantId=&price=&discount=&availability=&in=&tag=&shop-type=&\
                        referer=/shop/strampler?&landing-page-id=strampler&testGroup=20210706_ProductGateway"]


    def parse(self, response):
        self.logger.info("PARSE FUN CALLED ON {}".format(response.url))
        # base_link = "https://www.limango.de/search/api/search/listing?limit=200&search=&offset={}&sort=popularity&size=&color=&brand=&category=&\
        #                 campaign=&gender=&style=&product=&merchantId=&price=&discount=&availability=&in=&tag=&shop-type=&referer=/shop/{}?&\
        #                 landing-page-id={}&testGroup=20210706_ProductGateway"

        base_link = "https://www.limango.de/search/api/search/listing?limit=200&search=&offset={}&sort=popularity&size=&color=&brand=&category=&\
                        campaign=&gender=&style=&product=&merchantId=&price=&discount=&availability=&in=&tag=&shop-type=&\
                        referer=/shop/strampler?&landing-page-id=strampler&testGroup=20210706_ProductGateway"
                    
        data = json.loads(response.body)        
        
        limit       = 200
        count_total = data["data"]["products"]["pagination"]["totalCount"]
        
        count_pages = ceil(count_total / limit)

        i = 1
        for page in range(0, count_pages):        
            if i == 1:
                offset  = 0
                abs_url = base_link.format(offset)

                i = i + 1
            
                yield scrapy.Request(url = abs_url, callback = self.parse_page)

            else:
                offset  = offset + 200
                abs_url = base_link.format(offset)
                
                i = i + 1
                
                yield scrapy.Request(url = abs_url, callback = self.parse_page)


    def parse_page(self, response):
        self.logger.info("PARSE FUN CALLED ON {}".format(response.url))

        data = json.loads(response.body)
        products = data["data"]["products"]["data"]

        for product in products:
            loader = ItemLoader(item = Limango_Products_Items(), selector = product)

            loader.add_value("product_brand",            product["brand"]["id"])
            loader.add_value("product_name",             product["brand"]["name"])
            loader.add_value("product_id",               product["id"])
            loader.add_value("product_discount",         product["discount"]) # cotains discount value or null
            loader.add_value("product_price_full",       product["retailPrice"]["amount"])
            loader.add_value("product_price_sale",       product["salesPrice"]["amount"])
            loader.add_value("product_price_currency",   product["salesPrice"]["currency"])
            loader.add_value("product_labels",           product["labels"]) # contains type & value
            loader.add_value("product_image_link",       product["images"]["default"]["url"])
            loader.add_value("product_image_dpr",        product["images"]["default"]["devicePixelRatios"]["original"])
            loader.add_value("product_image_format",     product["images"]["default"]["formats"]["original"])
            loader.add_value("product_image_variant_id", product["images"]["default"]["variants"])
            loader.add_value("product_variants",         product["variants"]) # contains all variants info

            yield loader.load_item()



