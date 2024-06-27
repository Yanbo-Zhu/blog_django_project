from django import forms
from .models import Post


# ??????? forms.ModelForm ?? forms.Form ?????????????? ModelForm ???
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'tags', 'author']