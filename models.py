from django.db import models

from wagtail.core.models                  import Page
from wagtail.admin.edit_handlers          import FieldPanel
from wagtail.images.edit_handlers         import ImageChooserPanel
from wagtail.admin.edit_handlers          import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin


from django_extensions.db.fields          import AutoSlugField
from djmoney.models.fields                import MoneyField
from modelcluster.fields                  import ParentalKey
from wagtail.admin.edit_handlers          import InlinePanel
from longclaw.products.models             import ProductVariantBase, ProductBase



class PolozkaPageLONGCLAW(ProductBase):
    parent_page = ["polozka.PolozkaListingPage"]

    template = "polozka/polozka_page.html"

    picture = models.URLField(max_length = 1000, blank = True,  null = True, help_text = "Odkaz obrázku položky")
    name    = models.CharField(max_length = 100, blank = False, null = True, help_text = "Název položky")
    price   = models.FloatField(                 blank = False, null = True, help_text = "Cena položky")
    # shop    = models.CharField(max_length = 100, blank = False, null = True, help_text = "Obchod kde se dá položka koupit")


    content_panels = ProductBase.content_panels + [
        MultiFieldPanel([
            FieldPanel("picture"),
            FieldPanel("name"),
            FieldPanel("price"),
            # FieldPanel("shop"),
            ],
            heading = "Polozka content"),
        InlinePanel("polozka_variant_longclaw",
            panels = [
                FieldPanel("shop"),
                ], 
            label = ("Polozka Variant"))
        ]


    class Meta:
        verbose_name = "Polozka_vn"
        verbose_name_plural = "Polozka_vnp"



class PolozkaVariantLONGCLAW(ProductVariantBase):
    product = ParentalKey(PolozkaPageLONGCLAW, related_name = "polozka_variant_longclaw")

    shop = models.CharField(max_length = 100, blank = False, null = True, help_text = "Obchod kde se dá položka koupit")


# class PolozkaListingPage(RoutablePageMixin, Page):
class PolozkaListingPage(Page):
    subpage = ["polozka.PolozkaPageLONGCLAW"]

    template = "polozka/polozka_listing_page.html"

    custom_title = models.CharField(max_length = 100, blank = True, null = True, help_text = "Přepiš původní titulek")

    content_panels = Page.content_panels + [FieldPanel("custom_title"),]


    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        # sitemap.append({
            # "location": self.full_url + self.reverse_subpage("latest_posts"),
            # })

        return sitemap

    @property
    def products(self): # equivalent to get_context
        return Product.objects.child_of(self).live()

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)

    #     # context["polozkypages"] = self.get_children().live().specific() # works same as the second one
    #     context["polozkypages"] = PolozkaListingPage.get_children(self).live().specific()
    
    #   # pagination
    #   all_posts = BlogDetailPage.objects.live().public().order_by("-first_published_at")

    #   paginator = Paginator(all_posts, 2) # 1 post per page
    #   page = request.GET.get("page") # page = 1, page = 2, ...

    #   try:
    #       posts = paginator.page(page)
    #   except PageNotAnInteger:
    #       posts = paginator.page(1)
    #   except EmptyPage:
    #       posts = paginator.page(paginator.num_pages)

    #   context["posts"] = posts

        # return context
