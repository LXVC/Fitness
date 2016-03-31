# coding:utf-8
from django.shortcuts import render
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
        try:
            student = Student.objects.get(account=account)
        except Student.DoesNotExist:
            return JsonResponse({'ok': False, 'message': u'帐号不存在!'})
        if password == student.password:
            request.session['id'] = student.id
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False, 'message': u'密码不正确!'})
    else:
        raise Http404


def get_order(request):
    student_id = request.session.get('id', None)
    if student_id:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        coach = Coach.objects.get(account='123')  # 只有一个教练,故写死
        time_set = Time.objects.get(coach=coach)  # 教练的时间安排
        today_accept_order = Order.objects.filter(order_time__year=year, order_time__month=month, order_time__day=day,
                                                  accept=True, student_id=student_id)
        all_interval = get_all_interval(time_set.begin_time, time_set.end_time)
        enable_order_times = all_interval / (time_set.step * 60)  # 整个时间段内可预约次数
        begin = str(time_set.begin_time).split(':')
        begin_hour = int(begin[0])
        begin_minute = int(begin[1])
        begin_second = int(begin[2])
        real_begin = datetime(year, month, day, begin_hour, begin_minute, begin_second)
        data = {'timeList': [{'time': real_begin, 'isCoverByAccepted': False}], 'coach': coach.name, 'ok': True}
        for i in range(enable_order_times):
            item = dict()
            item['time'] = real_begin + timedelta(minutes=time_set.step) * (i + 1)
            item['isCoverByAccepted'] = False
            data['timeList'].append(item)
        for m in today_accept_order:  # 标记是否被预约时间覆盖 Oder.order_time -1 and +1
            for n in data['timeList']:
                if m.order_time - timedelta(hours=1) < n['time'] < m.order_time + timedelta(hours=1):
                    n['isCoverByAccepted'] = True
        data['timeList'] = [x for x in data['timeList'] if x['time'] > datetime.now()]  # 过滤掉请求时刻之前的order_time
        return JsonResponse(data)
    else:
        return JsonResponse({'ok': False, 'message': u'您还没有登录!'})


def add_order(request):
    student_id = request.session.get('id', None)
    if request.method == 'POST':
        if student_id:
            body = json.loads(request.body)
            post_time = body['time']
            coach = Coach.objects.get(name=body['coach'])
            student = Student.objects.get(pk=student_id)
            order_time = post_time.split(':')
            year = datetime.now().year
            month = datetime.now().month
            day = datetime.now().day
            hour = int(order_time[0][-2:])
            minute = int(order_time[1])
            second = int(order_time[2])
            order_time = datetime(year, month, day, hour, minute, second)
            try:
                Order.objects.get(coach=coach, student=student, order_time=order_time)
                return JsonResponse({'ok':False,'message':u'您已预约过这个时间'})
            except Order.DoesNotExist:
                order = Order(coach=coach, student=student, order_time=order_time)
                order.save()
                return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False, 'message': u'您还没有登录!'})
    else:
        raise Http404


def history(request, date):
    date = date.split('-')
    year = date[0]
    month = date[1]
    day = date[2]
    if int(month) not in range(1, 13) or int(day) not in range(1, 32):
        raise Http404
    date_record = Order.objects.filter(order_time__year=year, order_time__month=month, order_time__day=day)
    if date_record:
        print date_record           #输出该日的预约记录
        return HttpResponse('yes')
    else:
        return HttpResponse('no')


