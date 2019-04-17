from django.db import models
from django.forms import ClearableFileInput
from django.contrib.auth.models import User
from  django.utils import timezone


class Restaurant(models.Model):
    
    class Meta():
        db_table = 'Restaurant'
    name = models.CharField(max_length = 120)
    owner = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='restaurant_image', blank=True, default = None)
    description = models.TextField()
    phone = models.CharField(max_length=12)
    worktime = models.CharField(max_length=20)
    mark = models.IntegerField(default='0')

    categories = (
        ('CF', 'Кафе'),
        ('RS', 'Ресторан'),
        ('BR', 'Бар'),
        ('PC', 'Пиццерия'),
        ('KR', 'Караоке'),
        ('BG', 'Бургерная'),
    )

    category = models.CharField(
        max_length = 2,
        choices = categories,
        default = 'RS',
    )

    def getcategory(self):
        for x in self.categories:
           if x[0]==self.category:
              return x[1]

    def __str__(self):
        return self.name

class Table(models.Model):
    count = models.IntegerField(default='4')
    smoke = models.BooleanField()
    window = models.BooleanField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant.name+' ' +str(self.count)

class TimeTable(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    reservation = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.table.__str__()

class Comment(models.Model):
    class Meta():
        db_table = 'Comment'
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Like(models.Model):
    class Meta():
        db_table = 'Like'
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.restaurant.name)