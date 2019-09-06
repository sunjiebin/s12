from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from webchat import models
import json,time,queue,os
from django.core.cache import cache
# Create your views here.

@login_required()
def dashboard(request):
    return render(request,'webchat/dashboard.html')

global_msg_queues={}
def send_msg(request):
    '''该函数用于放入消息到队列'''
    msg_data=request.POST.get('data')
    print(msg_data)
    if msg_data:
        # 前端通过JSON.stringify将html对象转换为了字符串，这里需要json.loads将传过来的字符串再解析成字典
        msg_data=json.loads(msg_data)
        # 如果不loads，下面对字典操作会提示TypeError: 'str' object does not support item assignment
        msg_data['timestamp']=time.time()
        #一定要注意，前端传过来的都是字符串形式的值，msg_data['to']得到的是字符串格式的id，数据库拿到的又是整数的id，所以需要Int转换成一致
        user_id=int(msg_data['to'])
        if msg_data['type']=='single':
            if not global_msg_queues.get(user_id):
                global_msg_queues[user_id]=queue.Queue()
            global_msg_queues[user_id].put(msg_data)
        else:
            group_obj=models.WebGroup.objects.get(id=msg_data['to'])
            for member in group_obj.members.select_related():
                if not global_msg_queues.get(member.id):    #如果字典里不存在这个用户的队列，则创建一个队列
                    global_msg_queues[member.id]=queue.Queue()
                if member.id != request.user.userprofile.id:    #用户id不等于自己时，才向队列发数据，避免把消息发给自己
                    global_msg_queues[member.id].put(msg_data)

    print('队列字典',global_msg_queues)
    # print('队列内容',global_msg_queues[user_id].get())
    return HttpResponse(msg_data)

def get_new_msg(request):
    if request.user.userprofile.id not in global_msg_queues:
        print(f'no queue for user {request.user.userprofile.id,request.user.userprofile.name}')
        global_msg_queues[request.user.userprofile.id]=queue.Queue()
    msg_list=[]
    print('当前用户',request.user.userprofile.name,request.user.userprofile.id)
    que_obj=global_msg_queues[request.user.userprofile.id]
    # print('队列消息',que_obj.get())

    que_length=que_obj.qsize()
    print('队列长度',que_length)
    if que_length>0:
        for msg in range(que_length):
            msg_list.append(que_obj.get())
        print('所有消息列表',msg_list)
    else:
        print('目前没有消息',request.user.userprofile.name)
        try:
            # 设置超时60s，60s内如果有内容进来就append，没有就挂起等待60s直到抛出超时异常。
            msg_list.append(que_obj.get())
        except queue.Empty:
            print('等待超时了')
    return HttpResponse(json.dumps(msg_list))   #返回时需要json.dumps将其转换为字符串



def file_upload(request):
    print(request.POST,request.FILES)
    recv_size=0
    file_obj=request.FILES.get('file')  #这里的file是前端fromData.append里面定义的file，file_obj是一个对象，不是文件名称
    #file_data=json.loads(file_obj)
    print(file_obj,type(file_obj))
    user_home_dir=f'uploads/{request.user.userprofile.id}'
    if not os.path.isdir(user_home_dir):
        os.mkdir(user_home_dir)

    new_file_name='%s/%s'%(user_home_dir,file_obj.name)
    print('文件路径为：',new_file_name)
    with open(f'{new_file_name}','wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
            recv_size+=len(chunk)
            cache.set(file_obj.name,recv_size)

    return HttpResponse('文件上传成功')

# 课上该段视频缺失，没有跑通改用其他方法实现

# def delete_cache_key(request):
#     cache_key=request.GET.get('key_name')
#     cache.delete(cache_key)
#     return HttpResponse(f'缓存{cache_key}被删除')

# def file_upload_progress(request):
#     print(request.GET.get('filename'))
#     filename=request.GET.get('filename')
#     recv_size=cache.get(filename)
#     print('文件大小为',recv_size)
#     dict={}
#     dict['recv_size']=recv_size
#     dict['filename']=filename
#     return HttpResponse(json.dumps(dict))

'''
下面时上传显示进度条的方法
from django.views.generic import View
class UploadPage(View):
    def get(self, request):
        return render(request,'webchat/upload.html')


class Upload(View):
    def post(self, request):
        file = request.FILES['file']
        self.handle_uploaded_file(file)
        return HttpResponse('文件上传成功')

    def handle_uploaded_file(self, f):
        print(f.name)
        with open(f'uploads/{f.name}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
'''


