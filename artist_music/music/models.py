from django.db import models
from django.forms import CharField

# Create  your models here.

class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.artist} : {self.title}'

    