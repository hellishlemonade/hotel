from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, ButtonHolder, Submit, Field
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<div class="my-form">Регистрация</div>'),
            Field('email'),
            Field('first_name'),
            Field('last_name'),
            Field('password1'),
            Field('password2'),
            ButtonHolder(
                Submit(
                    'submit', 'Зарегистрироваться', css_class='button white')
            )
        )


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<div class="my-form">Вход</div>'),
            Field('username'),
            Field('password'),
            ButtonHolder(
                Submit(
                    'submit', 'Войти', css_class='button white')
            )
        )
