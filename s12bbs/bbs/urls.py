#!/usr/bin/env python3
# Auther: sunjb

from django.contrib import admin
from django.urls import path,re_path
from bbs import views
urlpatterns = [
    path('',views.index),
    re_path('category/(?P<id>\d+)',views.category),
    re_path('detail/(\d+)', views.article_detail, name='article_detail'),
    path('comment/',views.comment,name='post_comment'),
    re_path('get_comments/(\d+)',views.get_comments,name='get_comments'),
    path('new_article/',views.new_article,name='new_article'),
    path('file_upload/',views.file_upload,name='file_upload'),
    path('latest_article_count/',views.get_latest_article_count,name='get_latest_article_count'),
]
