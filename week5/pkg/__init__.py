#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
print('this is a package')
aa='aa'

'''在一个包里面调用其它的函数，要在__init__.py
文件里面导入这些模块，不能用其它文件直接导入该目录下的
模块'''

from . import pkg_module