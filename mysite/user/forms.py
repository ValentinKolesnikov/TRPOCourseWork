from django import forms
from django.contrib.auth.models import User



class EditorUser(forms.ModelForm):   

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

    phone = forms.CharField(
        label='Телефон',
        help_text='',
        required=True,
        max_length=12,
        min_length=12,
    )

    photo = forms.ImageField(
        label='Фотография',
        help_text='',
        required=True,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'photo')
