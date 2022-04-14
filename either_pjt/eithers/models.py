from tkinter import CASCADE
from django.db import models

# Create your models here.

class Either(models.Model):
    title = models.CharField(max_length=20)
    issue_a = models.CharField(max_length=100)
    issue_b = models.CharField(max_length=100)
    

class Comment(models.Model):
    either = models.ForeignKey(Either,on_delete=models.CASCADE)
    pick = models.CharField(max_length=10)
    content = models.CharField(max_length=100)