#!/usr/bin/env python3
# Auther: sunjb

from Arya.backends.base_module import  BaseSaltModule

class Pkg(BaseSaltModule):
    print('in PKG class')


    def is_required(self,*args,**kwargs):
        print('is required',args,kwargs)
        cmd=f'rpm -qa |grep {args[1]};echo $?'
        return cmd

    # def process(self):
    #     print('cmd process')

class WindowsPkg(BaseSaltModule):
    def is_required(self,*args,**kwargs):
        print('WindowsPkg is required',args,kwargs)
        cmd=f'netstat -tnao |findstr 5672'
        return cmd