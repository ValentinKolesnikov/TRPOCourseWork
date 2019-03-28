from django.shortcuts import render
from django.contrib import auth
from catalog.models import Restaurant
from loginsystem.forms import RegisterForm
from django.contrib.auth.models import User


def user(request, id=None):
    args = {}
    args['id'] = auth.get_user(request).id
    args['form'] = RegisterForm()
    if args['id']:
        if id==0:
            id = -1
        if id:
            try:
                user = User.objects.get(id=id)
                rest = None
                try:
                    rest = Restaurant.objects.filter(owner = id)[0]
                except:
                    next
                args = {'userprofile':user, 'rest': rest,'form': RegisterForm()}
                return render(request,'user/user.html',args)
            except:
                args = {'error':True}
                return render(request,'user/user.html',args)
        else:
            return render(request,'user/user.html',args)
    else:
        return render(request,'user/user.html',args)