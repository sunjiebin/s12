#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import paramiko

ssh.connect(hostname='10.10.1.1',port=22,username='root',password='123')
'''注意这里只能输出一次性返回的命令，像top之类的命令是不行的'''
stdin,stdout,stderr=ssh.exec_command('ls')
res,err=stdout.read(),stderr.read()
'''三元运算，如果res存在，result则为res的值，如果不存在，则为err的值'''
result=res if res else err

