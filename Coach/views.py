# coding:utf-8
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404, JsonResponse
from .models import Coach
from datetime import time
import json
from .models import Coach, Order, Student


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
        print account,password
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

def order(request):
    if request.session.get('id',None):
        return JsonResponse({'ok':True})
    else:
        return JsonResponse({'ok':False,'message':u'您还未登录!'})

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
