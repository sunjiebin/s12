from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

#
class row1(MiddlewareMixin):
    #process_request,process_response的名称是固定的，用于接收和返回，不能随意修改
    # request，response参数顺序不要弄反了，request得在前面
    # request里面包含了请求包含的所有东西
    def process_request(self,request):
        print('中间件1')
    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print('第二层1')
    def process_response(self,request,response):
        print('返回1')
        return response

class row2(MiddlewareMixin):
    def process_request(self,request):
        print('中间件2')
        # 在这里返回return后，则中间件在这里就已经返回了，不会再进行到下一个中间件
        #return HttpResponse('走吧')
    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print('第二层2')
        #return HttpResponse('到此为止')
    def process_response(self,request,response):
        print('返回2')
        return response

class row3(MiddlewareMixin):
    # 第一次进来走request
    def process_request(self, request):
        print('中间件3')
        # return HttpResponse('走你3')
    # 从url返回后再进入process_view
    def process_view(self,request,view_func,view_func_args,view_func_kwargs):
        print('第二层3')
        #return HttpResponse('boom')
    # 进入函数后再返回走response
    def process_response(self, request, response):
        print('返回3')
        return response
    # 出现异常后走exception
    # def process_exception(self,request,exception):
    #     # 如果exception是ValueError类型。isinstance用于判断对象类型。如isinstance(aa,str) 判断aa变量是否为str类型
    #     if isinstance(exception,ValueError):
    #         print('值错误',request,exception)
    #     elif isinstance(exception,TypeError):
    #         print('类型错误',request,exception)
    #     return HttpResponse('程序有错误')