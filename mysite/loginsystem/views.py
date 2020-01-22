from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from user.models import Client
from django.middleware import csrf


def login(request):
    args = {}
    args['csrf_token'] = csrf.get_token(request)
    if request.POST:
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect(request.META['HTTP_REFERER'])
        else:
            args['login_error'] = 'Попробуйте еще'
            return render(request, 'loginsystem/login.html', args)
    else:
        return render(request,'loginsystem/login.html', args)

def register(request):
    args = {}
    args['csrf_token'] = csrf.get_token(request)
    args['form'] = RegisterForm()
    if request.POST:
        newuser_form = RegisterForm(request.POST)
        client = Client()
        if newuser_form.is_valid():
            newuser_form.save()
            user = User.objects.get(username = request.POST.get('username',''))
            client.user = user
            client.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password = newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render(request,'loginsystem/register.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/')
