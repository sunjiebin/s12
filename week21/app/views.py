from django.shortcuts import render
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
    obj=Page(current_page,total_num)
    data=obj.data
    page_str=obj.page_str('/userlist/')
    return render(request,'userinfo.html',{'data':data,'page_str':page_str})
