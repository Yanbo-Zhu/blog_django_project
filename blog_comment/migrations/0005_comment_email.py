# Generated by Django 5.0.6 on 2024-06-27 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_comment', '0004_remove_comment_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='ybzhu@sina.com', max_length=255),
        ),
    ]
