from django.urls import re_path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
#router.register(r'post', views.PostViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
urlpatterns = [
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='api_post'),
]

urlpatterns += router.urls

