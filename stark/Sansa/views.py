from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#from django.http.response import HttpResponse
import core
import json
# Create your views here.

@csrf_exempt    #csrf免除,因为我们这个post请求没有页面,也就没法传csrf token过去,这里就直接跳过验证
def asset_report(request):
    print(request.GET)
    if request.method == 'POST':
        ass_handler = core.Asset(request)
        if ass_handler.data_is_valid(): #验证数据是否合法
            print('=====asset data valid')
            ass_handler.data_inject()   #如果数据合法就插入进去
        return HttpResponse(json.dumps(ass_handler.response))
    return HttpResponse('----test-----')


#注意对于下面的Post请求我们需要关闭csrf校验,因为我们是直接发送请求到url上面去,所以是没有办法先获取到
#服务器上的csrf_token的,所以如果开启了csrf就会报403没法提交数据了
@csrf_exempt
def asset_with_no_asset_id(request):
    if request.method=='POST':
        print(request.POST)
    return HttpResponse('in asset_with_no_asset_id')
        # ass_handler = core.Asset(request)
        # res=ass_handler.get_asset_id_by_sn()