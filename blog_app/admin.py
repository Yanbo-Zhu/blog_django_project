from django.contrib import admin
from blog_app.models import Post, Category, Tag


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category' , 'views' ]
    list_per_page = 20
    list_filter = ( 'title','tags')
    search_fields = ('title','create_time')
    date_hierarchy = 'create_time'
    ordering = ('id',)
    filter_horizontal = ('tags',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('tag',)

admin.site.site_header = "Blog Manager System"
admin.site.site_title = "Blog Manager"