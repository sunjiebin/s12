from django.shortcuts import render,HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.forms import fields as Ffields
from app01 import models
from django.forms import widgets
# Create your views here.

class UserInfoModelForm(forms.ModelForm):
    # 可以自定义字段，这个字段与数据库没有关系，可以用该字段做一些其它的校验功能。
    # 比如我要设置登录有效期，那么我就需要一个选框，选中就设置session保存有效的时间，这个与数据库并没有关系。
    is_rmb=Ffields.CharField(widget=widgets.CheckboxInput())
    class Meta:
        #定义从那个models对象里面取数据。这里会把UserInfo里面的对象都取出来，并生成html标签
        # 和form不同在于modelform不用再自己写字段了，而是自动从生成的数据库对象里面将字符段都取出来
        model=models.UserInfo
        #这里的__all__相当于获取userinfo的所有字段并显示在前端
        fields='__all__'
        #也可以直接写字段名称，只显示指定的列
        # fields=['username','user_type']
        #也可以指定排除不显示某些列，而显示其他列
        # exclude=['username']
        # 可以在Model Form里面定义labels,widgets等各个属性。注意各个属性之间不要有","逗号，否则会报错
        labels ={
            'username':'用户',
            'email':'邮箱',
            'u2g':'组列表'
        }
        help_texts={
            'username':'提示信息',
        }
        # 将username变成文本框，并赋值class为c1
        widgets={
            'username':widgets.Textarea(attrs={'class':'c1'})
        }
        #自定义错误信息
        error_messages={
            '__all__':{'用于定义整体的错误信息'},
            'email':{'required':'邮箱不能为空','invalid':'邮箱格式不正确'},
            'username':{'required':'用户名不能为空','invalid':'输入正确的格式'},
        }
        #修改字段的类,我们model里面定义的email为邮件格式，这里我们可以修改为url格式，在网页上就会提示”请输入网址“
        #注意fields前面定义变量时已经用了，和模块fields重名了，在调用的时候就会出错，所以我们在导入模块时用了as Ffields，将fileds模块重命名了
        field_classes={
            #注意这里要填URLField对象，不能填URLField()，加上()后就成了类了，会报错。
            'username':Ffields.EmailField
        }
        #设置时区，默认UTC时间，我们需要的时东八区的时间。要让他生效在settings里面也要做对应的配置。
        # localized_fields=('ctime')

        #还可以自定义勾子，用于对字段自定义验证
        # def clean_username(self):
        #     new=self.cleaned_data['username']
        #     new=new+'cleantest'
        #     print(new)
        #     return new

class UserInfoForm(forms.Form):
    username = Ffields.CharField(max_length=128,label='用户名',error_messages={'invalid':'输入正确的格式','required':"不能为空"})
    email = Ffields.EmailField(label='邮箱',error_messages={'invalid':'邮箱格式错误','required':'邮箱不能为空'})
    user_type_id = Ffields.ChoiceField(
        choices=models.UserType.objects.values_list('id','caption')
    )
    # 定义初始化构造函数，用于函数初始化时执行操作
    def __init__(self,*args,**kwargs):
        #继承父类里面的方法
        super(UserInfoForm,self).__init__(*args,**kwargs)
        # print(self)
        # 为了让每次刷新页面时都能够获取到数据库最新的数据，需要我们在初始化函数时获取一次数据。
        # 如果不写下面行，那么页面上的数据就一直停留在第一次实例化类时的数据，不会跟随数据库的变化而实时更新。
        self.fields['user_type_id'].choices=models.UserType.objects.values_list('id','caption')

def index(request):
    if request.method=='GET':
        obj=UserInfoForm()
    # aa=models.UserType.objects.filter(caption='ceshi')
    # print(aa.delete())
        return render(request,'index.html',{'obj':obj})
    elif request.method=='POST':
        obj=UserInfoForm(request.POST)
        if obj.is_valid():
            data=obj.cleaned_data
            print(obj.cleaned_data)
            #插入数据
            models.UserInfo.objects.create(**data)
            #更新数据
            # models.UserInfo.objects.filter(username=data.get('username')).update(**data)
            return render(request,'index.html',{'obj':obj})
        else:
            #注意要用as_json()将输出转换为字典，这样才能拿到code的值invalid
            print(obj.errors.as_json())
            #如果不用as_json，默认输出的时ul标签
            print(obj.errors)
            #要用get('email')拿到具体的email标签的报错，否则只会拿到key的值email
            return HttpResponse(obj.errors.get('email'))
def index2(request):
    if request.method=='GET':
        obj=UserInfoModelForm()
        return render(request,'index.html',{'obj':obj})
    elif request.method == 'POST':

        obj=UserInfoModelForm(request.POST)
        print(obj.is_valid(),obj.cleaned_data,obj.errors.as_json())
        print(obj.cleaned_data.get('user_type').caption)
        if obj.is_valid():
            # 用ModelForm对数据提交时很简单，obj.save()就行了。会自动将提交的数据插入，如果有多对多关联表，也会一并插入相关数据
            # obj.save()

            #下面三行和上面的obj.save()是等价的关系
            # 可以传入False参数，这样就可以将主表和多对多关联表的保存拆分开来执行。
            # 通过查看源码发现当为false时，将__save_m2m内置函数赋值给了save_m2m,这样我们就可以调用该方法了
            instance=obj.save(False)
            instance.save()
            obj.save_m2m()
        return render(request,'index.html',{'obj':obj})

def user_list(request):
    li=models.UserInfo.objects.all().select_related('user_type')
    return render(request,'userlist.html',{'li':li})

def user_edit(request,nid):
    # 获取当前ID对应的用户信息
    # 将用户信息填入input框中
    if request.method == 'GET':
        #注意这里要用first()，拿到的才是具体数据。如果用all拿到的是QuerySet对象，会导致下面的ModelForm处理出错
        obj=models.UserInfo.objects.filter(id=nid).first()
        #使用modelForm在生成html表单时，还能够将查询到的所有数据自动填充进表单
        u=UserInfoModelForm(instance=obj)
        nid=nid
        return render(request,'useredit.html',{'u':u,'nid':nid})
    elif request.method=='POST':
        obj=models.UserInfo.objects.filter(id=nid).first()
        # 注意这里ModelForm传入POST数据后，要加上instance=obj，这样才会对instance里面对应的行进行更新。
        # 如果不加instance=obj，则在执行u.save()时，不是更新对应的行，而是直接将POST数据插入一条新的数据进去了。
        u=UserInfoModelForm(request.POST,instance=obj)
        if u.is_valid():
            u.save()
        else:
            print(u.errors.as_json())
        return render(request,'useredit.html',{'u':u})

def ajax(request):
    print('in ajax')
    return render(request,'ajax.html')

def ajax_json(request):
    print('in ajax_json')
    # import time
    # time.sleep(4)
    print(request.POST)
    ret={'code':True,'data':request.POST.get('user')}
    import json
    #status可以定义响应码，reason可以定义响应内容
    return HttpResponse(json.dumps(ret),status=201,reason='Not Found',)

def upload(request):

    return render(request,'upload.html')

def upload_file(request):
    # 注意，在传文件的时候，这里要用FILES方法，而不是用POST，用request.POST.get是取不到数据的
    file_obj=request.FILES.get('uploadfile')
    #通过file_obj.name拿到上传的文件名称
    print(file_obj,file_obj.name)
    import os
    print(os.path.curdir,os.path.join(os.pardir,'upload',file_obj.name))
    # 注意上传的文件如果要通过url访问，那么可以放在static目录下，因为这个目录在settings里面定义了是静态目录，所以可以直接访问该目录
    # 如果上传的目录直接放在根目录下，那么通过http://127.0.0.1:8000/upload/aa.jpg 这样是不能访问的。
    upfile_path=os.path.join('static/upload',file_obj.name)
    print(upfile_path)
    #上传文件要以二进制的方式来写入，用wb，不是w
    with open(upfile_path,'wb') as e:
        # 对file_obj.chunks()得到每一个文件块，并进行循环写入
        for item in file_obj.chunks():
            e.write(item)
    #注意用ajax时不要用render返回，render会返回当前页面，把整个页面当作字符串传给ajax是不对的。
    #当用render返回时，ajax中的success:function (arg,a1,a2) 中的arg参数就收到的就是整个html页面。
    #return render(request,'upload.html',{'obj':upfile})
    ret={'data':upfile_path,'code':True,}
    import json
    #注意字典返回时要用json.dumps转换为字符串。不然取到的数据不是完整的字典。
    return HttpResponse(json.dumps(ret))

def checkcode(request):
    from io import BytesIO
    from utils import check_code
    stream=BytesIO()
    img,code=check_code.create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode']=code
    return HttpResponse(stream.getvalue())

def login(request):
    if request.method == 'POST':
        code=request.POST.get('checkcode').upper()
        Session=request.session.get('CheckCode').upper()
        print(code,Session)
        if code == Session:
            print('验证码正确')
        else:
            print('验证码错误')
            
    return render(request,'login.html')

def kind(request):
    
    return render(request,'kind.html')

#@csrf_exempt
def uploadimg(request):
    import os,json
    print(request.GET.get('dir'))
    print(request.FILES.get('imgFile'))
    #注意这里用get得到的是上传的文件，而不是一个文件名。如果要得到文件名，需要img.name才可以
    img=request.FILES.get('imgFile')
    #注意这里拼接需要上传图片的文件名，而img是图片不是图片名称。所以要img.name获取名称
    srcimg=os.path.join('static/upload',img.name)
    with open(srcimg,'wb') as e:
        for i in img.chunks():
            e.write(i)
    print(srcimg)

    dic = {
        'error':0,
        #url后面接要预览的图片访问路径
        'url':'/'+srcimg,
        'message':'0代表上传成功，1代表失败了',
    }
    return HttpResponse(json.dumps(dic))

def file_manager(request):
    """
    文件管理
    :param request:
    :return:
    {
        moveup_dir_path:
        current_dir_path:
        current_url:
        file_list: [
            {
                'is_dir': True,
                'has_file': True,
                'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': xxx.png,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            },
            {
                'is_dir': True,
                'has_file': True,
                'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': xxx.png,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }
        ]

    }


    """
    import os,time,json
    dic = {}
    root_path = 'D:/学习相关/python/s12/week24/static'
    static_root_path = '/static/'
    request_path = request.GET.get('path')
    if request_path:
        abs_current_dir_path = os.path.join(root_path, request_path)
        move_up_dir_path = os.path.dirname(request_path.rstrip('/'))
        dic['moveup_dir_path'] = move_up_dir_path + '/' if move_up_dir_path else move_up_dir_path

    else:
        abs_current_dir_path = root_path
        dic['moveup_dir_path'] = ''

    dic['current_dir_path'] = request_path
    dic['current_url'] = os.path.join(static_root_path, request_path)

    file_list = []
    for item in os.listdir(abs_current_dir_path):
        abs_item_path = os.path.join(abs_current_dir_path, item)
        a, exts = os.path.splitext(item)
        is_dir = os.path.isdir(abs_item_path)
        if is_dir:
            temp = {
                'is_dir': True,
                'has_file': True,
                'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }
        else:
            temp = {
                'is_dir': False,
                'has_file': False,
                'filesize': os.stat(abs_item_path).st_size,
                'dir_path': '',
                'is_photo': True if exts.lower() in ['.jpg', '.png', '.jpeg'] else False,
                'filetype': exts.lower().strip('.'),
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }

        file_list.append(temp)
    dic['file_list'] = file_list
    return HttpResponse(json.dumps(dic))