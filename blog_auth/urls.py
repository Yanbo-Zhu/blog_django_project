from django.urls import path
from . import views

app_name = 'blog_auth'

urlpatterns = [
    path('login', views.zllogin, name='login'),
    path('logout', views.zllogout, name='logout'),
    path('register', views.register, name='register'),
]