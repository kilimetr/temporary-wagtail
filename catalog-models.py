from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from djmoney.models.fields import MoneyField
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from longclaw.products.models import ProductVariantBase, ProductBase



class ProductIndex(Page):
    """Index page for all products
    """
    subpage_types = ('catalog.Product', 'catalog.ProductIndex')

    @property
    def subindexes(self):
        return ProductIndex.objects.child_of(self).live()

    @property
    def products(self):
        return Product.objects.child_of(self).live()


class Product(ProductBase):
    parent_page_types = ['catalog.ProductIndex']
    description = RichTextField(_('Description'))
    additional_info = RichTextField(_('Additional info'),
                                    blank=True,
                                    null=True)
    content_panels = ProductBase.content_panels + [
        FieldPanel('description'),
        FieldPanel('additional_info'),
        InlinePanel('variants',
                    label=_('Product variants'),
                    panels=[
                        FieldPanel('ref'),
                        FieldPanel('stock'),
                        FieldPanel('description'),
                    ]),
    ]

    @property
    def first_image(self):
        return self.images.first()


    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductVariant(ProductVariantBase):
    """Represents a 'variant' of a product
    """
    # You *could* do away with the 'Product' concept entirely - e.g. if you only
    # want to support 1 'variant' per 'product'.
    product = ParentalKey(Product, related_name='variants')

    vat = models.IntegerField(_('VAT'))
    main_price = MoneyField(_("price"), max_digits = 5)

    slug = AutoSlugField(
        separator='',
        populate_from=('product', 'ref'),
    )

    # Enter your custom product variant fields here
    # e.g. colour, size, stock and so on.
    # Remember, ProductVariantBase provides 'price', 'ref' and 'stock' fields
    description = RichTextField()


    @property
    def price(self):
        return self.main_price

    @property
    def price_money(self):
        return self.main_price.amount

    def get_product_title(self):
        try:
            return self.product.title
        except AttributeError:
            return self.ref

    def save(self, *args, **kwargs):
        self.base_price = 6
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product variant')
        verbose_name_plural = _('Product variants')



