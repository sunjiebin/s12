from django.shortcuts import render,redirect,HttpResponse
from utils.pagenation import Page
# Create your views here.

def tp1(request):
    userlist=[1,2,3]
    return render(request,'tp1.html',{'u':userlist})

def tp2(request):
    name='filter'
    arg='this is a test text'
    return render(request,'tp2.html',{'name':name,'arg':arg})

def user_list(request):
    total_num = 503
    # 获取get过来的数据（?p=2），如果没有，则默认值为1
    current_page=int(request.GET.get('p',1))
    # 注意从request传来的都是字符串，所以需要Int转换为数字
    per_page_count=int(request.COOKIES.get('page_num',10))
    print('yes',per_page_count)
    obj=Page(current_page,total_num,per_page_count)
    data=obj.data
    page_str=obj.page_str('/userlist/')
    return render(request,'userinfo.html',{'data':data,'page_str':page_str})

    
user_info={
    'sun':'jie',
    'luo':'mi',
}
def user_login(request):

    if request.method == 'GET':
         return render(request,'login.html')
    elif request.method == 'POST':
        u=request.POST.get('username')
        p=request.POST.get('pwd')
        if user_info.get(u):
            if user_info.get(u) == p:
                res=redirect('/index')
                #设置cookie，将post提交的用户名设置为cookie的值。cookie的key为username，值为sun,即{'username':'sun'}
                #默认设置的cookie在关闭浏览器后就会失效
                #res.set_cookie('username',u)
                #max_age=10设置10s后cookie过期
                #res.set_cookie('username',u,max_age=10)

                #expires= 设置超时实间，这个后面接的是具体的过期时间，而不是多少秒之后
                import datetime
                #获取当前时间的时间戳
                current_date=datetime.datetime.utcnow()
                print(current_date)
                #timedelta在当前时间上加上5s
                expire_date=current_date+datetime.timedelta(seconds=5)
                res.set_cookie('username',u,expires=expire_date)

                #返回跳转页码，并设置cookie
                return res
            else:
                return HttpResponse('用户密码不正确')
        else:
            return HttpResponse('用户不存在')
       # return render(request,'login.html',{'username':u,'pwd':p})
def index(request):
    # 获取cookies,cookies实际就是存储的一个字典，所以可以用[]或者get来取值，但是[]取值如果值不存在，则程序会报错
    #v=request.COOKIES['username']
    v=request.COOKIES.get('username')
    # 如果cookie不存在，则跳转到登陆页
    if not v:
        return redirect('/login/')
    return render(request,'index.html',{'username':v})

def cookie(request):
    request.COOKIES.get('username')
    response=redirect('/index')
    response.set_cookie('key','value')
    return response