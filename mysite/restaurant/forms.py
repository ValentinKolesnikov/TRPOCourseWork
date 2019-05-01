from django import forms
from catalog.models import Restaurant, Table


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


class AddTable(forms.ModelForm):
    count =  forms.IntegerField(
        label = 'Количество мест',
        max_value=30,
        min_value=1,
    )

    smoke = forms.BooleanField(
        label = 'Можно ли курить',
    )

    window = forms.BooleanField(
        label = 'У окна',
    )

    counttables = forms.IntegerField(
        label = 'Количество столиков',
        max_value=20,
        min_value=1,
    )
    class Meta:
        model = Table
        fields = ('count', 'smoke', 'window', 'counttables')
    