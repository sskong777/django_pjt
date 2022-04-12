from multiprocessing import AuthenticationError
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'last_name', 'first_name')

