from django.db import models
from django.forms import ClearableFileInput
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.name

class Comment(models.Model):
    class Meta():
        db_table = 'Comment'
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField()
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Like(models.Model):
    class Meta():
        db_table = 'Like'
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)