#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

def bar():
    print('in the bar!')
#定义一个高阶函数test
def test(func):
    print('test1返回值',func)
    func()
#在执行test函数时，在变量里面引用函数
test(bar)

'''以上过程相当于
func=bar
func()
这相当于变量的相互引用一样'''

'''定义一个返回值调用的函数'''
def test2(func):
    print('test2返回值 %s'%func)
    return func
print('执行test2并打印返回值'.center(50,'+'))
print(test2(bar))
print('重新定义bar'.center(50,'+'))
bar=test2(bar)
print('执行新定义的bar'.center(50,'+'))
bar()

'''函数的嵌套，注意每级嵌套函数都要有调用
如果去掉dad()的调用，则函数实际不会执行任何操作
'''
def grandpa():
    x=1
    def dad():
        x=2
        def son():
            x=3
            print(x)
        son()
    dad()
grandpa()

print('执行下一个函数'.center(50,'+'))


def test3(func):
    print('this is test3')
    return func


test3(bar)()








