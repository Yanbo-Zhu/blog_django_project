# Generated by Django 5.0.6 on 2024-06-27 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_comment', '0003_alter_comment_author_alter_comment_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
    ]