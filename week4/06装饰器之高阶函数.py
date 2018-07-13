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

#03-10装饰器2
'''传递参数的装饰器'''
'''定义装饰器函数'''
def test9(func):
    def test10(arg2):
        print('this is test10')
        func(arg2)
    return test10
@test9
def test11(arg):
    print('this is test11')
    print('this is %s'%arg)
test11('sun')

'''test11()=test10(),所以,test11(arg)=test10(arg)'''

#同时兼容带参数和不带参数的函数
'''工作中我们要装饰的函数可能是各种各样的,有些要参数,有的又不要
那么如何让装饰器匹配所有的函数呢'''
def test12(func):
    def test13(*args,**kwargs):
        print('this is test13')
        func(*args,**kwargs)
    return test13
#装饰一个不带参数的函数
@test12
def test14():
    print('this is test14')
test14()
#装饰一个带两个参数的函数
@test12
def test15(a,b=2):
    print('%s and %s'%(a,b))
test15('monkey','moon')

#获取原函数返回值
#装饰器返回值的处理
'''当我们对test18用test16装饰器进行进行装饰后，再次执行test18时实际上是在执行test17的函数了,
而此时test18的return值如果不传到test17里面，那么是返回不了的。这时候就需要在test17中将test18
的返回值取出来并赋值给return，这样test17就有了test18传来的返回值，实现返回值的传递'''
user,passwd='sun','jie'
def test16(func):
    def test17(*args,**kwargs):
        print('test17')
        username=input('name:')
        password=input('password:')
        if username == user and password == passwd:
            print('authentiation pass')
            ret=func(*args,**kwargs)
            return (ret)
            '''注意如果用下面的方法定义返回值，虽然会取到返回值，但同时会造成函数重复执行一次
            这个的过程就是先执行一次函数，然后再将函数的返回值赋值给return'''
            #return (func(*args,**kwargs))
        else:
            print('authentication failed')
    return test17
@test16
def test18(a,b):
    print('{} is {}'.format(a,b))
    return 'return pass'
aa=test18('sun','dog')
print(aa)