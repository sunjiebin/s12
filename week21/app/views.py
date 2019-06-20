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

class Page:
    def __init__(self,current_page,total_count,per_page_count=11,page_num=10):
        self.current_page=current_page
        self.total_count=total_count
        self.per_page_count=per_page_count
        self.page_num=page_num
    @property
    def start(self):
        return (self.current_page*self.page_num-self.page_num)
    @property
    def end(self):
        return self.current_page*self.page_num
    @property
    def total_page(self):
        # 分页 计算页码
        total_page, y = divmod(len(List), page_num)
        if y:
            total_page += 1
        return total_page
    @property
    def page_roll(self):
        # 标签滚动
        if self.total_page <= self.page_num:
            start_index = 1
            end_index = self.total_page + 1
        else:
            if self.current_page <= (self.page_num - 1) / 2:
                start_index = 1
                end_index = self.page_num + 1
            else:
                if self.total_page - self.current_page < (self.page_num - 1) / 2:
                    start_index = self.total_page - self.page_num + 1
                    end_index = self.total_page + 1
                    print(start_index, end_index)
                else:
                    start_index = int(self.current_page - (self.page_num - 1) / 2)
                    end_index = int(self.current_page + (self.page_num + 1) / 2)

        return (start_index,end_index)

    def pagg_str(self):
        page_list = []
        start_index, end_index = self.page_roll
        # 上一页
        if self.current_page <= 1:
            link = '<a class="page" href="#">上一页</a>'
        else:
            link = '<a class="page" href="/userlist/?p=%s">%s</a>' % (self.current_page - 1, '上一页')
        page_list.append(link)

        # 循环生成所有页码链接
        for i in range(start_index, end_index):
            # 如果循环的标签等于当前所在的标签，则添加active样式
            if i == self.current_page:
                link = '<a class="page active" href="/userlist/?p=%s">%s</a>' % (i, i)
                page_list.append(link)
            else:
                link = '<a class="page " href="/userlist/?p=%s">%s</a>' % (i, i)
                page_list.append(link)

        # 下一页
        if self.current_page >= self.total_page:
            link = '<a class="page" href="#">%s</a>' % ('下一页')
        else:
            link = '<a class="page" href="/userlist/?p=%s">%s</a>' % (self.current_page + 1, '下一页')
        page_list.append(link)

        # 搜索页码
        page_serach = '''
            <input id="input_page" type="text" class="input_search" placeholder="页码"/>
            <input id="search_button" type="button" onclick="search(this)" value="搜索"/>
            <script>
            function search(i) {
                var page=document.getElementById('input_page').value;
                var url='/userlist/?p='+ page;
                console.log(url);
                location.href = url
            }
            </script>
        '''
        page_list.append(page_serach)

        # 对page_list列表进行拼接
        page = " ".join(page_list)
        # 默认情况下，django对于传给页面的数据都会处理成字符串，以防止xss攻击，所以如果我们要让传过去的
        # html语法生效，就需要mark_safe，告诉django这个字符串是安全的，让其进行html解析。
        # 也可以不在函数里面处理，传过去依然是字符串，将处理交给前端html页面也可以。 {{ page_str|safe }} 也可以解析字符串
        page_str = mark_safe(page)

        return page_str

List=[]
total_num=503
page_num=11
page_num=10
for i in range(1,total_num):
    List.append(i)
def user_list(request):
    # 获取get过来的数据（?p=2），如果没有，则默认值为1
    current_page=int(request.GET.get('p',1))
    obj=Page(current_page,total_num,page_num,page_num)
    start = obj.start
    end = obj.end
    data = List[start:end]
    total_page=obj.total_page


    # # 标签滚动
    # if total_page<=page_num:
    #     start_index=1
    #     end_index=total_page+1
    # else:
    #     if current_page<=(page_num-1)/2:
    #         start_index=1
    #         end_index=page_num+1
    #     else:
    #         if total_page-current_page<(page_num-1)/2:
    #             start_index=total_page-page_num+1
    #             end_index=total_page+1
    #             print(start_index,end_index)
    #         else:
    #             start_index = int(current_page - (page_num - 1) / 2)
    #             end_index = int(current_page + (page_num + 1) / 2)

    page_list=[]
    # 上一页
    if current_page<=1:
        link = '<a class="page" href="#">上一页</a>'
    else:
        link = '<a class="page" href="/userlist/?p=%s">%s</a>' % (current_page-1, '上一页')
    page_list.append(link)

    # 循环生成所有页码链接
    for i in range(start_index,end_index):
        # 如果循环的标签等于当前所在的标签，则添加active样式
        if i == current_page:
            link='<a class="page active" href="/userlist/?p=%s">%s</a>' %(i,i)
            page_list.append(link)
        else:
            link='<a class="page " href="/userlist/?p=%s">%s</a>' %(i,i)
            page_list.append(link)

    # 下一页
    if current_page>=total_page:
        link = '<a class="page" href="#">%s</a>' % ('下一页')
    else:
        link = '<a class="page" href="/userlist/?p=%s">%s</a>' % (current_page+1, '下一页')
    page_list.append(link)

    # 搜索页码
    page_serach='''
        <input id="input_page" type="text" class="input_search" placeholder="页码"/>
        <input id="search_button" type="button" onclick="search(this)" value="搜索"/>
        <script>
        function search(i) {
            var page=document.getElementById('input_page').value;
            var url='/userlist/?p='+ page;
            console.log(url);
            location.href = url
        }
        </script>
    '''
    page_list.append(page_serach)

    # 对page_list列表进行拼接
    page=" ".join(page_list)
    # 默认情况下，django对于传给页面的数据都会处理成字符串，以防止xss攻击，所以如果我们要让传过去的
    # html语法生效，就需要mark_safe，告诉django这个字符串是安全的，让其进行html解析。
    # 也可以不在函数里面处理，传过去依然是字符串，将处理交给前端html页面也可以。 {{ page_str|safe }} 也可以解析字符串
    page_str= mark_safe(page)

    return render(request,'userinfo.html',{'data':data,'page_str':page_str})
