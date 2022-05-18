from django.urls import path

from . import views


app_name = 'articles'

urlpatterns = [
    # 게시글 
    path('', views.articles_cr, name='article_cr'),
    path('<int:article_pk>/', views.article_rud, name='article_rud'),

    # 댓글
    path('<int:article_pk>/comments/', views.comments_cr, name='comments_cr'),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_rud, name='comment_rud'),
]
