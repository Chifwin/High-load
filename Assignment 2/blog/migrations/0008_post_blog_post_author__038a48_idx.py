# Generated by Django 5.1.1 on 2024-10-10 07:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_post_blog_post_author__038a48_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author'], name='blog_post_author__038a48_idx'),
        ),
    ]
