from rest_framework import serializers
from .models import Article, Comment

# 게시글 1개를 위한 Serializer
class ArticleSerializer(serializers.ModelSerializer):
    # Article 전용 댓글 Serializer 
    class ArticleCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content')
    
    comment_set = ArticleCommentSerializer(many=True, read_only=True)
    comment_cnt = serializers.IntegerField(source='comment_set.count', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('author',)


# 게시글 목록을 위한 Serializer
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', )


# 댓글 하나를 위한 Serializer
class CommentSerializer(serializers.ModelSerializer):
    # 댓글에서 게시글 정보를 보기 위한 Serializer
    class CommentArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('id', 'title',)

    article = CommentArticleSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


# 댓글 목록을 위한 Serializer
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content',)