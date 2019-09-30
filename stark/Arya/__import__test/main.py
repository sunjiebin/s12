#!/usr/bin/env python3
# Auther: sunjb
"""
import作用:
    导入/引入一个python标准模块，其中包括.py文件、带有__init__.py文件的目录；
__import__作用:
　　1. 函数功能用于动态的导入模块，主要用于反射或者延迟加载模块。
　　2. __import__(module)相当于import module
    同import语句同样的功能，但__import__是一个函数，并且只接收字符串作为参数，所以它的作用就可想而知了。
    其实import语句就是调用这个函数进行导入工作的，import sys <==>sys = __import__('sys')。

__import__(package.module)相当于from package import name，
如果fromlist不传入值，则返回package对应的模块，
如果fromlist传入值，则返回package.module对应的模块。
"""

print('只导入了archives包')
archives = __import__('archives')
archives.sayHello()
#archives.user.sayHello()   #这样导入时没有user模块的,所以执行会报错

print('导入user模块')
print('不使用fromlist'.center(60,'-'))
print('main2')
f=__import__('archives.user')   #没有加fromlist
print(f)             #这时的f就是archives包
f.sayHello()         #返回archives包（即__init__.py）里面的sayHello()
f.user.sayHello()    #返回user.py里面的sayHello()
#f.role.sayHello()   #会报错，没有导入role模块
print(f.user)

print('使用fromlist'.center(60,'-'))
archives = __import__('archives.user',fromlist = ('user',))
print(archives)         #这时的archives就是user模块
archives.sayHello()     #返回user里面的sayHello()
