from django.db import models

from blog_app.models import Post, User
from datetime import datetime


class Comment(models.Model):
    author = models.ForeignKey(User,  related_name='comments', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    content = models.TextField()
    create_time = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.content[:20]

    class Meta:
        db_table = 'comment'
        ordering = ['-create_time']
