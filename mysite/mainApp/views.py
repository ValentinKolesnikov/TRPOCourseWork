from catalog.models import Restaurant
from django.shortcuts import render
from django.contrib import auth

def index(request):
    args = {}
    object_list = Restaurant.objects.all()
    count = object_list.count
    args['count'] = count

    return render(request,'mainApp/homePage.html',args)
