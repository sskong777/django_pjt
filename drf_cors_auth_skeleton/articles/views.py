from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Article, Comment
from .serializers import (
    ArticleListSerializer, 
    ArticleSerializer,
    CommentListSerializer,
    CommentSerializer
)


@api_view(['GET', 'POST'])
def articles_cr(request):

    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializers = ArticleListSerializer(articles, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializers = ArticleSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            ################## ##################
            serializers.save(author=request.user)
            return Response(serializers.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def article_rud(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializers = ArticleSerializer(article)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializers = ArticleSerializer(article, request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response({ id: article_pk }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comments_cr(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = article.comment_set.all()
        serializers = CommentListSerializer(comments, many=True)
        return Response(serializers.data)

    elif request.method == 'POST':
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            ######################################################
            serializers.save(article=article, author=request.uesr)
            return Response(serializers.data)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_rud(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializers = CommentSerializer(comment)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializers = CommentSerializer(comment, request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response({ 'id': comment_pk }, status=status.HTTP_204_NO_CONTENT)