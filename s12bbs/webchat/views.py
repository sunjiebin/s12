from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from webchat import models
import json
import time, queue
# Create your views here.

@login_required()
def dashboard(request):
    return render(request,'webchat/dashboard.html')

global_msg_queues={}
def send_msg(request):

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
            msg_list.append(que_obj.get(timeout=60))
        except queue.Empty:
            print('等待超时了')
    return HttpResponse(json.dumps(msg_list))   #返回时需要json.dumps将其转换为字符串
