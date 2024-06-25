from django import template
from django.db.models import Count, Avg

from blog_app.models import Post, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-create_time")[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'year', order='DESC')


@register.simple_tag
def get_all_category():
    # ?? annotate ???????????
    # annotate ??? all ??????????? post ???????? num_post?????? category ???? num_post ??
    # annotate ????? Avg, Max, Min ?
    # ?? Goods ???? price ??
    # Goods.objects.annotate(avg_price=Avg('price')) ?????????? avg_price ??
    # Goods.objects.annotate(max_price=Max('price)) ????
    return Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)


@register.simple_tag
def get_all_tag():
    return Tag.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)
