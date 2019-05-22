from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.

def login(request):
    return render(request,'login.html',{'var':'变量1'})

def index(request):
    return HttpResponse('<h1>hello,index</h1>')

def register(request):
    if request.method == 'GET':
        return render(request,'register.html',{'var':'get方式'})
    elif request.method == 'POST':
        # 如果一个变量后面有多个值,那么要用getlist来拿,这样拿到的就是一个列表
        v=request.POST.getlist('favor')
        print(v)
        return render(request,'register.html')
    else:
        return HttpResponse('<h1>Error</h1>')

def upload(request):
    if request.method == 'POST':
        # 注意这里用POST.get是获取不到上传的数据的
        # aa = request.POST.get('load')
        # print(aa)

        # 这里的load名称要和upload.html里面的上传标签里面定义的name一致
        # 对上传的文件要用FILES来获取,获取上传的对象
        obj = request.FILES.get('load')
        # obj.name获取对象的名字
        print(obj,obj.name)
        import os
        file=os.path.join('upload',obj.name)
        f=open(file,'wb')
        # obj.chunks()  上传的文件实际是分块的,所以我们要用循环将一块块的数据写入到文件中
        for i in obj.chunks():
            f.write(i)
        f.close()
    return render(request,'upload.html')

class Home(View):
    # 下面的dispatch相当于起到了对get/post方法的装饰器的作用,在下面的get/post前后都执行命令.
    # 在get前打印before,在get后打印after.
    # 如果不需要在get/post前后执行命令,那么这个dispatch方法可以不写.
    def dispatch(self, request, *args, **kwargs):
        print('before')
        # 注意下面的dispatch()里面没有self,如果写上,会导致参数错位,从而导致获取不到request.method方法
        # super继承父类里面的disaptch方法,而不是覆盖父类里面的disaptch,相当于装饰了dispatch
        result=super(Home,self).dispatch(request, *args, **kwargs)
        print('after')
        # 注意这里要写上return返回,因为我们是通过dispatch来调用的get方法,get方法中的return是返回给dispatch,需要从dispatch里面return出来才能让urls调用到返回
        # 如果这里没有return,浏览器就会报错The view app01.views.Home didn't return an HttpResponse object. It returned None instead.
        return result
    # Home继承了View类里面的方法,而View里面的dispatch自动判断了浏览器传来的是get还是post,然后用反射的方法getattr自动匹配到
    # 我们下面定义的get/post方法并执行. 所以这里的方法名称get/post不是随便写的.要和View里面定义的一致
    def get(self,request):
        print(request.method)
        return render(request,'home.html')
    def post(self,request):
        print(request.method)
        return render(request,'home.html')

def dict(request):
    USER_DIC={
        'k1':'v1',
        'k2':'v2',
        'k3':'v3',
    }

    return render(request,'dict.html',{'dic':USER_DIC})

HOST_DIC={
        '1':{'name':'root1','ip':'172.11.22.22','os':'centos6'},
        '2':{'name':'root2','ip':'172.22.22.22','os':'centos7'},
        '3':{'name':'root3','ip':'172.33.22.22','os':'centos5'},
    }
def index(request):

    return render(request,'index.html',{'dic':HOST_DIC})


def detail(request,nid):
    # 注意这里的nid是django自动从你的url里面把正则变量取过来了.也就是urls.py里面定义的(\d+)的值
    # return HttpResponse(nid)
    d=HOST_DIC.get(nid)
    print(d)
    return render(request,'detail.html',{'detail':d})

def detail2(request,*args,**kwargs):
   # *args将传入的参数打包成元祖，**kwargs接收传入的字典形式参数，这么写就可以兼容各种正则匹配的方式了
    print(kwargs)
    nid=kwargs.get('nid',None)
    uid=kwargs['uid']
    d=HOST_DIC.get(nid)
    print(d)
    return render(request,'detail.html',{'detail':d,'uid':uid})

def url1(request,*args,**kwargs):
    from django.urls import reverse
    print(args)
    if args:
        print('exist')
        # 下面的命令相当于将原来的url替换为url2=reverse/2/2
        url2 = reverse('u2', args=(2, 2,))
        print(url2)
        return render(request,'reverse.html',{'url':url2})
    else:
        if kwargs:
            url3=reverse('u3',kwargs={'num1':3,'num2':4,})
            return render(request,'reverse.html',{'url':url3})
        else:
            url1=reverse('u1')
            return render(request,'reverse.html',{'url':url1})

def url2(request,*args,**kwargs):
    if args:
        url=2
        return render(request,'urlmatch.html',{'url':url})
    else:
        if kwargs:
            url=3
            return render(request,'urlmatch.html',{'url':url})
        else:
            url=1
            return render(request,'urlmatch.html',{'url':url})

def orm(request):
    from app01 import models
    # # 插入数据
    # # 第一种写法
    # models.UserInfo.objects.create(username='root',password='123',)
    # # 第二种写法
    # dic={'username':'eric','password':'222'}
    # models.UserInfo.objects.create(**dic)
    # # 第三种写法
    # obj=models.UserInfo(username='sun',password='jie')
    # obj.save()

    # 查找数据
    # 生成的result是QuerySet类型，可以用result.query来显示其真正执行的数据库查询语句
    result=models.UserInfo.objects.all()
    root=models.UserInfo.objects.filter(username='root',password='123')
    for i in result:
        print(i.username,i.password)
    # 删除数据
    models.UserInfo.objects.filter(username='sun').delete()

    # 更新数据
    models.UserInfo.objects.all().update(password='hnm')

    return render(request,'orm.html',{'result':result,'single_user':root})

