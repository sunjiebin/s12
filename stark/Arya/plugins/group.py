#!/usr/bin/env python3
# Auther: sunjb

from Arya.backends.base_module import BaseSaltModule


class Group(BaseSaltModule):
    def uid(self,*args,**kwargs):
        pass
    def gid(self,*args,**kwargs):
        pass
    def shell(self,*args,**kwargs):
        pass
    def home(self,*args,**kwargs):
        pass
    def require(self,*args,**kwargs):
        pass
    def present(self,*args,**kwargs):
        pass
    def is_required(self,*args,**kwargs):
        print('is required',args,kwargs)
        cmd=f"id {args[1]};echo $?"
        return cmd


class UbuntuGroup(Group):
    def home(self,*args,**kwargs):
        print('in ubnutn home ')