from django.shortcuts import render
from django.contrib import auth

def index(request):
    return render(request,'mainApp/homePage.html')

def contact(request):
    return render(request,'mainApp/basic.html', {'values':['Вопросы - звоните','375296497315']})