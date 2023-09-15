from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from markdown_deux import markdown

from django.contrib import admin

from django.contrib.auth.models import User



class PostManager(models.Manager):
    def active(self, *args, **kwargs):
   
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):

    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1

    return "blog_pic/%s/%s" % ( new_id, filename)

def upload_location_pic(instance, filename):
    return '%s/%s' % ( instance.category.name, filename)

def upload_location_photo(instance, filename):
    return 'blogger_pic/%s/%s' % ( instance.user, filename)



class BloggerProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,)
    image = models.CharField(max_length=200 ,blank=True)
    image_2 = models.ImageField(upload_to=upload_location_photo,
            blank=True,
            null=True,             
            )
    about = models.TextField(blank=True)
    fb_link = models.CharField(max_length=200 ,blank=True)
    twitter_link = models.CharField(max_length=200 ,blank=True)
    linkdin_link = models.CharField(max_length=200, blank=True )

    def __str__(self):
        return (self.user.username)

    class Meta:       
        verbose_name_plural = "Bloggers"

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    keywords = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return '/'+self.name+'/'

class FooterText(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    updated = models.DateField(auto_now=True, auto_now_add=False)   
    
    def __str__(self):
        return str(self.name)

class PostPictures(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=90)
    image_1 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,

            )
    image_2 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )
    image_3 = models.ImageField(upload_to=upload_location_pic,
                         
            blank=True,
            null=True,             
            )
    image_4 = models.ImageField(upload_to=upload_location_pic,             
            blank=True,
            null=True,
            )
    image_5 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )
    image_6 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )
    image_7 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )
    image_8 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )
    image_9 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )
    image_10 = models.ImageField(upload_to=upload_location_pic,
            blank=True,
            null=True,             
            )

    def __str__(self):
        return str(self.post_title)

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(BloggerProfile, default=1)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=300)
    keywords = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, blank=True, max_length=70)
    image = models.ImageField(upload_to=upload_location,
	    blank=True,
            null=True,        
            width_field="width_field", 
            height_field="height_field")
    image_thumbnail_1 = ImageSpecField(source='image',
            processors=[ResizeToFill(450, 300)],            
            options={'quality': 50})
	
    image_thumbnail_2 = ImageSpecField(source='image',
            processors = [ResizeToFill(130, 110)],             
            options={'quality': 50})

    image_description = models.CharField(max_length=300)
    video = models.CharField(blank=True, max_length=200)
    content = models.TextField()      
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    viewed = models.IntegerField(default=0)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)


# posts_category
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)










