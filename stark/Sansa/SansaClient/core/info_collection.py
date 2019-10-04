#!/usr/bin/env python3
# Auther: sunjb

import platform
from plugins import plugin_api
class InfoCollection(object):
    def __init__(self):
        pass

    def get_platform(self):
        '''获取操作系统类型'''
        os_platform = platform.system()
        return os_platform

    def collect(self):
        '''根据不同的操作系统类型执行不同的方法'''
        os_platform=self.get_platform()
        print('in collect:',os_platform)
        try:
            func=getattr(self,os_platform)
            info_data=func()
            format_data=self.build_report_data(info_data)
            return format_data
        except AttributeError as e :
            exit('出错了,不支持该系统%s,错误信息%s'%(os_platform,e))

    def Linux(self):
        '''调用linux系统的api脚本,获取操作系统信息'''
        sys_info=plugin_api.LinuxSysInfo()
        return sys_info

    def Windows(self):
        sys_info=plugin_api.WindowsSysInfo()
        # print('in Windows:',sys_info)
        return sys_info

    def build_report_data(self,data):
        '''生成对应的数据'''
        return data