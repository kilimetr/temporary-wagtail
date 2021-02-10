from django.db import models

from wagtail.core.models 		  import Page
from wagtail.admin.edit_handlers  import FieldPanel, MultiFieldPanel
from wagtail.core.fields		  import RichTextField


class User_ProfilePage(Page):
	templates = "user_profile/user_profile_page.html"

	titlee 		= models.CharField(max_length = 100, blank = False, null = True)
	description = RichTextField()

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel("titlee"),
			FieldPanel("description"),
			],
			heading = "User Profile content"),
		]


	class Meta:
		verbose_name = "User profile_vn"
		verbose_name_plural = "User profile_vnp"





