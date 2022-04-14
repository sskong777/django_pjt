from random import choices
from django import forms
from .models import Either,Comment


class EitherForm(forms.ModelForm):
    class Meta:
        model = Either
        fields = '__all__'


class CommentForm(forms.ModelForm):
    PICKS = [
        ('red', 'RED'),
        ('blue', 'BLUE')
    ]
    pick = forms.CharField(
        widget=forms.Select(choices=PICKS)
    )
    class Meta:
        model = Comment
        fields = ('pick','content',)