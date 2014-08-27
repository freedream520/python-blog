from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Category, Article
import calendar
import datetime
from django.core.urlresolvers import reverse
from django_ajax.decorators import ajax
from django.core import serializers

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def index(request):
    """The news index"""
    archive_dates = Article.objects.dates('date_publish', 'month', order='DESC')
    categories = Category.objects.all()

    page = request.GET.get('page')
    article_queryset = Article.objects.all()
    paginator = Paginator(article_queryset, 7)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    #print("index", articles)

    return render(
        request,
        "blog/article/index.html",
        {
            "articles": articles,
            "archive_dates": archive_dates,
            "categories": categories
        }
    )


@ajax
def scroll_load(request):
    page = request.GET.get('page')
    article_queryset = Article.objects.all()
    paginator = Paginator(article_queryset, 7)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return {"articles": serializers.serialize('json', articles)}

@ajax
def random_list(request):
    article_queryset = Article.objects.all()
    import random
    count = article_queryset.count()
    list1 = []
    for i in range(7):
        a = random.randint(1, count)
        while a in list1:
            if a == count:
                a = 0
            a += 1
        list1.append(a)

    articles = [article_queryset[i-1] for i in list1]

    return {"list": list1, "articles": serializers.serialize('json', articles)}


@ajax
def relate_list(request, title):
    pass


def single(request, slug):
    """A single article"""
    article = get_object_or_404(Article, slug=slug)
    archive_dates = Article.objects.dates('date_publish', 'month', order='DESC')
    categories = Category.objects.all()
    prev = Article.objects.filter(date_publish__gt=article.date_publish).order_by("date_publish")
    prev = prev[0] if prev else "none"
    nex = Article.objects.filter(date_publish__lt=article.date_publish).order_by("-date_publish")
    nex = nex[0] if nex else ""
    
    return render(request, "blog/article/single.html",
                  {"article": article, "archive_dates": archive_dates, "categories": categories, "prev": prev,
                   "nex": nex})


def date_archive(request, year, month):
    """The blog date archive"""
    # this archive pages dates
    year = int(year)
    month = int(month)
    month_range = calendar.monthrange(year, month)
    start = datetime.datetime(year=year, month=month, day=1)
    end = datetime.datetime(year=year, month=month, day=month_range[1])
    archive_dates = Article.objects.dates('date_publish', 'month', order='DESC')
    categories = Category.objects.all()

    # Pagination
    page = request.GET.get('page')
    article_queryset = Article.objects.filter(date_publish__range=(start.date(), end.date()))
    paginator = Paginator(article_queryset, 5)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(
        request,
        "blog/article/date_archive.html",
        {
            "start": start,
            "end": end,
            "articles": articles,
            "archive_dates": archive_dates,
            "categories": categories
        }
    )


def category_archive(request, slug):
    archive_dates = Article.objects.dates('date_publish', 'month', order='DESC')
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)

    # Pagination
    page = request.GET.get('page')
    article_queryset = Article.objects.filter(categories=category)
    paginator = Paginator(article_queryset, 5)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/article/category_archive.html",
        {
            "articles": articles,
            "archive_dates": archive_dates,
            "categories": categories,
            "category": category
        }
    )


def search_result(request, keyword=""):
    if request.method == "POST":
        keyword = request.POST['keyword']
        print(keyword)
        return redirect(
            reverse("blog:blog_article_search_result", kwargs={'keyword': keyword})
        )

    title_set = Article.objects.filter(title__icontains=keyword)
    article_set = Article.objects.filter(content_markdown__icontains=keyword)
    result = {}.fromkeys(title_set | article_set).keys()
    categories = Category.objects.all()
    #if the query is null
    if not result:
        return render(request, "blog/article/index.html",{
            "articles": "null",
            "categories": categories
        })

    page = request.GET.get('page')
    paginator = Paginator(result, 5)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    print("redirect", result)
    return render(
        request,
        "blog/article/index.html",
        {
            "articles": articles,
            "categories": categories
        }
    )