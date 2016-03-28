#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.
def index(request):
    return HttpResponse("Hello,World!")
    # raise Http404(u'当前页面不存在!')