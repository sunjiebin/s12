from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#from django.http.response import HttpResponse
from Sansa import core,models
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
    return HttpResponse('----asset_report-----')


#注意对于下面的Post请求我们需要关闭csrf校验,因为我们是直接发送请求到url上面去,所以是没有办法先获取到
#服务器上的csrf_token的,所以如果开启了csrf就会报403没法提交数据了
@csrf_exempt
def asset_with_no_asset_id(request):
    if request.method=='POST':
        print(request.POST)
        ass_handler = core.Asset(request)
        res=ass_handler.get_asset_id_by_sn()
        print(res)
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponse('in asset_with_no_asset_id with get method')

def new_assets_approval(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        print('request.POST:',request.POST)
        approved_asset_list = request.POST.getlist('approved_asset_list')   #来源于html里面的select隐藏标签
        approved_asset_list = models.NewAssetApprovalZone.objects.filter(id__in=approved_asset_list)    #拿到数据库里面待批准的数据

        response_dic = {}
        for obj in approved_asset_list:
            request.POST['asset_data'] = obj.data   #设置一个键值,后面的data_is_valid_without_id会用到.
            ass_handler = core.Asset(request)   #所有跟资产相关的都会调用这个类,创建/更新/删除资产都在这里面
            if ass_handler.data_is_valid_without_id():
                ass_handler.data_inject()
                obj.approved = True
                obj.save()

            response_dic[obj.id] = ass_handler.response
        return render(request, 'assets/new_assets_approval.html',
                      {'new_assets': approved_asset_list, 'response_dic': response_dic})
    else:
        ids = request.GET.get('ids')
        id_list = ids.split(',')
        new_assets = models.NewAssetApprovalZone.objects.filter(id__in=id_list)
        return render(request, 'assets/new_assets_approval.html', {'new_assets': new_assets})