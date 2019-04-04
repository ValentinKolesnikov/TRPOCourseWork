from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    
    class Meta():
        db_table = 'Client'
    photo = models.ImageField(upload_to='user_image', blank=True, default = None)
    phone = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)