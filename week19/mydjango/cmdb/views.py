from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse,HttpResponseRedirect,render,redirect
from app01 import  models
def login(request):

    print(request)
    if request.method == 'GET':
        print(request)
        return render(request,'cmdb/login.html')
    elif request.method == 'POST':
        u=request.POST.get('user')
        p=request.POST.get('pass')
        obj=models.UserInfo.objects.filter(username=u,password=p).first()
        # count=models.UserInfo.objects.filter(username=u,password=p).count()
        print(obj)
        if obj:
            print(u,p)
            return render(request, 'cmdb/index.html')
        else:
            return HttpResponse('用户不存在')

    else:
        return render(request,'index.html')

def userinfo(request):
    if request.method == 'GET':
        alluser=models.UserInfo.objects.all()
        # 用alluser.query可以查看alluser翻译成的sql语句
        print(alluser.query)
        return render(request,'cmdb/userinfo.html',{'alluser':alluser})
    else:
        u=request.POST.get('user')
        p=request.POST.get('pass')
        models.UserInfo.objects.create(username=u,password=p,)
        return HttpResponseRedirect('/cmdb/userinfo')
def groupinfo(request):

    return render(request,'cmdb/groupinfo.html')

def userdetail(request, nid):
    print(id)
    detail=models.UserInfo.objects.filter(id=nid).first()
    # 下面的方法也可以只获取匹配到的一条数据，但是这个get方法在数据不存在时会报错，而不是像上面的语句一样返回空
    # models.UserInfo.objects.get(id=id)
    print(detail.username)
    return render(request,'cmdb/userdetail.html',{'detail':detail})

def useredit(request,nid):
    obj=models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        return render(request,'cmdb/useredit.html',{'userdata':obj})
    elif request.method == 'POST':
        u=request.POST.get('user')
        p=request.POST.get('pass')
        models.UserInfo.objects.filter(id=nid).update(username=u,password=p,)
        return redirect('/cmdb/userinfo')

def userdel(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return HttpResponseRedirect('/cmdb/userinfo')
