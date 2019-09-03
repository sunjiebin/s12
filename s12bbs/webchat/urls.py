#!/usr/bin/env python3
# Auther: sunjb

from django.contrib import admin
from django.urls import path,re_path
from webchat import views
urlpatterns = [
    path('',views.dashboard,name='chat_dashboard'),
    path('msg_send/',views.send_msg,name='send_msg'),
    path('get_new_msg/',views.get_new_msg,name='get_new_msg'),
    path('file_upload',views.file_upload,name='file_upload_webchat'),
#    path('file_upload_progress',views.file_upload_progress,name='file_upload_progress'),
#    path('delete_cache_key',views.delete_cache_key,name='delete_cache_key'),
#    path('upload_page/', views.UploadPage.as_view()),
#    path('upload/', views.Upload.as_view()),
]
