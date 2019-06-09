from django.shortcuts import render,HttpResponse
from myapp import models
# Create your views here.

def bussiness(request):
    v1 = models.Bussiness.objects.all()
    # 返回QuerySet类型，里面包含了不同的的对象
    # [obj(id,caption,code),obj(id,caption,code)...]
    v2 = models.Bussiness.objects.all().values('id','caption')
    # 返回QuerySet类型，里面包含的是字典
    # [{'id':1,'caption':'运维'},{'id':2,'caption':'开发'},...]
    v3 = models.Bussiness.objects.all().values_list('id','caption')
    # 返回QuerySet类型，里面包含的是元组
    # [(1,运维),(2,开发),...]
    return render(request,'bussiness.html',{'obj':[v1,v2,v3,]})

def host(request):
    if request.method == 'GET':
        v1 = models.Host.objects.filter(nid__gt=0) #和all()结果一样
        print(v1[0].hostname)
        for row in v1:
            print(row.nid,row.hostname,row.b_id,row.b.caption,sep='\t')
        # b__caption 双下划线表示连表查询，查询关联表bussiness里面的caption列的值并返回。
        v2 = models.Host.objects.values('nid','hostname','b__caption')
        print(v2[0]['nid'],v2[1]['hostname'],v2[1].get('b__caption'))

        v3 = models.Host.objects.values_list('nid','hostname','b__caption')

        return render(request,'host.html',{'v1':v1,'v2':v2,'v3':v3})
    elif request.method == 'POST':
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        bid = request.POST.get('caption')
        print(h,i,bid)
        return render(request,'host.html')