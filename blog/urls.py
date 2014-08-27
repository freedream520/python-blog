from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^blog/archive/(?P<year>[\d]+)/(?P<month>[\d]+)/$', 'blog.views.date_archive', name="blog_date_archive"),
    url(r'^blog/archive/(?P<slug>[-\w]+)/$', 'blog.views.category_archive', name="blog_category_archive"),
    url(r'^blog/(?P<slug>[-\w]+)/$', 'blog.views.single', name="blog_article_single"),
    url(r'^$', 'blog.views.index', name="blog_article_index"),
    url(r'^scroll_load/$', 'blog.views.scroll_load', name="blog_article_scroll_load"),
    url(r'^search/$', 'blog.views.search_result', name="blog_article_search"),
    url(r'^search/(?P<keyword>[^/]+)/$', 'blog.views.search_result', name="blog_article_search_result"),
    url(r'^random-list/$', 'blog.views.random_list', name="blog_article_random_list"),
    url(r'^relate-list/(?P<title>[^/]+)/$', 'blog.views.relate_list', name="blog_article_relate_list"),
)