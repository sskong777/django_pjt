from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)