from django.urls import path
from . import views

app_name = 'blog_auth'

urlpatterns = [
    path('login', views.to_login, name='login'),
    path('logout', views.to_logout, name='logout'),
    path('register', views.to_register, name='register'),
]