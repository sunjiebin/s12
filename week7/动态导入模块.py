#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''默认情况下我们是不能对一个变量或者字符串导入的
import 'lib.aa'  是不可以的
'''
'''importlib用于支持对字符串或者定义的变量导入，这样
当模块名称为变量或字符串时，就可以导入了，官方推荐
用importlib进行动态导入'''
import importlib
Module='lib.aa'
lib=importlib.import_module(Module)
print(lib)
lib.cat('sun').miao()
'''用内置方法__import__也可以动态导入，
但是导入lib.aa，实际上只导入到了lib层，不推荐用'''
lib2=__import__('lib.aa')
print(lib2)
b=lib2.aa.cat('mi')
b.miao()