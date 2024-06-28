from django.urls import re_path
from . import views

# Include app_name with the same value as the namespace in the include statement, otherwise the URLs might not be found.
app_name = 'blog_app'

urlpatterns = [
    re_path(r'^home/$', views.HomeView.as_view(), name='home'),

    re_path(r'^full/$', views.FullPostView.as_view(), name='full'),

    re_path(r'^about/$', views.about, name='about'),

    re_path(r'^contact/$', views.contact, name='contact'),

    re_path(r'^post/new/$', views.new_post, name='new_post'),

    re_path(r'^search/$', views.search, name='search'),

    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name="detail"),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name="detail"),

    re_path(r'^query/$', views.query, name='query'),

    # url(r'^archives/(?P<year>[0-9]{4})/$', views.archives, name="archives"),
    re_path(r'^archives/(?P<year>[0-9]{4})/$', views.ArchivesView.as_view(), name="archives"),

    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name="category"),
    re_path(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),

    #re_path(r'^tag/(?P<pk>[0-9]+)/$', views.tags, name='tags'),
    re_path(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tags'),
]
