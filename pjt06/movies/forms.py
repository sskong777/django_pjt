from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    GENRE_1 = "comedy"
    GENRE_2 = "horror"
    GENRE_3 = "romance"
    GENRE_CHOICES = [
        (GENRE_1, "comedy"),
        (GENRE_2, "horror"),
        (GENRE_3, "romance"),
    ]
    genre = forms.ChoiceField(choices=GENRE_CHOICES, widget=forms.Select())

    score = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'min': '0',
                'max': '5',
                'step': '0.5',
            }
        )        
    )

    release_date = forms.DateTimeField(
        # input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'type':'date',

            # 'class': 'form-control datetimepicker-input',
            # 'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Movie
        fields = '__all__'
         
