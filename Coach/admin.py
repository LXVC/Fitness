from django.contrib import admin

# Register your models here.
from .models import Coach,Time,Student,Order

admin.site.register(Coach)
admin.site.register(Time)
admin.site.register(Student)
admin.site.register(Order)
