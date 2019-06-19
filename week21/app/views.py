from django.shortcuts import render
from django.utils.safestring import mark_safe
# Create your views here.

def tp1(request):
    userlist=[1,2,3]
    return render(request,'tp1.html',{'u':userlist})

def tp2(request):
    name='filter'
    arg='this is a test text'
    return render(request,'tp2.html',{'name':name,'arg':arg})

List=[]
for i in range(1,103):
    List.append(i)
def user_list(request):
    # 获取get过来的数据（?p=2），如果没有，则默认值为1
    current_page=int(request.GET.get('p',1))
    start = current_page*10-9
    end = current_page*10
    data = List[start:end]
    # 分页 计算页码
    count,y=divmod(len(List),10)
    if y:
        count += 1

    page_list=[]
    for i in range(1,count):
        # 如果循环的标签等于当前所在的标签，则添加active样式
        if i == current_page:
            link='<a class="page active" href="/userlist/?p=%s">%s</a>' %(i,i)
            page_list.append(link)
        else:
            link='<a class="page " href="/userlist/?p=%s">%s</a>' %(i,i)
            page_list.append(link)
    # 对page_list列表进行拼接
    page=" ".join(page_list)
    # 默认情况下，django对于传给页面的数据都会处理成字符串，以防止xss攻击，所以如果我们要让传过去的
    # html语法生效，就需要mark_safe，告诉django这个字符串是安全的，让其进行html解析。
    # 也可以不在函数里面处理，传过去依然是字符串，将处理交给前端html页面也可以。 {{ page_str|safe }} 也可以解析字符串
    page_str= mark_safe(page)

    return render(request,'userinfo.html',{'data':data,'page_str':page_str})
