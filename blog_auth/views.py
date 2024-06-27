from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # ??
                login(request, user)
                # ?????????
                if not remember:
                    # ?????????????????????0????????????
                    request.session.set_expiry(0)
                # ????????????????????2??????
                return redirect('/')
            else:
                print('????????')
                # form.add_error('email', '?????????')
                # return render(request, 'login.html', context={"form": form})
                return redirect(reverse('zlauth:login'))


def zllogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            # ?????????
            return redirect(reverse('zlauth:register'))
            # return render(request, 'register.html', context={"form": form})