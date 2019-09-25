#!/usr/bin/env python3
# Auther: sunjb

from Arya.backends.base_module import  BaseSaltModule

class File(BaseSaltModule):
    print('in File class')
    def source(self,*args,**kwargs):
        pass
    def user(self,*args,**kwargs):
        pass
    def group(self,*args,**kwargs):
        pass
    def mode(self,*args,**kwargs):
        pass
    def managed(self,*args,**kwargs):
        print('managed',args,kwargs)
        return kwargs
    def is_required(self,*args,**kwargs):
        print('is required',args,kwargs)
        cmd=f'rpm -qa |grep {args[1]};echo $?'
        return cmd

class WindowsFile(BaseSaltModule):
    print('in WindowsFile class')
    def source(self,*args,**kwargs):
        pass
    def user(self,*args,**kwargs):
        pass
    def group(self,*args,**kwargs):
        pass
    def mode(self,*args,**kwargs):
        pass
    def managed(self,*args,**kwargs):
        print('managed',args,kwargs)
        return kwargs
    def is_required(self,*args,**kwargs):
        print('is required',args,kwargs)
        cmd='pwd'
        return cmd