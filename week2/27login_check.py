#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import sys

lock_file='user.txt'
def deny_account(username):
    print('用户已经被锁定')
    with file(lock_file,'a') as deny_f:
        deny_f.write('\n'+username)
def main():
    retry_count=0
    retry_limit=3
    while retry_count<retry_limit:
        username=raw_input('请输入用户名')
        with file(lock_file,'r') as lock_f:
            for line in lock_f.readlines():
                if username == line.strip():
                    sys.exit('用户%s被锁定'%username)
                if len(username)==0:
                    print ('用户名不能为空')
                    continue
        # username=raw_input('请输入用户名')
        # with file(lock_file,'r') as lockuser:
        #     list = []
        #     for line in lockuser.readlines():
        #         list.append(line.strip())
        #     if username in list:
        #         sys.exit('用户%s已经被锁定'%username)