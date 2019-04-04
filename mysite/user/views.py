from django.shortcuts import render, redirect
from django.contrib import auth
from catalog.models import Restaurant
from django.contrib.auth.models import User
from .models import Client
from django.middleware import csrf
import os
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EditorUser
from .models import Client
from mysite.settings import BASE_DIR


def user(request, id=None):
    args = {}
    args['id'] = auth.get_user(request).id
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
                args = {'userprofile':user, 'rest': rest}
                args['client'] = Client.objects.get(user = user)
                return render(request,'user/user.html',args)
            except:
                args = {'error':True}
                return render(request,'user/user.html',args)
        else:
            return render(request,'user/user.html',args)
    else:
        return render(request,'user/user.html',args)

def editor(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    user = request.user
    args = {}
    args['csrf_token'] = csrf.get_token(request)
    client = Client.objects.get(user = request.user)
    form = EditorUser(initial={'first_name': user.first_name, 'last_name': user.last_name, 'phone': client.phone, 'photo': client.photo})

    args['form'] = form

    if request.POST:
        post = request.POST
        if request.FILES:
            photo = request.FILES['photo']
            photo.name = str(user.id)+'.jpg'
            if os.path.exists(BASE_DIR+'\\mysite\\media\\user_image\\'+str(user.id)+'.jpg'):
                os.remove(BASE_DIR+'\\mysite\\media\\user_image\\'+str(user.id)+'.jpg')
            client.photo = photo
        user.first_name = post.get('first_name','')
        user.last_name = post.get('last_name','')
        client.phone = post.get('phone','')
        client.save()
        user.save()
        return redirect('/user/'+str(user.id))
    return render(request,'user/editor.html', args)