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
from django.urls import re_path,path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 注意要加上/，不然访问app01路径下的url就变成了app01upload，用app01/upload就匹配不到了。实际上就是把两个urls里面的路径拼接起来了
    # 当一个项目下面多个模块，URL会有很多时，就可以用include来对url分流存放。
    path('app/',include('app01.urls')),
    path('cmdb/',include('cmdb.urls')),
    path('orm/',views.orm),
]
