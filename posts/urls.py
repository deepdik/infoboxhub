from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_detail,
    category_view,
    home_page,
    footer_view
)

urlpatterns = [
    url(r'^$', home_page, name='home_page'),
    url(r'^category/(?P<name>[\w.@+-]+)/$', category_view, name='category_list'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^IBH/(?P<footer>[\w.@+-]+)/$', footer_view, name='footer_view'),
]

handler404 = 'posts.views.handler404'
handler500 = 'posts.views.handler500'
handler400 = 'posts.views.handler400'
