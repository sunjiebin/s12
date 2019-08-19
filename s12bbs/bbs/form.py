#!/usr/bin/env python3
# Auther: sunjb

from django import forms
from bbs import models

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model=models.Article    #生成Article表的html表单
        exclude=['author','priority']      #不显示指定列，[]代表显示所有列
        labels={        #列别名
            'category':'文章分类',
            'author':'作者',
        }
        error_messages={
            'head_img':{'required':'必须上传图片'},
            # '__all__':{'自定义整体错误信息'},
            
        }

    def __init__(self,*args,**kwargs):
        super(ArticleModelForm,self).__init__(*args,**kwargs)
        for filed_name in self.base_fields:
            filed = self.base_fields[filed_name]