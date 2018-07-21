#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''导入模块
用import的方式导入后，在执行时模块里面的功能时，要加上模块名称
'''
print('导入模块，在导入模块时，实际上已经执行了该模块的内容')
'''比如我在module_sun.py里面print了sun，在导入时，这个sun被打印了，
这时候相当于将module_sun.py里面的所有内容，赋值给了变量module_sun'''
import module_sun
#打印模块里面的变量
print('------------')
print(module_sun.name)
#执行模块里面的函数
module_sun.say_hello()

'''还可用from的方式导入模块里面的功能，这时候不用加模块名，
相当于把module_sun里面的代码粘贴在了本脚本里面'''
print('导入模块里面所有方法')
from module_sun import *
'''直接执行模块里面的函数名，不用加模块名称，这种方式并不推荐，
因为如果本脚本里面也有相同的函数名称，那么会冲突，会执行本地的函数。'''
say_hello()

'''为了避免和执行脚本里面的变量冲突，可以用as的方法 ，
将导入的变量重命名为新的名称'''
print('将模块里面的导入变量重新命名')
from module_sun import say_hello as say
def say_hello():
    print('main hello')
say_hello()
#执行导入的模块里面的say_hello
say()
'''导入模块多个函数，这种方式相当于直接读取了module_sun文件里面
指定的函数代码'''
print('导入模块里面的多个变量')
from module_sun import say_hello,say2,name
print(name)
say2()
say_hello()

import os,sys
print('打印系统环境变量搜索路径')
print(sys.path)
print('打印当前文件绝对路径')
print(os.path.abspath(__file__))
print('打印当前文件夹的名称')
print(os.path.dirname(os.path.abspath(__file__)))
fatherdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('打印父级目录名称')
print(fatherdir)

'''跨目录调用
当我们跨目录调用模块时，首先要先知道模块在哪个目录下，
系统默认会根据sys.path的路径去寻找对应的模块名，找不到则报错，
当前目录是在sys.path里面的，所以执行程序当前目录下的py文件是可以
直接找到的。'''
#导入base目录下的test.py
'''首先要把base目录加入到sys.path中去'''
fatherdir2='%s\\base'%(fatherdir)
print(fatherdir2)
'''在这里重新定义sys.path变量时，一定要注意，append是把路径加入
到这个列表的最后面，所以，在对sys.path搜索时，如果前面的路径中已经
包含了相同的模块名称，则会把先找到的模块给加载'''
#sys.path.append(fatherdir)
'''如果我们想让我们自己定义的路径最先加载，那么可以加入到sys.path
列表的最前面'''
sys.path.insert(0,fatherdir2)
print(sys.path)
import test2
test2.mypath()