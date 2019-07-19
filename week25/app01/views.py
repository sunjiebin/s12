from django.shortcuts import render
from app01 import models
# Create your views here.

def article(request,**kwargs):
    print(kwargs)
    dic={}
    '''当v为0时，相当于数据库里面id=0，实际上时不存在的，我们定义为代表查询全部数据，所以当v=0，我们就不设置该查询条件。在filter查询时
    就会把所有匹配的数据查出来'''
    for k,v in kwargs.items():
        #默认v是字符串，我们将他转化为数字，这样在html模板中就能够和category取到的id相比较了。否则一个字符串一个数字没法相等
        kwargs[k]=int(v)
        if v != '0':
            dic[k]=v
    print(dic)
    category=models.Category.objects.all()
    articletype=models.ArticleType.objects.all()
    result=models.Article.objects.filter(**dic)
    return render(request,'article.html',{'result':result,'category':category,'articletype':articletype,'kwargs':kwargs})