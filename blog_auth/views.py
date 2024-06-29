from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User_all = get_user_model()

# login view
@require_http_methods(['GET', 'POST'])
def to_login(request):
    if request.method == 'GET':
        return render(request, 'blog_auth/login.html')
    else:
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            print(username, password, remember)

            user = User_all.objects.filter(username=username).first()
            if user and user.check_password(password):
                # to login
                login(request, user)
                # to judge remember me
                if not remember:
                    # if not remember me, set the expiry time to 0, that is, it will expire after the browser is closed
                    request.session.set_expiry(0)
                # if clicked, do nothing, use the default 2-week expiration time
                return redirect(reverse('blog_app:home'))
            else:
                print('Login failed!')
                return redirect(reverse('blog_auth:login'))

# logout view
def to_logout(request):
    logout(request)
    return redirect('/auth/login')

# register view
@require_http_methods(['GET', 'POST'])
def to_register(request):
    if request.method == 'GET':
        return render(request, 'blog_auth/register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User_all.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('blog_auth:login'))
        else:
            print(form.errors)
            return redirect(reverse('blog_auth:register'))
