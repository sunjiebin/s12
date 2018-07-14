#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
school='qinghua'
name='aa'
#局部变量，函数体里面的变量默认都是局部变量
def change_name(name):
        print('before name %s'%name)
        name='SUN'  #在函数里面改变了name变量的值
        print('after name')

change_name('sun')
#执行函数后，再看看name变量结果没有被函数改变，证明不是全局变量
print(name)

'''全局变量
定义在代码第一层级的都是全局变量
在函数里面如果要定义全局变量，就要用global来申明
注意不建议在函数里面定义全局变量，因为在程序复杂时，调用的函数会非常多，
如果在函数里面定义了全局变量，到时候排查问题的时候会非常麻烦，不知道变量是从哪个函数里面定义的'''
def global_name():
    global school
    school='qingniao'
global_name()
#在函数中运行后，发现函数外的变量也被改变
print(school)

'''注意全局变量与局部变量只针对字符串和数字生效
对于列表等是不生效的'''
alist=[1,2,'a']
def test():
    alist.append(5)
    alist[1]='aa'

test()
print(alist)