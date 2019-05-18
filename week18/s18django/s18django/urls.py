"""s18django URL Configuration

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
from cmdb import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cmdb/', views.cmdb),
    # 注意这里的login/要和views.login里面定义的一样,这里有/那里也要有,这里没有,那里也就不要写,否则会出错
    path('login',views.login),
    path('home/',views.home),
]
