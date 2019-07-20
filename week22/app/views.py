from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.cache import cache_page
from django import forms
from django.forms import fields,widgets
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
    ret={'k':'v1','k2':'v2'}
#    if request.session['login']:
    if request.session.get('login'):
        return render(request,'index.html')
    else:
        return HttpResponse("list(%s)" %(ret))
    
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


class FM(forms.Form):
    # error_messages自定义错误显示信息。required/invalid/不能随便写，必须跟返回的obj.errors里面的code的值一样。如"code": "invalid"，那么这里"invalid"就是key
    user=fields.CharField(error_messages={'required':'用户名不能为空'},initial='sun',label='用户名',disabled=True)
    #widget用来引用插件，widgets.PasswordInput代表密码插件。
    #这个插件有很多，input，select,radius,checkbox等都有。
    # fields.CharField表示对字段验证，widget表示使用里面的某个插件
    pwd=fields.SlugField(max_length=12,min_length=6,
                         error_messages={'required':'密码不能为空','min_length':'太短了','max_length':'太长了','invalid':'只支持数字字母下划线减号'},
                         widget=widgets.PasswordInput)
    email=fields.EmailField(error_messages={'required':'用户名不能为空','invalid':'邮箱格式错误'},initial='sun@jie.bin')
    #可以定义input的类型，比如widgets.Textarea就是文本框，还可以定义属性，attrs可以定义里面的属性，样式等。
    #引用文本框插件Textarea，并且给文本框定义样式。
    msg=fields.CharField(required=False,error_messages={'required':'信息不能为空'},widget=widgets.Textarea(attrs={'class':'c1','name':'msg'}))
    # phone=fields.CharField(validators=[RegexValdator(r'^[0-9]+$','请输入数字'),RegexValdator(r'^159[0-9]+$','数字必须以159开头')])
    # 在页面上显示templates文件夹下面的所有文件
    file=fields.FilePathField(path='templates')
    #下拉框
    #单选框
    c1=fields.ChoiceField(choices=[(0,'北京'),(1,'上海'),(2,'NewYork')],initial=2)
    #多选框
    c2=fields.MultipleChoiceField(choices=[(0,'北京'),(1,'上海'),(2,'NewYork')],initial=[1,2])
    #单选按钮
    c3=fields.ChoiceField(choices=[(0,'北京'),(1,'上海'),(2,'NewYork')],widget=widgets.RadioSelect)
    #单选select
    c4=fields.CharField(widget=widgets.Select(choices=((1,'上海'),(2,'北京'),)))
    #单选勾选
    c5=fields.CharField(widget=widgets.CheckboxInput())
    #多选checkbox
    c6=fields.MultipleChoiceField(choices=((1,'上海'),(2,'北京'),(3,'湖南'),),widget=widgets.CheckboxSelectMultiple())

def fm(request):
    if request.method=='GET':
        # 传入FM()对象，在html里面就能直接obj.user来生成input框了，并且自带校验功能
         dic={
            'user':'sun',
            'pwd':'111111',
            'email':'sun@sun.com',
            'msg':'测试默认值传入',
             'c3':2,
             'c6':[1,2],
         }
        #可以给这个函数传入一个字典，字典的Key和FM里面定义的字段名称一致就可以了。页面就能够生成默认值了
         obj=FM(initial=dic)
         return render(request,'fm.html',{'obj':obj})
    elif request.method=='POST':
        #将POST的数据传入校验函数
        obj=FM(request.POST)
        #is_valid()执行校验,所有输入校验成功就返回True，有失败就返回False
        r1=obj.is_valid()
        print('r1',r1)
        #如果r1有，代表通过校验
        if r1:
            #打印校验成功的数据，生成的是一个字典，可以直接写入数据库
            #{'user': 'fdsf', 'pwd': 'sdfsfdf', 'email': 'sf@sd.com'}
            print(obj.cleaned_data)
            # 直接将数据插入到数据库，前提是字段名称和key要一致
            # models.UserInfo.objects.create(**obj.cleaned_data)
        else:
            #校验失败打印的错误信息

            #默认拿到的是<ul class="errorlist"><li>email<ul class="errorlist"><li>Enter a valid email address.</li></ul></li></ul>
            # print(obj.errors)
            #通过as_json()对输出格式化，拿到的是字典。{"email": [{"message": "Enter a valid email address.", "code": "invalid"}]},注意json格式化后中文会变成unicode编码格式
            #这里输出的code:invalid的value与FM函数里面的error_messages里面的字典Key对应
            print(obj.errors.as_json())
            # get拿到错误信息，[0]拿到里面具体的错误输出文字
            print('user错误输出',obj.errors.get('user'))
        return  render(request,'fm.html',{'obj':obj})
