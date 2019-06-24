from django.shortcuts import render,HttpResponseRedirect
from utils.pagenation import Page
from host import models
# Create your views here.

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




def hostlist(request):
    if request.method == 'GET':
        v1 = models.Host.objects.filter(nid__gt=0) #和all()结果一样
        d1 = models.Department.objects.all()

        for row in v1:
            print(row.nid,row.hostname,row.to_department_id,row.to_department.fullname,sep='\t')


        return render(request,'host/host.html',{'v1':v1,'d1':d1})
    elif request.method == 'POST':
        h = request.POST.get('hostname')
        i = request.POST.get('ip')
        bid = request.POST.get('department')
        p = request.POST.get('port')
        print(h,i,p,bid)
        models.Host.objects.create(hostname=h,ip=i,port=p,to_department_id=bid)
        return HttpResponseRedirect('/host/hostlist')