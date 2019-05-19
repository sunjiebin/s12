"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from django.urls import re_path,path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.login),
    path('index',views.index),
    path('register',views.register),
    path('upload',views.upload),
    # 这里的Home是我们定义的函数名,as_view()是固定的方法
    path('home/',views.Home.as_view()),
    path('dict/',views.dict),
    # 注意在2.2.1版本的django中,要导入re_path,然后用re_path才能使得正则生效,用path正则是不生效的.这个和老版本的有区别
    re_path('detail-(\d+).html',views.detail),
]
