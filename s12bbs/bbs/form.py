#!/usr/bin/env python3
# Auther: sunjb

from django import forms
from bbs import models

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model=models.Article    #生成Article表的html表单
        exclude=[]      #显示所有列
        labels={        #列别名
            'category':'文章分类',
            'author':'作者',
        }

