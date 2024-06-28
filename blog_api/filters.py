import django_filters

from blog_app.models import Post

'''
example: use 127.0.0.1:8000/api/posts/?title=python

filter function: Define the parameters for filtering. CharFilter is one type of filter parameter, but there are many others, including BooleanFilter, ChoiceFilter, DateFilter, NumberFilter, RangeFilter, etc. The field_name is the name of the parameter to be filtered and must match the name in your model. The lookup_expr specifies the condition for filtering. For example, icontains means case-insensitive containment, while NumberFilter can have conditions like gte, gt, lte, lt, year__gt, year__lt, etc.
'''
class PostFilter(django_filters.rest_framework.FilterSet):
    # designate the filter parameters
    title = django_filters.CharFilter("title", lookup_expr='icontains')

    # designate the model and parameters to be filtered
    class Meta:
        model = Post
        fields = ['title']


