from django.shortcuts import render,HttpResponse
from django.views import View
import json
from app01 import models
# Create your views here.
class BaseResponse(object):
    def __init__(self):
        self.status=True
        self.data=None
        self.message=None

class ServerView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'server.html')

class ServerJsonView(View):
    def __init__(self):
        pass
    def get(self,request,*args,**kwargs):
        response=BaseResponse()
        try:
            # 获取显示的列
            table_config=[
                {
                    'q':'hostname',     #注意这里的q的值hostname必须于数据库里面的表的列名一样，因为后面会直接用这个值去查询数据库
                    'title':'主机名',
                    'display':1,
                },
                {
                    'q':'user_id__name',
                    'title':'用户组',
                    'display':0,
                },
                {
                    'q':'port',
                    'title':'端口',
                    'display':1
                },
                {
                    'q':'bussiness_unit__name',
                    'title':'业务线',
                    'display':1,
                },
                {
                    'q':None,
                    'title':'操作',
                    'display':1,
                }
            ]
            value_list=[]
            for item in table_config:
                # 判断q是否存在，因为有些列比如“操作”列是不需要查询数据库的，所以如果为None则不执行value_list.append
                if item['q']:
                    value_list.append(item['q'])
            # values(*value_list)在查询中传入value_list列表，列表里面是要显示的字段名称
            result=models.Server.objects.values(*value_list)
            # 由于返回的是QuerySet类型，并不能想列表一样直接操作，所以需要用list(result)将QuerySet转换为list列表格式
            result=list(result)
            print(result)
            ret={'table_config':table_config,'data_list':result}
            response.data=ret
        except Exception as e:
            response.status=False
            response.message=str(e)

        return HttpResponse(json.dumps(response.__dict__))      #注意这里要json.dumps将其转换为字符串传过去，否则取不到传入的数据
