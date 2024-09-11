from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.updated_at = timezone.now()
        super().save(**kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Comment(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()


