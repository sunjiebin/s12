#!/usr/bin/env python3
# Auther: sunjb

from Arya.backends.base_module import  BaseSaltModule

class Pkg(BaseSaltModule):
    print('in PKG class')
    def pkgs(self,*args,**kwargs):
        print('in pkg.py pkgs')
        print(args[0],kwargs)
        cmd=' '.join(args[0])
        print(cmd)
        self.raw_cmds.extend(args[0])

    def installed(self,*args,**kwargs):
        print('in pkg installed module')
        cmd_list=[]
        self.raw_cmds.insert(0,'yum install -y')
        print(self.raw_cmds)
        cmd=' '.join(self.raw_cmds)
        cmd_list.append(cmd)
        return cmd_list

    def is_required(self,*args,**kwargs):
        print('is required',args,kwargs)
        cmd=f'rpm -qa |grep {args[1]}'
        return cmd

    # def process(self):
    #     print('cmd process')

class WindowsPkg(BaseSaltModule):
    def is_required(self,*args,**kwargs):
        print('WindowsPkg is required',args,kwargs)
        cmd=f'netstat -tnao |findstr 5672'
        return cmd