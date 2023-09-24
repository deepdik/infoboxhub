try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category, FooterText, BloggerProfile

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache


def addsView(request):
    return render(request, 'ads.html')


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    title = instance.title
    author = instance.user
    img = instance.image
    keywords = instance.keywords
    description = instance.description
    share_description = quote_plus(instance.description)
    share_title = quote_plus(instance.title)

    old_views = instance.viewed
    new_views = old_views + 1
    instance.viewed = new_views
    instance.save()  #

    category_id = instance.category_id
    most_popular = Post.objects.active().order_by('-viewed')[:5]
    latest_post = Post.objects.active().order_by('-publish').filter(category__id=category_id).exclude(slug=slug)

    queryset_list = Post.objects.active()
    query = request.GET.get("q")
    if query:
        latest_post = queryset_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query) |
            Q(user__user__first_name__icontains=query) |
            Q(user__user__last_name__icontains=query) |
            Q(user__about__icontains=query)
        ).distinct()

    search_post_count = latest_post.count()
    paginator = Paginator(latest_post, 10)  # Show 25 contacts per page
    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.filter(is_active=True).values("name", "description", "svg_class").order_by('order')
        # Cache the queryset with a specified timeout (e.g., 300 seconds)
        cache.set('categories', categories, 3600)

    context = {
        "post_detail": instance,
        "popular": most_popular,
        "latest": queryset,
        "title": title,
        "author": author,
        "img": img,
        "description": description,
        "keywords": keywords,
        "count": search_post_count,
        "share_description": share_description,
        "share_title": share_title,
        "categories": categories
    }
    return render(request, "post_detail.html", context)


def category_view(request, name):
    today = timezone.now().date()
    latest = Post.objects.active().order_by('-publish').filter(category__name=name)[:1]
    popular = Post.objects.active().order_by('-viewed')[:5]
    latest_post = Post.objects.active().order_by('-publish').filter(category__name=name)

    queryset_list = Post.objects.active()
    query = request.GET.get("q")
    if query:
        latest_post = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(description__icontains=query) |
            Q(user__user__first_name__icontains=query) |
            Q(user__user__last_name__icontains=query) |
            Q(user__about__icontains=query)
        ).distinct()

    search_post_count = latest_post.count()
    paginator = Paginator(latest_post, 10)  # Show 25 contacts per page
    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    instance = get_object_or_404(Category, name=name)
    description = instance.description
    keywords = instance.keywords

    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.filter(is_active=True).values("name", "description", "svg_class").order_by('order')
        # Cache the queryset with a specified timeout (e.g., 300 seconds)
        cache.set('categories', categories, 3600)

    context = {
        "object_list": queryset,
        "title": name,
        "description": description,
        "keywords": keywords,
        "today": today,
        "latest": latest,
        "most_popular": popular,
        "count": search_post_count,
        "categories": categories

    }
    return render(request, "post_list.html", context)


def home_page(request):
    main_latest_post = Post.objects.active().order_by('-publish')[:1]
    popular_post = Post.objects.active().order_by('-viewed')[:5]
    latest_post = Post.objects.active().order_by('-publish')

    queryset_list = Post.objects.active()
    query = request.GET.get("q")
    if query:
        latest_post = queryset_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query) |
            Q(user__user__first_name__icontains=query) |
            Q(user__user__last_name__icontains=query) |
            Q(user__about__icontains=query)
        ).distinct()

    search_post_count = latest_post.count()

    paginator = Paginator(latest_post, 10)  # Show 25 contacts per page

    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.filter(is_active=True).values("name", "description", "svg_class").order_by('order')
        # Cache the queryset with a specified timeout (e.g., 300 seconds)
        cache.set('categories', categories, 3600)

    context = {
        "popular": popular_post,
        "latest": queryset,
        "main_latest": main_latest_post,
        "count": search_post_count,
        "categories": categories

    }
    return render(request, "home_page.html", context)


def footer_view(request, footer=None):
    instance = get_object_or_404(FooterText, name=footer)
    popular_post = Post.objects.active().order_by('-viewed')[:5]
    latest_post = Post.objects.active().order_by('-publish')
    queryset_list = Post.objects.active()
    query = request.GET.get("q")
    if query:
        latest_post = queryset_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(content__icontains=query) |
            Q(user__user__first_name__icontains=query) |
            Q(user__user__last_name__icontains=query) |
            Q(user__about__icontains=query)
        ).distinct()

    search_post_count = latest_post.count()

    paginator = Paginator(latest_post, 10)  # Show 25 contacts per page

    page = request.GET.get("page")
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    our_team = BloggerProfile.objects.all()

    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.filter(is_active=True).values("name", "description", "svg_class").order_by('order')
        # Cache the queryset with a specified timeout (e.g., 300 seconds)
        cache.set('categories', categories, 3600)

    context = {
        "footer_text": instance,
        "popular": popular_post,
        "latest": queryset,
        "title": footer,
        "count": search_post_count,
        "our_team": our_team,
        "categories": categories
    }
    return render(request, "footer_text.html", context)


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def handler400(request):
    return render(request, '400.html', status=400)
