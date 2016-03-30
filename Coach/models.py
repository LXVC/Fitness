# coding:utf-8
from __future__ import unicode_literals

from django.db.models import Model
from django.db.models import TimeField, BooleanField, IntegerField, CharField, ForeignKey, DateField, DateTimeField
from .myException import EndBeforeBeginError, StepTooLongError
from django.utils import timezone
from datetime import time


# Create your models here.
class Coach(Model):
    account = CharField(max_length=20,unique=True)
    password = CharField(max_length=20)
    name = CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'教练'
        verbose_name_plural = u'教练'


class Time(Model):
    coach = ForeignKey(Coach)
    begin_time = TimeField(u'开始时间')
    end_time = TimeField(u'结束时间')
    step = IntegerField(u'时间间隔')
    ceate_date = DateField(u'创建时间')

    def __unicode__(self):
        return str(self.begin_time) + '-' + str(self.end_time)

    def save(self, *args, **kwargs):
        hour_interval = (self.end_time.hour - self.begin_time.hour) * 60 * 60
        minute_interval = (self.end_time.minute - self.begin_time.minute) * 60
        second_interval = self.end_time.second - self.begin_time.second
        all_interval = hour_interval + minute_interval + second_interval
        if all_interval <= 0:
            raise EndBeforeBeginError(all_interval)
        elif self.step * 60 > all_interval:
            raise StepTooLongError(all_interval, self.step)
        else:
            super(Time, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'日程'
        verbose_name_plural = u'日程管理'


class Student(Model):
    account = CharField(max_length=20,unique=True)
    password = CharField(max_length=20)
    name = CharField(max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'学员'
        verbose_name_plural = u'学员'


class Order(Model):
    coach = ForeignKey(Coach, verbose_name='教练')
    student = ForeignKey(Student, verbose_name='学员')
    order_time = DateTimeField(u'预约时间')
    accept = BooleanField(u'接受预约', default=False)

    def __unicode__(self):
        return self.student.name + u'预约了' + self.coach.name + u'在' + str(self.order_time.month) \
               + u'月' + str(self.order_time.day) + u'号' + str(self.order_time.hour) + u'点'+\
                str(self.order_time.minute)+'分'

    class Meta:
        verbose_name = u'预约'
        verbose_name_plural = u'预约管理'
