#!/usr/bin/env python3
# Auther: sunjb

import os,sys,platform

'''
if platform.system()=='Windows':
    #获取父级目录的上级目录,这里就是指获取SansaClient目录,并赋值给BASE_DIR
    BASE_DIR='\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
    print(BASE_DIR)
else:
    BASE_DIR='/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
'''
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

from core import HouseStark

if __name__ == '__main__':
    HouseStark.ArgvHandler(sys.argv)