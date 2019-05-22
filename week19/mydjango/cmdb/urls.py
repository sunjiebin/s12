#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
from django.contrib import admin
from django.urls import path
from cmdb import views
from django.urls import re_path,path

urlpatterns = [
    path('login/', views.login),
    path('userinfo',views.userinfo),
    re_path('userdetail-(?P<id>\d+).html',views.userdetail,name='detail'),
    # path('index', views.index),
    # path('register', views.register),
    # path('upload', views.upload),
    # # 这里的Home是我们定义的函数名,as_view()是固定的方法
    # path('home/', views.Home.as_view()),
    # path('dict/', views.dict),
    # # 注意在2.2.1版本的django中,要导入re_path,然后用re_path才能使得正则生效,用path正则是不生效的.这个和老版本的有区别
    # re_path('detail-(\d+).html', views.detail),
    # # 可以同时传递多个参数，通过?P<nid>将正则匹配到的值与nid匹配，形成一个字典{'nid':数字1,'uid':'数字2'}，这样在detail2中，就不用担心接受的形参的位置了
    # # 在detail中，只需要取key值nid就能够得到第一个实参，取uid就得到第二个实参
    # re_path('detail-(?P<nid>\d+)-(?P<uid>\d+).html', views.detail2),
    # re_path('reverse$', views.url1, name='u1'),
    # re_path('reverse/(\d+)/(\d+)', views.url1, name='u2'),
    # re_path('reverse3/(?P<num1>\d+)/(?P<num2>\d+)', views.url1, name='u3'),
    # re_path('urlmatch$', views.url2, name='i1'),
    # re_path('urlmatch/(\d+)/(\d+)', views.url2, name='i2'),
    # re_path('urlmatch3/(?P<num1>\d+)/(?P<num2>\d+)', views.url2, name='i3'),
]