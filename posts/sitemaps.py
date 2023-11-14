from django.contrib.sitemaps import Sitemap

from posts.models import Post, Category
from django.contrib.sites.models import Site




class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"
    
    def items(self):
        return Post.objects.active()



class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
   

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        # Assuming 'name' is a field in your Category model
        return '/category/{}/'.format(obj.name)




