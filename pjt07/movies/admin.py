from django.contrib import admin
from .models import Movie,Comment
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.admin impor
# Register your models here.

admin.site.register(Movie)
admin.site.register(Comment)
