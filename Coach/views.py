# coding:utf-8
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404, JsonResponse
import json
from .models import Coach, Order, Student, Time
from datetime import timedelta, datetime
from publicFunc import get_all_interval


# Create your views here.
def index(request, status):
    if status == 'dev':
        # 开发环境
        data = {'baseUrl': 'http://127.0.0.1:8000/Coach/'}
        return render(request, 'Coach/index.html', data)
    elif status == 'pro':
        # 生产环境
        data = {'baseUrl': 'htt://121.42.181.79/Coach/'}
        return render(request, 'Coach/index.html', data)
    else:
        raise Http404


def login(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        account = body['account']
        password = body['password']
        print account, password
        student = Student.objects.filter(account=account)
        if student:
            if password == student[0].password:
                request.session['id'] = student[0].id
                return JsonResponse({'ok': True})
            else:
                return JsonResponse({'ok': False, 'message': u'密码不正确!'})
        else:
            return JsonResponse({'ok': False, 'massage': u'帐号不存在!'})
    else:
        raise Http404


def get_order(request):
    c = Coach.objects.filter(account='123')[0]
    t = Time.objects.filter(coach=c)[1]
    all_interval = get_all_interval(t.begin_time, t.end_time)
    enable_order_times = all_interval / (t.step * 60)  # 可预约次数
    begin = str(t.begin_time).split(':')
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    begin_hour = int(begin[0])
    begin_minute = int(begin[1])
    begin_second = int(begin[2])
    real_begin = datetime(year, month, day, begin_hour, begin_second, begin_minute)
    data = {'timeList': [t.begin_time], 'coach': c.name}
    for i in range(enable_order_times):
        data['timeList'].append(str(real_begin + (timedelta(minutes=t.step) * (i + 1))).split(' ')[1])
    return JsonResponse(data)


def add_order(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
        post_time = post_data['time']
        coach = Coach.objects.filter(name=post_data['coach'])[0]
        student = Student.objects.get(pk=request.session['id'])
        order_time = post_time.split(':')
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        hour = int(order_time[0])
        minute = int(order_time[1])
        second = int(order_time[2])
        order_time = datetime(year, month, day, hour, minute, second)
        order = Order(coach=coach, student=student, order_time=order_time)
        order.save()
        return JsonResponse({'ok': True})
    else:
        return HttpResponse('add')


def history(request, date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = date[2]
    if int(month) not in range(1, 13) or int(day) not in range(1, 32):
        raise Http404
    date_record = Order.objects.filter(order_time__year=year, order_time__month=month, order_time__day=day)
    if date_record:
        print date_record
        return HttpResponse('yes')
    else:
        return HttpResponse('no')


def test(request, status):
    if status == 'dev':
        return HttpResponse('dev')
    elif status == 'pro':
        return HttpResponse('pro')
    else:
        raise Http404

# def json(request, status):
#     data = {'ok': True}
#     if status == 'dev':
#         if request.session.get('me', None):
#             return JsonResponse(data)
#         else:
#             data['ok'] = False
#             return JsonResponse(data)
#     elif status == 'pro':
#         return HttpResponse('pro')
#     else:
#         raise Http404
