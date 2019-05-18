from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

def cmdb(request):
    return HttpResponse('<h1>cmdb</h1>')

# 注意request参数不能少,请求提交的值都是通过request来传进来的
def login(request):
    print(request.method)
    error_msg=''
    if request.method == "POST":
        #获取用户通过POST提交过来的数据
        #推荐get('username',None)的方式,这样就算username不存在,就会返回none,而不是直接报错
        user=request.POST.get('username',None)
        pwd=request.POST.get('password',None)
        print(user,pwd)
        if user == 'sun' and pwd == 'jie':
            # 当post方式登录成功后,跳转到/home/页面,注意这里的/home/要和urls.py里面定义的一致.后面要有/
            #由于是跳转本地,前面的/也不能少.,前面的/代表了前面的域名,没有就无法跳转本地
            return redirect('/home/')
        else:
            error_msg='用户名或密码错误'
    #     注意不要用下面的方式来获取,因为如果获取的key一旦不存在,页面就会报错
        #user = request.POST['username']


    #这里login.html就是templates下面的login.html,这个路径在setting.py里面就已经定义好了
    #通过render模块就能够实现自动读取templates文件夹下指定的文件并返回给浏览器解析
    # 可以将login.html中的{{error_msg}}建立映射,将render中的error_msg的值传进html中,相当于模版功能
    return render(request,'login.html',{'error_msg':error_msg})
    #上面的一行相当于下面的几行,起到的效果一样,只是django给我们将这个功能封装好了
    # f=open('templates/login.html','r',encoding='utf-8')
    # data=f.read()
    # f.close()
    # return HttpResponse(data)

USER_LIST = [
        {'username': 'alex', 'gender': '男', 'email': 'xxoo@xx.com'},
        {'username': 'sun', 'gender': '男', 'email': 'oo@xx.com'},
    ]
def home(request):

    if request.method == 'POST':
        u = request.POST.get('username')
        g = request.POST.get('gender')
        e = request.POST.get('email')
        tmp={'username':u,'gender':g,'email':e}
        USER_LIST.append(tmp)
        #将userlist传入到home.html,以供里面的模版引用
    return render(request,'home.html',{'userlist':USER_LIST})