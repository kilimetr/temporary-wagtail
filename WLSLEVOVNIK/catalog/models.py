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

VAT_1 = 1
VAT_2 = 2
VAT_3 = 3

VAT_RATIOS = {
    VAT_1: Decimal(1.21),
    VAT_2: Decimal(1.15),
    VAT_3: Decimal(1.10),
}

# TODO: Add automatic calculation
VAT_CHOICES = (
    (VAT_1, '21%'),
    (VAT_2, '15%'),
    (VAT_3, '10%'),
)


class VATPrice(models.Model):
    price_no_vat = MoneyField(_('Price without VAT'),
                              max_digits=10,
                              editable=True)
    vat = models.IntegerField(_('VAT'), choices=VAT_CHOICES, default=VAT_1)
    main_price = MoneyField(_('Price including VAT'), max_digits=10)

    def save(self, *args, **kwargs):
        self.price_no_vat = self.price / VAT_RATIOS[self.vat]
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ProductIndex(Page):
    """Index page for all products
    """
    subpage_types = ('catalog.Product', 'catalog.ProductIndex')

    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.SET_NULL,
                              related_name='+',
                              null=True,
                              blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
    ]

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
        InlinePanel('images', label=_('Images')),
        InlinePanel('variants',
                    label=_('Product variants'),
                    panels=[
                        FieldPanel('ref'),
                        FieldPanel('vat'),
                        FieldPanel('main_price'),
                        FieldPanel('stock'),
                        FieldPanel('description'),
                    ]),
    ]

    @property
    def first_image(self):
        return self.images.first()

    @property
    def price_range(self):
        """ Calculate the price range of the products variants
        """
        ordered = self.variants.order_by('main_price')
        if ordered:
            return ordered.first().price, ordered.last().price
        else:
            return None, None

    @property
    def price_range_money(self):
        """ Calculate the price range of the products variants
        """
        ordered = self.variants.order_by('main_price')
        if ordered:
            return ordered.first().price_money, ordered.last().price_money
        else:
            return None, None

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductVariant(ProductVariantBase, VATPrice):
    """Represents a 'variant' of a product
    """
    # You *could* do away with the 'Product' concept entirely - e.g. if you only
    # want to support 1 'variant' per 'product'.
    product = ParentalKey(Product, related_name='variants')

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
        return self.main_price.amount

    @property
    def price_money(self):
        return self.main_price

    def get_product_title(self):
        try:
            return self.product.title
        except AttributeError:
            return self.ref

    def save(self, *args, **kwargs):
        self.base_price = self.main_price.amount
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product variant')
        verbose_name_plural = _('Product variants')


class ProductImage(Orderable):
    """Example of adding images related to a product model
    """
    product = ParentalKey(Product, related_name='images')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE,
                              related_name='+')
    caption = models.CharField(blank=True, max_length=255)

    panels = [ImageChooserPanel('image'), FieldPanel('caption')]

    class Meta:
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')