from rest_framework import serializers
from ..models import Article
from django.contrib.auth import get_user_model
from .comment import CommentSerializer

class ArticleSerializer(serializers.ModelSerializer):

    class UserSerialzier(serializers.ModelSerializer):
        class Meta:
            models = get_user_model()
            fields = ('pk','username',)

    comments = CommentSerializer(many=True,read_only=True)
    user = UserSerialzier(read_only=True)
    like_users = UserSerialzier(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('user','pk','title','content','comments','like_users',)
