from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from catalog.models import Restaurant,Like, Table
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf

@csrf_exempt
def post(request):
    if request.POST:
        if request.POST.get('id'):
            rest = Restaurant.objects.get(id = request.POST.get('id'))
            if request.POST.get('window') == 'true':
                window = True
            else:
                window = False
            if request.POST.get('smoke') == 'true':
                smoke = True
            else:
                smoke = False
            print(smoke)
            tables = Table.objects.filter(restaurant = rest)
            goodtable = []
            for tb in tables:
                if tb.window == window and tb.smoke == smoke:
                    goodtable.append(tb)
            return render_to_response('catalog/order.html', {'tables':goodtable})
        cat = request.POST.get('cat','')
    else:
        cat = request.GET.get('cat')
    object_list = Restaurant.objects.all()
    if cat:
        object_list = object_list.filter(category = cat)
    object_list = object_list.order_by("-mark")
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    likes = Like.objects.filter(user = request.user.id)

    args = {'list':queryset, 'likes':likes}
    args['cat'] = cat
    args['csrf_token'] = csrf.get_token(request)
    args['categories'] = Restaurant.categories
    if request.POST:
        return render(request,'catalog/newposts.html', args)
    return render(request,'catalog/posts.html', args)