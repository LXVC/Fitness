from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^([a-z]+)/$', views.index, name='index'),
    url(r'^api/login/$', views.login, name='login'),
    url(r'^api/order/$',views.order,name='order'),
    url(r'^history/(\d{4}-\d{1,2}-\d{1,2})',views.history,name='history')
]
