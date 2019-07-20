from django.shortcuts import render
from app01 import models
# Create your views here.

def article(request,**kwargs):
    print(kwargs)
    dic={}
    '''当v为0时，相当于数据库里面id=0，实际上时不存在的，我们定义为代表查询全部数据，所以当v=0，我们就不设置该查询条件。在filter查询时
    就会把所有匹配的数据查出来'''
    for k,v in kwargs.items():
        #注意从urls.py里面拿过来的kwargs字典里面的值是字符串，即v是字符串不是数字。而从数据库里面拿到的是数字。category.id是数字。
        #默认v是字符串，我们将他转化为数字，这样在html模板中就能够和category取到的id相比较了。否则一个字符串一个数字没法相等
        kwargs[k]=int(v)
        if v != '0':
            dic[k]=v
    print(dic)
    #category是从表里面查询出所有的数据，返回的是queryset类型的数据
    category=models.Category.objects.all()
    #articletype是从Article类里面取的数据，type_choice是放在内存里面的，并没有在数据库里面存放。返回的是元组。
    articletype=models.Article.type_choice
    result=models.Article.objects.filter(**dic)
    return render(request,'article_template.html',{'result':result,'category':category,'articletype':articletype,'kwargs':kwargs})