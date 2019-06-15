from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from myapp import models
import json
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
        b1 = models.Bussiness.objects.all()
        print(v1[0].hostname)
        for row in v1:
            print(row.nid,row.hostname,row.b_id,row.b.caption,sep='\t')
        # b__caption 双下划线表示连表查询，查询关联表bussiness里面的caption列的值并返回。
        v2 = models.Host.objects.values('nid','hostname','b__caption')
        print(v2[0]['nid'],v2[1]['hostname'],v2[1].get('b__caption'))

        v3 = models.Host.objects.values_list('nid','hostname','b__caption')

        return render(request,'host.html',{'v1':v1,'v2':v2,'v3':v3,'b1':b1})
    elif request.method == 'POST':
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        bid = request.POST.get('caption')
        p = request.POST.get('port')
        print(h,i,p,bid)
        models.Host.objects.create(hostname=h,ip=i,port=p,b_id=bid)
        return HttpResponseRedirect('/host')
    
def ajax_check(request):
    ret = {'status':True,'error':None,'data':None}
    print(request.POST)
    try:
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        bid = request.POST.get('caption')
        p = request.POST.get('port')
        print('ajax',h, i, p, bid)

        if h and len(h)>5:
            models.Host.objects.create(hostname=h, ip=i, port=p, b_id=bid)

        else:
            ret['status']=False
            ret['error']='主机名太短'

    except Exception as e:
        ret['status']=False
        ret['error']='请求错误'
    #     注意：这里HttpResponse是不能直接传字典的，只能传字符串，所以，这里需要json.dumps()来对字典序列化成字符串
    return HttpResponse(json.dumps(ret))

def ajax_edit(request):
    ret = {'status':True,'error':None,'data':None}
    print(request.POST)
    try:
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        bid = request.POST.get('caption')
        p = request.POST.get('port')
        nid = request.POST.get('nid')
        print('ajax',nid, h, i, p, bid)

        if h:
            print(models.Host.objects.filter(nid=nid))
            models.Host.objects.filter(nid=nid).update(hostname=h, ip=i, port=p, b_id=bid)

        else:
            ret['status']=False
            ret['error']='主机名太短'

    except Exception as e:
        ret['status']=False
        ret['error']='请求错误'
    #     注意：这里HttpResponse是不能直接传字典的，只能传字符串，所以，这里需要json.dumps()来对字典序列化成字符串
    return HttpResponse(json.dumps(ret))

def ajax_del(request):
    ret = {'status':True,'error':None,'data':None}
    print(request.POST)
    try:
        nid = request.POST.get('nid')
        print('ajax',nid)

        if nid:
            print(models.Host.objects.filter(nid=nid))
            models.Host.objects.filter(nid=nid).delete()
        else:
            ret['status']=False
            ret['error']='nid不存在'

    except Exception as e:
        ret['status']=False
        ret['error']='请求错误'
    #     注意：这里HttpResponse是不能直接传字典的，只能传字符串，所以，这里需要json.dumps()来对字典序列化成字符串
    return HttpResponse(json.dumps(ret))

def app(request):
    if request.method == 'GET':
        app_list = models.Applications.objects.all()
        host_list = models.Host.objects.all()
        # for row in app_list:
        #     print(row.name,row.r.all())

        return render(request,'app.html',{'app_list':app_list,'host_list':host_list})
    elif request.method == 'POST':
        app = request.POST.get('appname')
        # 注意后端传来的hostname是一个列表，所以对应的我们要用getlist来获取，否则只能拿到最后一个值。
        host = request.POST.getlist('hostname')
        # print(app,host)
        # 添加应用，插入一条数据，此时会生成一个obj对象
        obj = models.Applications.objects.create(name=app)
        # 对这个对象的关联表添加对应关系
        obj.r.add(*host)
        return HttpResponseRedirect('/app')
    
def ajax_addapp(request):
    ret = {'status':True,'error':None,'data':None}
    print(request.POST)
    try:
        app = request.POST.get('appname')
        host = request.POST.getlist('hostname')
        print('ajax',app,host)


        if app:
             obj = models.Applications.objects.create(name=app)
             obj.r.add(*host)
        else:
            ret['status']=False
            ret['error']='app不存在'

    except Exception as e:
        ret['status']=False
        ret['error']='请求错误'
    #     注意：这里HttpResponse是不能直接传字典的，只能传字符串，所以，这里需要json.dumps()来对字典序列化成字符串
    return HttpResponse(json.dumps(ret))

#编辑应用和主机
def ajax_eidtapp(request):
    ret = {'status': True, 'error': None, 'data': None}
    try:
        appname = request.POST.get('app')
        host = request.POST.getlist('host')
        appid = request.POST.get('appid')
        print('ajax',appname,host,appid)
        if appname:
             print(ret['status'])
             # 注意这里要写.get(id=appid)，用filter(iid=appid)是不行的，这样获取到的obj对象不能执行obj.r.set
             # 区别在于get获取到的是一个对象，而filter获取到的是一个对象列表，如果要得到filter下面的对象，需要进行切片obj[0]来获取下面的对象才行
             obj = models.Applications.objects.get(id=appid)
             obj2 = models.Applications.objects.filter(id=appid)
             print('obj2',type(obj2[0]))
             print(type(obj))
             print(obj.id,obj.name)
             # 通过.get()获取到的对象，需要用obj.name='值'的方式赋值，不能用obj.create(name=appname)的方式
             obj.name=appname
             # 注意要save()保存
             obj.save()
             obj.r.set(host)
             print(obj.name)

             # obj.r.set(host)
        else:
            ret['status']=False
            ret['error']='app不存在'

    except Exception as e:
        ret['status']=False
        ret['error']='请求错误'
    #     注意：这里HttpResponse是不能直接传字典的，只能传字符串，所以，这里需要json.dumps()来对字典序列化成字符串
    return HttpResponse(json.dumps(ret))

def ajax_alldelapp(request):
    ret = {'status': True, 'error': None, 'data': None}
    print('request',request)
    if request.method == 'POST':
        try:
            hidlist = request.POST.getlist('hidlist')
            appid = request.POST.get('appid')
            print('ajax',appid,hidlist)
            print(type(appid))

            if appid:
                print(ret['status'])
                obj = models.Applications.objects.get(id=appid)
                # 执行删除时一定要注意关联表的问题，我设置了两张关联表applications_r,apptohost，两个关联表都有appliccations_id=3的关联数据,结果导致下面的删除语句怎么也执行不了。
                # 错误提示'str' object is not callable。实际上并不是因为id为str导致的，而是apptohost关联表里面也有关联数据存在，从而无法删除applications里面id=3的数据。
                models.Applications.objects.filter(id=appid).delete()
                print(obj.id,obj.name,appid)
                obj.r.remove(*hidlist)

            else:
                ret['status']=False
                ret['error']='app不存在'

        except Exception as e:
            print(e)
            ret['status']=False
            ret['error']='请求错误'
        #     注意：这里HttpResponse是不能直接传字典的，只能传字符串，所以，这里需要json.dumps()来对字典序列化成字符串
        return HttpResponse(json.dumps(ret))
    else:
        return HttpResponseRedirect('/app')