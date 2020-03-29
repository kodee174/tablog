from django.urls import re_path
from .views import TagListView, TagDetailView, PostDetailView, PostSearchView

app_name = 'blog'

urlpatterns = [
    re_path(r'^search/$', PostSearchView.as_view(), name='search_post'),
    re_path(r'^search/(?P<search>[-\w]+)/$', PostSearchView.as_view(), name='search_post'),
    re_path(r'^search/(?P<search>[-\w]+)/page-(?P<page>[\d]+)/$', PostSearchView.as_view(), name='search_post'),
    re_path(r'^tags/$', TagListView.as_view(), name='list_tag'),
    re_path(r'^tags/(?P<slug>[-\w]+)/$', TagDetailView.as_view(), name='detail_tag'),
    re_path(r'^tags/(?P<slug>[-\w]+)/page-(?P<page>[\d]+)/$', TagDetailView.as_view(), name='detail_tag'),
    re_path(r'^posts/$', PostDetailView.as_view(), name='list_post'),
    re_path(r'^posts/(?P<slug>[-\w]+)/$', PostDetailView.as_view(), name='detail_post'),
]