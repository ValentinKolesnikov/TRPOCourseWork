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
    worktime = models.CharField(max_length=50)
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
    
    def __get_worktime__(self):
        return self.worktime

    def getcategory(self):
        for x in self.categories:
           if x[0]==self.category:
              return x[1]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            wk = Week.objects.get(restaurant = self)
            wk.timework =  self.worktime
        except:
            wk = Week(restaurant = self, timework = self.worktime)
        wk.save()


class Week(models.Model):
    class Meta():
        db_table = 'Week'
    monday = models.CharField(max_length = 15, default='Выходной 0')
    tuesday = models.CharField(max_length = 15, default='Выходной 0')
    wednesday = models.CharField(max_length = 15, default='Выходной 0')
    thursday = models.CharField(max_length = 15, default='Выходной 0')
    friday = models.CharField(max_length = 15, default='Выходной 0')
    saturday = models.CharField(max_length = 15, default='Выходной 0')
    sunday = models.CharField(max_length = 15, default='Выходной 0')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    timework = models.CharField(max_length=50, default = 'Пн-Пт 10:00-18:00')

    def set_day(self, day, timework):
        if(day=='ПН'):
            self.monday = timework
        elif(day=='ВТ'):
            self.tuesday  = timework
        elif(day=='СР'):
            self.wednesday = timework
        elif(day=='ЧТ'):
            self.thursday = timework
        elif(day=='ПТ'):
            self.friday = timework
        elif(day=='СБ'):
            self.saturday = timework
        elif(day=='ВС'):
            self.sunday = timework

    def  GetIntervals(self):
        intervals = str(self.timework).split(', ')
        keys = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        for interval in intervals:
            days = interval.split(' ')[0].upper()
            time = interval.split(' ')[1]
            starttime, endtime = time.split('-')
            hours = int(endtime.split(':')[0])-int(starttime.split(':')[0])
            minutes = int(endtime.split(':')[1]) - int(starttime.split(':')[1])
            count = int(hours*2+minutes/30)

            if(len(days.split('-'))==1):
                self.set_day(days, time + " " + str(count))
            else:
                startday, endday = days.split('-')
                s = e = 1
                for i in range(7):
                    if(keys[i]==startday):
                        s = i
                    elif(keys[i]==endday):
                        e = i
                        break
                for k in range(s,e+1):
                    self.set_day(keys[k],time + " " + str(count))

    def __str__(self):
        return str(self.restaurant.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.GetIntervals()
        super().save(*args, **kwargs)


class Table(models.Model):
    count = models.IntegerField(default='4')
    smoke = models.BooleanField()
    window = models.BooleanField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant.name+' ' +str(self.count)

class TimeTable(models.Model):
    time = models.DateTimeField()
    reservation = models.BooleanField(default=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, default = '')
    
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