#!/usr/bin/env python3
# Auther: sunjb

class Asset(object):
    def __init__(self,request):
        self.request=request
        self.mandatory_fields=['sn','asset_id','asset_type']    #强制要求的字段
        self.field_sets = {
            'asset':['manufactory'],
            'server':['model','cpu_count','cpu_core_count','cpu_model','os_type','os_distribution','os_release'],
            'networkdevice':[]
        }
        self.response={
            'error':[],
            'info':[],
            'warning':[]
        }
    def response_msg(self,msg_type,key,msg):
        if self.response.has_key(msg_type):
            self.response[msg_type].append({key:msg})
        else:
            raise ValueError
    def mandatory_check(self,data,only_check_sn=False):
        for field in self.mandatory_fields:
            if not data.has_key(field):
                self.response_msg('error','MandatoryCheckField','The field %s is mandatory and not provided in your reporting data'%(field))

    def data_is_valid(self):
        '''先获取到数据,校验数据'''
        data=self.request