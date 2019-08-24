#!/usr/bin/env python3
# Auther: sunjb

from django import forms
from bbs import models

class ArticleModelForm(forms.ModelForm):
    class Meta:
        model=models.Article    #生成Article表的html表单
        exclude=['author','priority','pub_date']      #不显示指定列，[]代表显示所有列
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
        # 如果只需要给某个字段单独加样式，可以用下面的写法
        # self.fields['title'].widget.attrs['class']='form-control'
        print(self.base_fields)
        # 给所有字段统一加样式
        for filed_name in self.base_fields:
            filed = self.base_fields[filed_name]
            filed.widget.attrs.update({'class':'form-control'})
