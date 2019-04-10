from django import forms
from catalog.models import Restaurant


class EditorRestaurant(forms.ModelForm):   

    name = forms.CharField(
        label='Название',
        help_text='',
        required=True,
    )

    description = forms.CharField(
        label = 'Описание',
    )

    worktime = forms.CharField(
        label = 'Время работы',
    )
    
    category = forms.ChoiceField(
        label = 'Категория',
        choices = Restaurant.categories,
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
        fields = ('name', 'description', 'worktime', 'category','phone',  'photo')
