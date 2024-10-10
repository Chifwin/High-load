from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from .cache_util import comments_cache_dec


class CustomUser(User):
    bio = models.TextField(max_length=1000, null=True, blank=True)


class Tag(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=['title'])]

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    @property
    @comments_cache_dec
    def comments_count(self):
        return self.comments.count()

    def __int__(self):
        return self.id

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["author"]),
        ]


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["post", "created_at"]),
        ]
