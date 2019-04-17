from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from catalog.models import Restaurant,Like
from django.contrib import auth
from django.middleware import csrf

def post(request):
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
    return render(request,'catalog/posts.html', args)