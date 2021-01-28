from django.db import models

from wagtail.admin.edit_handlers 	 import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting



@register_setting
class NastaveniSocialnichMedii(BaseSetting):
	facebook             = models.URLField(blank = True, null = True, help_text = "Facebook URL")
	twitter              = models.URLField(blank = True, null = True, help_text = "Twitter URL")
	youtube              = models.URLField(blank = True, null = True, help_text = "Youtube URL")
	instagram            = models.URLField(blank = True, null = True, help_text = "Instagram URL")
	linkedin             = models.URLField(blank = True, null = True, help_text = "Linkedin URL")
	
	panels = [
		MultiFieldPanel([
				FieldPanel("facebook"),
				FieldPanel("twitter"),
				FieldPanel("youtube"),
				FieldPanel("instagram"),
				FieldPanel("linkedin"),

			],
			heading = "Nastavení sociálních medií"),
	]



