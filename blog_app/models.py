import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags

# Category of post
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"  # define the table name with 'category', the default valuie is 'blog-category'
        ordering =  ['-id']

# Tag of post
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tag"


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0)  # how many times this post is viewed

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # reverse: return the url of 'blog:post_detail', kwargs contains the input variable
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # The times that the post is already veiwed get increased
    def increase_views(self):
        self.views += 1
        # specify the field to update in order to increase the update efficiency
        self.save(update_fields=['views', ])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # strip_tags: strip the html tag from body. [:50] takes the first 50 characters
            self.excerpt = strip_tags(md.convert(self.body))[:50]
        super(Post, self).save(*args, **kwargs)

    class Meta:
        db_table = "post"
        ordering = ['-create_time']