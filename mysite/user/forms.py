from django import forms
from catalog.models import User


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

    class Meta:
        model = User
        fields = ('first_name', 'last_name')