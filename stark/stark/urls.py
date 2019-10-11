"""stark URL Configuration

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
from django.urls import path,include
from rest_framework import routers
from stark.rest_views import AssetViewSet
from stark.rest_views import ManufactoryViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('asset', AssetViewSet)  #这里的asset和url里面写的api/相结合,组成api/asset
router.register('Manufactory', ManufactoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('salt/',include('Arya.urls')),
    path('asset/',include('Sansa.urls')),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),   #api认证
    path('api/', include(router.urls)),  #只要是api开头的,都映射到这里面,当访问api/asset时,就会跳到AssetViewSet
]


