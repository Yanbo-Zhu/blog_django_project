from django.contrib import admin

# Register your models here.
from django.contrib import admin
from blog_comment.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'email', 'post','create_time','content']
    list_per_page = 10
    list_filter = [ 'author','post' ]
    search_fields = ['author','post']
    date_hierarchy = 'create_time'
    ordering = ('id',)
