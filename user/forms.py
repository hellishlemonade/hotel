from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from hotel.constants import EMAIL_MAX_LENGTH


User = get_user_model()


class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        max_length=EMAIL_MAX_LENGTH
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )
