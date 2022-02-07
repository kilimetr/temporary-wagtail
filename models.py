from django.db import models
from django_extensions.db.fields import AutoSlugField
from djmoney.models.fields import MoneyField
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from longclaw.products.models import ProductVariantBase, ProductBase



class ProductIndex(Page): # v podstatě jako PolozkaListingPage
    # template = "polozka/polozka_page.html"

    # subpage_types = ["catalog.Product"]

    @property
    def products(self):
        # return Product.objects.child_of(self).live()
        return ProductIndex.get_children(self).live().specific()


class Product(ProductBase): # v podstatě jako PolozkaPage
    template = "catalog/product.html"

    parent_page_types = ["catalog.ProductIndex"]

    picture         = models.URLField(max_length = 1000, blank = True,  null = True, help_text = "Odkaz obrázku položky")
    name            = models.CharField(max_length = 100, blank = False, null = True, help_text = "Název položky")

    content_panels = ProductBase.content_panels + [
        MultiFieldPanel([
            FieldPanel("picture"),
            FieldPanel("name"),
            ]),
        InlinePanel("variants", label = "Product variants", panels = [
                        FieldPanel("shop"),
                        FieldPanel("ref"),
                        FieldPanel("main_price"),
                        FieldPanel("stock"),
                    ])]

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)

    #     # context["polozkypages"] = self.get_children().live().specific() # works same as the second one
    #     context["polozkypages"] = ProductIndex.get_children(self).live().specific()
    

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")



class ProductVariant(ProductVariantBase):
    product = ParentalKey(Product, related_name = "variants")

    main_price = MoneyField(("Price including VAT"), max_digits = 20, blank = False, null = True, help_text = "Cena položky")
    shop       = models.CharField(max_length = 100, blank = False, null = True, help_text = "Obchod kde se dá položka koupit")

    slug = AutoSlugField(separator = "", populate_from = ("product", "ref")) # populate_from=('product')


    @property
    def price(self):
        return self.main_price.amount

    @property
    def price_money(self):
        return self.main_price

    def save(self, *args, **kwargs):
        self.base_price = self.main_price.amount
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = ("Product variant")
        verbose_name_plural = ("Product variants")


