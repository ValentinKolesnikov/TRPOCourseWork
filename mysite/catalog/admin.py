from django.contrib import admin
from catalog.models import Restaurant, Table, Comment,Like

admin.site.register(Restaurant)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Table)



# Register your models here.
