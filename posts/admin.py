from django.contrib import admin
from django.db import models

from pagedown.widgets import AdminPagedownWidget
from .models import Post,Category,BloggerProfile,FooterText,PostPictures


class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp", "category" ]
	list_display_links = ["title","category"]
	# list_editable = ["title"]
	list_filter = ["updated", "timestamp"]

	search_fields = ["title", "content", "maincontent"]

	formfield_overrides = {
		models.TextField: {'widget': AdminPagedownWidget },
	}
	
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)
admin.site.register(Category)
admin.site.register(BloggerProfile)
admin.site.register(PostPictures)

class FooterTextModelAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': AdminPagedownWidget },
	}
	
	class Meta:
		model = FooterText

admin.site.register(FooterText, FooterTextModelAdmin)


