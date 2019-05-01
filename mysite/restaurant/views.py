from django.shortcuts import render,redirect, render_to_response
from django.db.models import Max
from catalog.models import Restaurant, Comment, Like, Table, TimeTable, Week
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
import os, os.path
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EditorRestaurant, AddTable
from mysite.settings import BASE_DIR

import cgi

@csrf_exempt
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
        args['tables'] = Table.objects.filter(restaurant = args['rest'])
        if request.POST:
            if(request.POST.get('text','')):
                text = request.POST.get('text','')
                if len(text)>3 and request.user.is_authenticated:
                    com = Comment(text = text, author = request.user.id, restaurant = Restaurant.objects.get(id = id))
                    com.save()
            else:
                idtable = request.POST.get('id','')
                times = TimeTable.objects.filter(table = args['tables'][int(idtable)])
                args['times'] = times
                return render_to_response('restaurant/time.html',args)
                
        comments = Comment.objects.filter(restaurant=id)
        for x in comments:
            x.name = User.objects.get(id=x.author).username
        args['object_list'] = comments
        args['rest'] = Restaurant.objects.get(id=id)
        args['owner'] = User.objects.get(id=args['rest'].owner).username
        args['likes'] = Like.objects.filter(user = request.user.id)
        wk = Week.objects.get(restaurant = args['rest'])
        wek = []
        wek.append(str(wk.monday).split(' '))
        wek.append(str(wk.tuesday).split(' '))
        wek.append(str(wk.wednesday).split(' '))
        wek.append(str(wk.thursday).split(' '))
        wek.append(str(wk.friday).split(' '))
        wek.append(str(wk.saturday).split(' '))
        wek.append(str(wk.sunday).split(' '))
        args['week'] = wek

        return render(request,'restaurant/restaurant.html',args)
        
def create(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    args = {}
    form = EditorRestaurant()
    args['form'] = form
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
        rest = Restaurant.objects.latest('id')
        photo.name = str(rest.id)+'.jpg'
        rest.photo = photo
        rest.save()
        return redirect('/user/'+str(owner))
    return render(request, 'restaurant/create.html', args)


def editortables(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    rest = Restaurant.objects.filter(owner = request.user.id)[0]
    args = {}
    args['csrf_token'] = csrf.get_token(request)
    args['tables'] = Table.objects.filter(restaurant = rest)
    form = AddTable(initial={'count':4, 'counttables':1})
    args['form'] = form
    if request.POST:
        if request.POST.get('id'):
            id = int(request.POST.get('id'))
            if rest == Table.objects.get(id = id).restaurant:
                Table.objects.get(id = id).delete()
            return render_to_response('restaurant/editortables.html',args)

            
        count = int(request.POST.get('count'))
        smoke = True if request.POST.get('smoke')=='true' else False
        window = True if request.POST.get('window')=='true' else False
        counttable = int(request.POST.get('counttables'))
        for x in range(counttable):
            table = Table(count = count, smoke = smoke, window = window, restaurant = rest)
            table.save()
        return render_to_response('restaurant/editortables.html',args)
        
        

    return render(request,'restaurant/editortables.html', args)

    


def editor(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    rest = Restaurant.objects.filter(owner = request.user.id)[0]
    args = {}
    args['csrf_token'] = csrf.get_token(request)
    form = EditorRestaurant(initial={'name': rest.name,'description':rest.description,'worktime':rest.worktime, 'category':rest.category, 'phone':rest.phone, 'photo':rest.photo})
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
            rest.worktime = post.get('worktime','')
            rest.phone = post.get('phone','')
            rest.category = post.get('category','')
            rest.save()
            return redirect('/restaurant/'+str(rest.id))
        else:
            args['form'] = newuser_form
    return render(request,'restaurant/editor.html', args)



def CheckLike(likes, restaurant):
    for like in likes:
        if restaurant == str(like.restaurant.id):
            return True
    return False

@csrf_exempt
def like(request):
    try:
        request.META['HTTP_REFERER']
    except:
        return redirect('/')
    if not request.user.is_authenticated:
        return redirect(request.META['HTTP_REFERER'])
    else:
        id = request.POST.get('id')
        likes = Like.objects.filter(user = request.user.id)
        if  CheckLike(likes, id):
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


#var formData = new FormData(document.forms.postcomment);
# var xhr = new XMLHttpRequest();
# xhr.open("POST", "http://127.0.0.1:8000/restaurant/1");
# xhr.send(formData);