from django.urls import re_path, include
from .views import HomePageView, AboutView, ContactView

app_name = 'cores'

urlpatterns = [
    re_path(r'^$', HomePageView.as_view(), name='homepage'),
    re_path(r'^page-(?P<page>[\d]+)/$', HomePageView.as_view(), name='homepage'),
    re_path(r'^about/$', AboutView.as_view(), name='about'),
    re_path(r'^contact/$', ContactView.as_view(), name='contact'),
    re_path(r'', include('users.urls')),
    re_path(r'', include('blog.urls')),
]
