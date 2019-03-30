from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):   

    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }
    username = forms.CharField(
        label='Логин',
        help_text='',
        required=True,
    )

    first_name = forms.CharField(
        label='Имя',
        help_text='',
        required=True,
    )

    last_name = forms.CharField(
        label='Фамилия',
        help_text='',
        required=True,
    )

    password1 = forms.CharField(
        label='Пароль',
        help_text='',
        required=True,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        help_text='',
        required=True,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')