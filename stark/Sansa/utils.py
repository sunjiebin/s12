#!/usr/bin/env python3
# Auther: sunjb

import time,hashlib,json
from Sansa import models
from django.shortcuts import render,HttpResponse
from stark import settings

from django.core.exceptions import ObjectDoesNotExist

def json_date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d")


def json_datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.strftime("%Y-%m-%d %H:%M:%S")


def gen_token(username,timestamp,token):
    '''对传过来的用户名/时间/token三者进行md5加密,然后取md5值的10-17位
    这个生成密钥的方式需要和客户端的一致,这样才能得出一样的加密结果.
    '''
    token_format = "%s\n%s\n%s" %(username,timestamp,token)
    print('--->token format:[%s]'% token_format)

    obj = hashlib.md5()
    obj.update(token_format.encode())
    return obj.hexdigest()[10:17]


def token_required(func):
    '''
    客户端校验的装饰器
    在执行向服务器汇报资产时,先执行这个装饰器,验证客户端是否合法
    首先从get请求里面拿到客户端发送过来的user/token/timestamp,
    拿到后和服务端的数据库里面的对应用户的token进行对比,如果是一致的,且未超时,
    那么则开始执行真正的函数.
    如果不一致,则返回认证失败
    :param func:
    :return:
    '''
    def wrapper(*args,**kwargs):
        response = {"errors":[]}
        get_args = args[0].GET
        username = get_args.get("user")
        token_md5_from_client = get_args.get("token")
        timestamp = get_args.get("timestamp")
        if not username or not timestamp or not token_md5_from_client:
            response['errors'].append({"auth_failed":"This api requires token authentication!"})
            return HttpResponse(json.dumps(response))
        try:
            user_obj = models.UserProfile.objects.get(email=username)
            token_md5_from_server = gen_token(username,timestamp,user_obj.token)
            if token_md5_from_client != token_md5_from_server:
                response['errors'].append({"auth_failed":"Invalid username or token_id"})
            else:
                if abs(time.time() - int(timestamp)) > settings.Params.get('timeout'):# default timeout 120
                    response['errors'].append({"auth_failed":"The token is expired!"})
                else:
                    pass #print "\033[31;1mPass authentication\033[0m"

                print("\033[41;1m;%s ---client:%s\033[0m" %(time.time(),timestamp), time.time() - int(timestamp))
        except ObjectDoesNotExist as e:
            response['errors'].append({"auth_failed":"Invalid username or token_id"})
        if response['errors']:
            return HttpResponse(json.dumps(response))
        else:
            return  func(*args,**kwargs)
    return wrapper



