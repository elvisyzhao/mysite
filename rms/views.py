# coding: UTF-8

from django.shortcuts import render
from .models import Restaurant, Dish, OrderEntry, Order
from django.views.decorators.csrf import csrf_protect
import re
import logging
from django.http import HttpResponse, HttpResponseNotFound
import datetime
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)

# Create your views here.
@csrf_protect
def menu(request, rid):
    restaurant = get_object_or_404(Restaurant, pk=rid)
    #restaurant = Restaurant.objects.get(id=rid)
    dish_types = restaurant.dishtype_set.all()
    dic = {}
    dic['types'] = {}
    dic['dishes'] = {}
    for dish_type in dish_types:
        dic['types'][dish_type.id] = dish_type.name 
        dic['dishes'][dish_type.id] = list(dish_type.dish_set.all())
    return render(request, 'menu_template.html', dic)

@csrf_protect
def pre_order(request):
    totalPrice = 0
    request.session['order'] = request.POST
    dic = {}
    dic['min_date'] = datetime.datetime.now().strftime("%m/%d/%Y %H:%M")
    dic['max_date'] = (datetime.datetime.now()+datetime.timedelta(days=7)).strftime("%m/%d/%Y")
    logger.error("user's phone is : " + request.user.myuser.phone)
    return render(request, 'pre_order_template.html', dic)

@csrf_protect
@login_required
def order(request):
    appointment_time = request.POST['appointment_time'].encode('utf-8')
    logger.error(type(appointment_time))
    reg = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2}) ([\x80-\xff]+)(\d{1,2})点(\d{1,2})分')
    reMatch = reg.match(appointment_time)
    time = None
    if (reMatch.lastindex == 6):
        pStr = reMatch.group(4)
        yearStr = reMatch.group(1)
        monthStr = reMatch.group(2)
        dayStr = reMatch.group(3)
        hourStr = reMatch.group(5)
        minuteStr = reMatch.group(6)
        if pStr == '凌晨':
            if hourStr == '12':
                hourStr = '0'
        elif pStr == '早上':
            pass
        elif pStr == '上午':
            pass
        elif pStr == '中午':
            if hourStr == '12' and int(minuteStr) != 0:
                hourStr = str(int(hourStr)+12)
        elif pStr == '下午':
            hourStr = str(int(hourStr)+12)
        elif pStr == '晚上':
            hourStr = str(int(hourStr)+12)
        else:
            pass
        time_str = "%s-%s-%s %s:%s" % (yearStr, monthStr, dayStr, hourStr, minuteStr)
        time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M');
        phone = request.POST['phone']
        order = Order.objects.create(appointment_time=time, phone=phone, customer=request.user.myuser)
        totalPrice = 0
        for key, value in request.session['order'].items():
            pid = key
            try:
                count = int(value)
                dish = Dish.objects.get(id=pid)
                price = dish.price
                totalPrice += price * count
                entry = OrderEntry.objects.create(dish=dish, order=order, count=count)
            except:
                pass
        order.customer = request.user.myuser
        logger.error('----------' + request.user.username)
        logger.error('----------' + request.user.myuser.phone)
        order.save()
        return redirect(show_order, order.id)
    else:
        logger.error('time string error')        
    return HttpResponse(datetime.datetime.strftime(time, "%Y-%m-%d %H:%M"))

@login_required
def show_order(request, oid):
    order = Order.objects.get(pk=oid)
    items = list(order.orderentry_set.all())
    totalPrice = 0
    for item in items:
        totalPrice += item.dish.price * item.count
    dic = {}
    dic['items'] = items
    dic['appointment_time'] = order.appointment_time
    dic['total_price'] = totalPrice
    return render(request, 'show_order.html', dic)

@login_required
def order_list(request):
    order_list = list(request.user.myuser.order_set.all())
    return render(request, 'order_list.html', {'order_list':order_list})

@csrf_protect
def get_code(request):
    logger.error(request.POST.get('phone', None))
    return HttpResponse('successful')

def handler404(request, exception, template_name='404.html'):
    return HttResponse('404')

def handler500(request, template_name='500.html'):
    return HttpResponse('服务器发生了一些问题')
