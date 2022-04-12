from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    # RADIO_SELECT = [
    #     (1, '1번이염'),
    #     (2, '2번이염'),
    #     (3, '3번이염')
    # ]
    # # title 입력은 TextInput이 아닌 TextArea로 변경
    # title = forms.CharField(widget=forms.Textarea(
    #     attrs = {
    #         'rows':'3',
    #         'class': 'w-100 m-5'
    #     }
    # ))
    # check_test_ssafy7 = forms.CharField(
    #     widget = forms.CheckboxInput(),
    #     required = False
    # )
    # radio_test_ssafy7 = forms.CharField(
    #     widget = forms.RadioSelect(choices=RADIO_SELECT)
    # )
    class Meta:
        model = Article
        fields = '__all__'
