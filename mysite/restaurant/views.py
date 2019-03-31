from django.shortcuts import render,redirect, render_to_response
from django.db.models import Max
from catalog.models import Restaurant, Comment, Like
from django.contrib.auth.models import User
from django.middleware import csrf
import os, os.path
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EditorRestaurant
from mysite.settings import BASE_DIR

def restaurant(request, id=None):
    if not id:
        return render(request,'restaurant/restaurant.html',{'error':True})
    else:
        args={}
        try:
            args['rest'] = Restaurant.objects.get(id=id)
        except:
            return render(request,'restaurant/restaurant.html',{'error':True})
        args['csrf_token'] = csrf.get_token(request)
        if request.POST:
            text = request.POST.get('text','')
            if len(text)>3 and request.user.is_authenticated:
                com = Comment(text = text, author = request.user.id, restaurant = Restaurant.objects.get(id = id))
                com.save()
        comments = Comment.objects.filter(restaurant=id)
        for x in comments:
            x.name = User.objects.get(id=x.author).username
        args['object_list'] = comments
        args['rest'] = Restaurant.objects.get(id=id)
        args['owner'] = User.objects.get(id=args['rest'].owner).username
        args['likes'] = Like.objects.filter(user = request.user.id)
        return render(request,'restaurant/restaurant.html',args)

def like(request, id= None):
    try:
        request.META['HTTP_REFERER']
    except:
        return redirect('/')
    if not id or not request.user.is_authenticated:
        return redirect(request.META['HTTP_REFERER'])
    else:
        likes = Like.objects.filter(user = request.user.id)
        if  CheckLike(likes,id):
            r = Restaurant.objects.get(id = id)
            r.mark-=1
            r.save()
            like = Like.objects.filter(user = request.user.id, restaurant = Restaurant.objects.get(id = id))
            like.delete()
        else:
            r = Restaurant.objects.get(id = id)
            r.mark+=1
            r.save()
            like = Like(user = request.user, restaurant = Restaurant.objects.get(id = id))
            like.save()
        return redirect(request.META['HTTP_REFERER'])
        
def create(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    args = {}
    args['csrf_token'] = csrf.get_token(request)
    if request.POST:
        name = request.POST.get('name','')
        owner = request.user.id
        description = request.POST.get('description','')
        phone = request.POST.get('phone','')
        worktime = request.POST.get('worktime','')
        photo = request.FILES['photo']
        restaurant = Restaurant(name = name, owner = owner, description= description, phone = phone, worktime = worktime)
        restaurant.save()
        rest = Restaurant.objects.latest('if')
        photo.name = str(rest.id)+'.jpg'
        rest.photo = photo
        rest.save()
        return redirect('/user/'+str(owner))
    return render_to_response('restaurant/create.html', args)

def editor(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    rest = Restaurant.objects.filter(owner = request.user.id)[0]
    args = {}
    args['csrf_token'] = csrf.get_token(request)

    form = EditorRestaurant(initial={'name': rest.name,'description':rest.description,'phone':rest.phone, 'photo':rest.photo})

    args['form'] = form

    if request.POST:
        newuser_form = EditorRestaurant(request.POST)
        if (len(request.POST.get('phone',''))==12):
            post = request.POST
            if request.FILES:
                photo = request.FILES['photo']
                photo.name = str(rest.id)+'.jpg'
                if os.path.exists(BASE_DIR+'\\mysite\\media\\restaurant_image\\'+str(rest.id)+'.jpg'):
                    os.remove(BASE_DIR+'\\mysite\\media\\restaurant_image\\'+str(rest.id)+'.jpg')
                rest.photo = photo
            rest.name = post.get('name','')
            rest.description = post.get('description','')
            rest.phone = post.get('phone','')
            rest.save()
            return redirect('/restaurant/'+str(rest.id))
        else:
            args['form'] = newuser_form
    return render(request,'restaurant/editor.html', args)



def CheckLike(likes, restaurant):
    for like in likes:
        if restaurant == like.restaurant.id:
            return True
    return False