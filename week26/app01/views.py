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
                # 这里面的元素就是要显示的表格标题名称
                {
                    'q':'id',
                    'title':'id',
                    'display':0,
                    'text':{},
                },
                {
                    'q':'hostname',     #注意这里的q的值hostname必须于数据库里面的表的列名一样，因为后面会直接用这个值去查询数据库
                    'title':'主机名',
                    'display':1,
                    # 自定义显示数据
                    'text':{'content':'{n}-{m}','kwargs':{'n':'华东1','m':'@hostname'}},
                    # """   注意注释不要弄错了，这个出错导致问题排查了很久
                    # 自定义属性。 设置original等于数据库查出来的原来的值。这样做便于在我们对表单修改后，可以比对修改后的数据，如果有变化就提交数据库更新。
                    # 没有变化，则不提交更新。因为我们行和列很多，有些行列不一定有更改，如果没有修改的数据也提交到数据库更新，就会消耗数据库性能。
                    # 在前端先判断一下，再将有更改的数据提交更新，这样可以减轻数据库的压力。
                    # """
                    'attr':{'original':'@hostname','k1':'v1'}
                },
                {
                    'q':'user_id__name',
                    'title':'用户组',
                    'display':1,
                    'text': {'content': '{n}-{m}', 'kwargs': {'n': '深圳区', 'm': '@user_id__name'}},
                    'attr': {'original': '@user_id__name', 'k1': 'v1'}
                },
                {
                    'q':'port',
                    'title':'端口',
                    'display':1,
                    'text': {'content': '{m}', 'kwargs': {'m': '@port'}},
                    'attr': {'original': '@port', 'k1': 'v1'}
                },
                {
                    'q':'bussiness_unit__name',     #注意__name是双下划线，代表连表查询。根据外键跨表查询app01_BusinessUnit表里面的name字段
                    'title':'业务线',
                    'display':1,
                    'text': {'content': '{m}', 'kwargs': {'m': '@bussiness_unit__name'}},
                    'attr': {'original': '@bussiness_unit__name', 'k1': 'v1'}
                },
                {
                    'q':None,
                    'title':'操作',
                    'display':1,
                    'text':{'content':'<a href="/server-detail-{n}.html">查看详细</a>','kwargs':{'n':'@id'}},
                    'attr': {'k1': 'v1'}
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
        # 注意这里要json.dumps将其转换为字符串传过去，否则取不到传入的数据. response.__dict__将得到BaseResponse里面的静态属性。
        # views.BaseResponse().__dict__  将返回 {'status': True, 'data': None, 'message': None}
        return HttpResponse(json.dumps(response.__dict__))      

class BusinessView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'business.html')

class BusinessJsonView(View):
    def __init__(self):
        pass
    def get(self,request,*args,**kwargs):
        response=BaseResponse()
        try:
            # 获取显示的列
            table_config=[
                {
                    'q':'id',     #注意这里的q的值hostname必须于数据库里面的表的列名一样，因为后面会直接用这个值去查询数据库
                    'title':'编号',
                    'display':1,
                },
                {
                    'q':'name',
                    'title':'用户组',
                    'display':1,
                },

            ]
            value_list=[]
            for item in table_config:
                # 判断q是否存在，因为有些列比如“操作”列是不需要查询数据库的，所以如果为None则不执行value_list.append
                if item['q']:
                    value_list.append(item['q'])
            # values(*value_list)在查询中传入value_list列表，列表里面是要显示的字段名称
            result=models.BusinessUnit.objects.values(*value_list)
            # 由于返回的是QuerySet类型，并不能像列表一样直接操作，所以需要用list(result)将QuerySet转换为list列表格式
            result=list(result)
            print(result)
            ret={'table_config':table_config,'data_list':result}
            response.data=ret
        except Exception as e:
            response.status=False
            response.message=str(e)

        return HttpResponse(json.dumps(response.__dict__))      #注意这里要json.dumps将其转换为字符串传过去，否则取不到传入的数据