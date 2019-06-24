#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from django.contrib import admin
from django.urls import path,include
from host import views

urlpatterns = [
    path('hostlist',views.hostlist),
    # path('grouplist',views.grouplist),
    # path('addhost',views.addhost),
    # path('delhost',views.delhost),
]
