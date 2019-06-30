from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.cache import cache_page
# Create your views here.

#通过装饰器csrf_exempt可以将该函数跳过csrf检测
# @csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        user=request.POST.get('username')
        pwd=request.POST.get('pwd')
        exp=request.POST.get('exp')
        
        print(user,pwd,exp)
        if user=='sun' and pwd=='jie':
            #生成随机字符串，将字符串写入到浏览器cookie中，将字符串写入到session中，并作为key，将下面设置的值写入到session中，作为随机字符串的value
            #设置了session后，用户浏览器的cookie中会有一个cookie，{'sessionid':'随机值'},
            # 同时服务器端的数据库django_session表中也会生成对应的一条数据，session_key和cookie的key对应，session_data加密存放。
            #设置值
            request.session['user']=user
            request.session['pwd']=pwd
            request.session['login']=True
            if exp=='1':
                #设置session超时时间为10s
                print('设置了超时')
                request.session.set_expiry(10)
            return redirect('/index')
        else:
            return redirect('/login')

def index(request):
    #获取当前user的随机字符串
    #根据随机字符串获取对应的session信息
    #获取值
    u=request.session.get('user')
    l=request.session.get('login')
#    if request.session['login']:
    if request.session.get('login'):
        return render(request,'index.html')
    else:
        return HttpResponse('用户未登录')
    
def logout(request):
    request.session.clear()
    return redirect('/index')

def test(request):
    print('测试中间件流程')
    return HttpResponse('ok')

def cache_view(request):
    import time
    t=time.time()
    return render(request,'cache.html',{'t':t})

#对整个函数进行缓存 10代表缓存10s.那么访问页面时的时间数据就会10s变一次
#函数如果还带了参数，那么每个参数都会做一个缓存
@cache_page(10)
def cache(request):
    import time
    from single import mysg
    a=mysg.single.send(sender='test',args2='a',args3='b')
    print('取信号里面的参数',a[0][1].get('args2'))
    return HttpResponse(time.time())

