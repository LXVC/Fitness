from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Coach, Time, Student, Order
from datetime import datetime, timedelta


class OrderAdmin(admin.ModelAdmin):
    list_display = ['student', 'order_time', 'accept']
    list_filter = ('order_time',)
    date_hierarchy = 'order_time'
    ordering = ['-order_time']
    

admin.site.register(Coach)
admin.site.register(Time)
admin.site.register(Student)
admin.site.register(Order, OrderAdmin)
