from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from bbs import  models
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')  # 倒序(-'position_index')

#对index添加登录校验的装饰器，那么这个index.html页面就得先登录才能访问
@login_required
def index(request):
    #提取文章分类标签，过滤出set_as_top_menu为True的数据，并且依照position_index来排序
    category_list=models.Category.objects.filter(set_as_top_menu=True).order_by('position_index')       #倒序(-'position_index')
    category_obj = models.Category.objects.get(position_index=1)
    article_list = models.Article.objects.filter(status='published')
    return render(request,'bbs/index.html',{'category_list':category_list,'category_obj':category_obj,'article_list':article_list})

def category(request,id):
    category_obj=models.Category.objects.get(id=id)
    #我们约定position_index=1时，代表就是全部
    if category_obj.position_index == 1:
        article_list=models.Article.objects.filter(status='published')
    else:
        article_list=models.Article.objects.filter(category_id=id,status='published')
    return render(request,'bbs/index.html',{'category_list':category_list,'category_obj':category_obj,'article_list':article_list})

def acc_login(request):
    if request.method == 'POST':
        print(request.POST)
        #去数据库认证
        user = authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
        print('authenticate返回的值',user)
        #如果认证成功，则会返回user对象，失败则为None
        if user is not None:    #认证成功
            #login用于登录，本质上会在后端生成相关的session
            login(request,user)
            #获取get的参数 URL后面？部分的数据，会被以字典的形式获取到，这里将获取到next的值
            backurl=request.GET.get('next')
            return HttpResponseRedirect(backurl or'/bbs')       # or用于当backurl为空时，则自动跳转到用/bbs
        else:
            login_err='用户名或密码错误'
            return render(request,'login.html',{'login_err':login_err})
    return render(request,'login.html')

def acc_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def article_detail(request,article_id):
    article_obj=models.Article.objects.get(id=article_id)
    return render(request,'bbs/article_detail.html',{'article_obj':article_obj,'category_list':category_list})

def comment(request):
    print(request.POST)
    new_comment_obj=models.Comment(
        article_id=request.POST.get('article_id'),
        parent_comment_id=request.POST.get('parent_comment_id') or None,
        comment_type=request.POST.get('comment_type'),
        comment=request.POST.get('comment'),
        user_id=request.user.userprofile.id,
    )
    new_comment_obj.save()
    return HttpResponse('ok')