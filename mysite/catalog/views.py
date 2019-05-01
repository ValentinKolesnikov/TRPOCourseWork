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
        if request.POST.get('text'):
            dateorder = request.POST.get('date')
            dayorder, monthorder, yearorder = dateorder.split('.')
            tableorder = request.POST.get('table')
            timeorder = request.POST.get('time')
            hourorder, minuteorder = timeorder.split(':')
            textorder = request.POST.get('text')
            restaurantorder = request.POST.get('restaurant')

            order = TimeTable(
            time = datetime(int(yearorder),int(monthorder),int(dayorder),int(hourorder),int(minuteorder),0), 
            table = Table.objects.get(id = int(tableorder)), 
            text = textorder, user = request.user, restaurant = Restaurant.objects.get(id = int(restaurantorder)))
            order.save()
            return render_to_response('catalog/order.html', {})
            
        
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
                tw,count = wt.split(' ')
                if(tw=='Выходной'):
                    return render_to_response('catalog/order.html', {'times': tw})
                list_time = []
                shour, sminute = (wt.split(' ')[0].split('-'))[0].split(':')
                shour = int(shour)
                sminute = int(sminute)
                booktables = TimeTable.objects.filter(table = table)
                newbooktable = []
                for x in booktables:
                    if x.time.day == int(day) and x.time.month == int(month) and x.time.year == int(years):
                        newbooktable.append(str(x.time.hour+3)+':'+str('00' if x.time.minute==0 else '30'))


                for x in range(int(count)-1):
                    hour = int(x/2) + shour
                    minute = (x%2)*30+sminute
                    if minute == 60:
                        hour+=1
                        minute = 0
                    if minute ==0:
                        minute = '00'
                    list_time.append(str(hour)+':'+str(minute))
                return render_to_response('catalog/order.html', {'times': list_time,'booktables':newbooktable})

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
