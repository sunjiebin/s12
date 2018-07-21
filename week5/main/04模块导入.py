#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import os,sys
fatherdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(fatherdir)

'''这时候我们如果要导入base下的东西'''
sys.path.append(fatherdir)
print(sys.path)

'''还可以导入一个包，导入包实际上执行了包里面的__init__.py文件'''
print('导入一个包,包里面的内容在import时已经被执行')
import pkg
#执行导入的包里面的模块功能
pkg.pkg_module.pkg2()