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

#08-08章节
print('一个真正的装饰器'.center(50,'+'))
def test5(func):
    def test4():
        print('this is test4')
        func()
    return test4


'''
在test6函数上面加上@test5，代表test5是一个装饰器，
相当于执行了test6=test5(test6)这个操作
'''
@test5
def test6():
    print('this is test6')

'''下面的语句执行后，相当于上面的@test5，但要注意
@test5是写在test6函数上面的，而下面的test6=test5(test6)
要写在test6函数下面，否则会报错'''
#test6=test5(test6)
test6()

def test8(func):
    def test7():
        print('test7')
        func()
    return test7
bar=test8(bar)
bar()
