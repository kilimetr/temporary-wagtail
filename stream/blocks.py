from wagtail.core		   import blocks
from wagtail.images.blocks import ImageChooserBlock
# STREAMFIELDS LIVE IN HERE


class TitleAndTextBlock(blocks.StructBlock):
	# TITLE AND TEXT AND NOTHING ELSE

	title = blocks.CharBlock(required = True, help_text = "Add title")
	text  = blocks.TextBlock(required = True, help_text = "Add additional text")


	class Meta:
		template = "streams/title_and_text_block.html"
		icon     = "edit"
		label    = "Title & Text"



class RichtextBlock(blocks.RichTextBlock):

	class Meta:
		template = "streams/richtext_block.html"
		icon     = "doc-full"
		label    = "Full RichText"



class SimpleRichtextBlock(blocks.RichTextBlock):

	def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
		super().__init__(**kwargs)
		self.features = ["bold", "italic", "link"]

	class Meta:
		template = "streams/richtext_block.html"
		icon     = "edit"
		label    = "Sample RichText"



class CardBlock(blocks.StructBlock):
	# CARDS WITH IMAGE AND TEXT AND BUTTON(S)

	title = blocks.CharBlock(required = True, help_text = "Add your title")

	cards = blocks.ListBlock(blocks.StructBlock(
		[
			("image",       ImageChooserBlock(      required = True)),
			("title",       blocks.CharBlock(       required = True, max_lenght = 40)),
			("text",        blocks.TextBlock(       required = True, max_lenght = 200)),
			("button_page", blocks.PageChooserBlock(required = False)),
			("button_url",  blocks.URLBlock(        required = False, help_text = "if the button page is selected, that will be used first.")),
		]
		))

	class Meta:
		template = "streams/card_block.html"
		icon     = "placeholder"
		label    = "Staff Cards"
			


class CTABlock(blocks.StructBlock):
	# SIMPLE CALL TO ACTION SECTION

	title       = blocks.CharBlock(required = True, max_lenght = 60)
	text        = blocks.RichTextBlock(required = True, features = ["bold", "italic"])
	button_page = blocks.PageChooserBlock(required = False) # internal
	button_url  = blocks.URLBlock(required = False) # external
	button_text = blocks.CharBlock(required = True, default = "Learn More", max_lenght = 40)

	class Meta:
		template = "streams/cta_block.html"
		icon     = "placeholder"
		label    = "Call to Action"





			# STREAMFIELD LOGIC - button optional
class LinkStructValue(blocks.StructValue):
	# ADDITIONAL STREAMFIELD LOGIC TO ButtonBlock

	def url(self):
		button_page = self.get("button_page")
		button_url  = self.get("button_url")

		if button_page:
			return button_page.url
		elif button_url:
			return button_url
		else:
			return None

	def latest_blog_posts(self):
		return BlogDetailPage.objects.live()[:3]



			# STREAMFIELD LOGIC
class ButtonBlock(blocks.StructBlock):
	# EXTERNAL OR INTERNAL URL
	button_page = blocks.PageChooserBlock(required = False, help_text = "if selected, this url will be used first") # internal
	button_url  = blocks.URLBlock(required = False, help_text = "if added, this url will be used secondarily to the button page") # external
	

	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)
		# context["latest_blog_posts"] = BlogDetailPage.objects.live().public()[:3]
		return context


	class Meta:
			template    = "streams/button_block.html"
			icon        = "placeholder"
			label       = "Single Button"
			value_class = LinkStructValue

		

