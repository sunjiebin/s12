from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

#
class row1(MiddlewareMixin):
    #process_request,process_response的名称是固定的，用于接收和返回，不能随意修改
    # request，response参数顺序不要弄反了，request得在前面
    # request里面包含了请求包含的所有东西
    def process_request(self,request):
        print('中间件1')
    def process_response(self,request,response):
        print('返回1')
        return response

class row2(MiddlewareMixin):
    def process_request(self,request):
        print('中间件2')
        # 在这里返回return后，则中间件在这里就已经返回了，不会再进行到下一个中间件
        return HttpResponse('走吧')
    def process_response(self,request,response):
        print('返回2')
        return response

class row3(MiddlewareMixin):
    def process_request(self, request):
        print('中间件3')
        return HttpResponse('走你3')

    def process_response(self, request, response):
        print('返回3')
        return response