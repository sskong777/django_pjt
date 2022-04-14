from django.db import models
from django.conf import settings
from accounts.models import User
# Create your models here.

class Todo(models.Model):
    title = models.TextField()
    completed = models.BooleanField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
