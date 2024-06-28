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
    '''
    1 Using annotate to get the total number of posts in this category
    2 annotate works similarly to all, but also counts the number of posts and names the field num_post, which can be   accessed directly through the category instance
    3 annotate can also work with Avg, Max, Min, etc.
    4 For example, if the Goods model has a price field
    5 Goods.objects.annotate(avg_price=Avg('price')) calculates the average, which can be accessed directly through the avg_price field
    6 Goods.objects.annotate(max_price=Max('price')) calculates the maximum value
    '''
    return Category.objects.annotate(num_post=Count('posts')).filter(num_post__gt=0)

@register.simple_tag
def get_all_tag():
    return Tag.objects.annotate(num_post=Count('posts')).filter(num_post__gt=0)
