from django import forms
from .models import Article, Comment
from django.contrib.auth.forms import AuthenticationForm

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ('user', 'like_users',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

