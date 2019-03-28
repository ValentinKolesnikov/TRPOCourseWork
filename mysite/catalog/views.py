from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from catalog.models import Restaurant,Like
from django.contrib import auth
import time

def post(request):
    t = time.time()
    object_list = Restaurant.objects.all().order_by("-mark")
    print(time.time()-t)
    paginator = Paginator(object_list, 4)

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    likes = Like.objects.filter(user = request.user.id)
    args = {'list':queryset, 'likes':likes}
    return render(request,'catalog/posts.html', args)