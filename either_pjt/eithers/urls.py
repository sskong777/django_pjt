from django.urls import path
from . import views

app_name ='eithers'
urlpatterns = [
    path('',views.index, name='index'),
    path('create/', views.create, name='create'),
    path('detail/<int:either_pk>/',views.detail,name='detail'),
    path('comment_create/<int:either_pk>/',views.comment_create, name='comment_create'),
]