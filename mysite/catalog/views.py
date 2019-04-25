from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from catalog.models import Restaurant,Like, Table, TimeTable, Week
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from datetime import datetime

@csrf_exempt
def post(request):
    if request.POST:
        if request.POST.get('id') or request.POST.get('idtable'):
            if request.POST.get('window'):
                rest = Restaurant.objects.get(id = request.POST.get('id'))
                if request.POST.get('window') == 'true':
                    window = True
                else:
                    window = False
                if request.POST.get('smoke') == 'true':
                    smoke = True
                else:
                    smoke = False
                tables = Table.objects.filter(restaurant = rest)
                goodtable = []
                for tb in tables:
                    if tb.window == window and tb.smoke == smoke:
                        goodtable.append(tb)
                return render_to_response('catalog/order.html', {'tables':goodtable})
            elif request.POST.get('time'):
                day, month, years = request.POST.get('date').split('.')
                date = datetime(int(years), int(month),int(day))
                wkday = date.weekday
                table = Table.objects.get(id = request.POST.get('idtable'))
                rest = Restaurant.objects.get(id = request.POST.get('id'))
                wk = Week.objects.get(restaurant = rest)
                return render_to_response('catalog/order.html', {})
            else:
                table = Table.objects.get(id = request.POST.get('idtable'))
                day, month, years = request.POST.get('date').split('.')
                times = TimeTable.objects.filter(table = table)
                date = datetime(int(years), int(month),int(day))
                wkday = date.weekday()
                wk = Week.objects.get(restaurant = table.restaurant)

                if wkday == 0:
                    wt = wk.monday
                elif wkday==1:
                    wt = wk.tuesday
                elif wkday==2:
                    wt = wk.wednesday
                elif wkday==3:
                    wt = wk.thursday
                elif wkday ==4:
                    wt = wk.friday
                elif wkday==5:
                    wt = wk.saturday
                else:
                    wt = wk.sunday
                count = wt.split(' ')[1]
                return render_to_response('catalog/order.html', {'times': range(int(count))})

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