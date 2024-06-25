import datetime

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Hello django")


def index(request):
    title = "My Blog Home"
    welcome = "Welcome to My Blog"
    return render(request, 'blog_app/index.html', locals())


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError as e:
        print(e)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("{} hours later is {}".format(offset, dt))