from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from catalog.models import Restaurant
from django.forms import ClearableFileInput


class EditorRestaurant(forms.ModelForm):   

    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }

    name = forms.CharField(
        label='Название',
        help_text='',
        required=True,
    )

    description = forms.CharField(
        label='Описание',
        help_text='',
        required=True,
    )

    phone = forms.CharField(
        label='Телефон',
        help_text='',
        required=True,
        max_length=12,
        min_length=12,
    )

    photo = forms.ImageField(
        label='Фотография заведения',
        help_text='',
        required=True,
    )

    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'phone', 'photo')
