from django.urls import re_path
from . import views

# ?? app_name, ?? include ? namespace ??????????? url
app_name = 'blog_app'
urlpatterns = [
    # <a href="{% url 'blog:home' %}"><b>Home</b></a>
    re_path(r'^home$', views.home, name='home'),
    re_path(r'^time/ahead/(?P<offset>\d{1,2})/$', views.hours_ahead, name="time_ahead"),
    re_path(r'^index$', views.index, name="index")
]