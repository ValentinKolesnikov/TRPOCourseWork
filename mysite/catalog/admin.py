from django.contrib import admin
from catalog.models import Restaurant, Table, Comment,Like, TimeTable, Week

admin.site.register(Restaurant)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Table)
admin.site.register(TimeTable)
admin.site.register(Week)



# Register your models here.
