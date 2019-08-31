#!/usr/bin/env python3
# Auther: sunjb

from django.contrib import admin
from django.urls import path,re_path
from webchat import views
urlpatterns = [
    path('',views.dashboard,name='chat_dashboard'),
    path('msg_send/',views.send_msg,name='send_msg'),
    path('get_new_msg/',views.get_new_msg,name='get_new_msg'),
]
