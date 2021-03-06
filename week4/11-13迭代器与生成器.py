#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#给每个生成的值乘以2,用于对列表里面的每个元素进行计算
a=[ i*2 for i  in range(10)]
print(a)
#如给a列表里面的每个元素*2+2
b=[i*2+2 for i in a]
print(b)
#这个功能还能用map来实现
c=map(lambda x:x+10,a)
print(list(c))

#生成一个生成器
'''生成器会将你的计算条件存储在内存中，当你调用时，会调用这个计算方法，
然后依次进行计算，生成器本身并不会将所有结果存入内存，而是用到哪就算到哪，
只生成当前的值，无法跳跃式的取指定位置的值，也无法回退取过去的值
用生成器生成数据量很大的数据时，依然会很快，因为它只是存了一个计算的方法，
并没有将所有数据取出存放。和上面定义列表的方式是不一样的。'''
a=( i*2 for i in range(10))
print(type(a),a)
for i in a:
    print(i)

'''斐波拉契数列
1,1,2,3,5,8....'''
print('斐波拉契'.center(50,'#'))
def aa(num):
    n,a,b=0,0,1
    while n<num:
        print(b)
        a,b=b,a+b #等同于t=(b,a+b) a=t[0],b=t[1]
        '''注意这个写法并不是a=b,b=a+b的意思    
        第一次循环:a=0,b=1-->a=b=1,b=a+b=1+1=2
        第二次循环:a=1,b=2-->a=b=2,b=a+b=2+2=4'''
        #上面的写法相当于t=(b,a+b),a=t[0],b=t[1]
        #第一次循环 a=0,b=1-->a=t[0]=0=1  b=t[1]=0+1=1
        #第二次循环 a=1,b=1-->a=b=1,b=a+b=2
        #第三次循环 a=1,b=2-->a=b=2,b=a+b=1+2=3
        n+=1
aa(10)

'''上面的函数其实也就是实现了一个生成器的类似功能，根据算法不停的推导
生成的值，将上面的print改为yield，就变成了一个生成器
'''

"""
def fib(num):
    n,a,b=0,0,1
    while n<num:
        yield b
        a,b=b,a+b #等同于t=(b,a+b) a=t[0],b=t[1]
        n=n+1
        print('进入第%s次'%n)
        return 'done'
a=fib(10)
print(a)
print(a.__next__())
print(a.__next__())
print('--中间干点别的事--')
print(a.__next__())
'''通过上面的例子，我们可以发现，我们定义的函数每执行一次就会退出函数，
可以反复的进出函数。我们常规的函数都是直接等函数体执行完之后，再进入下
一行代码，这里能够反复在此函数中执行，在函数循环中还可以执行外面的代码'''
print('----接着前面的次数继续for循环----')
for i in a:
    print(i)

#注意生成器的循环次数用完时，再用next执行就会报错了
print(a.__next__())
"""

#用下面的方法捕获异常
print('循环并捕获异常'.center(50,'#'))
#当一个函数有yield的存在时，它就变成了一个生成器了，而不是一个单纯的函数
#return的返回则用来判断执行异常
def fib2(num):
    n,a,b=0,0,1
    while n<num:
        yield b
        a,b=b,a+b #等同于t=(b,a+b) a=t[0],b=t[1]
        n=n+1
        print('进入第%s次'%n)
    return 'dong'
'''一定要注意return的缩进，如果位于while循环体之内写
    return，那么会导致while循环一次就退出了，因为循环
    时遇到了return，则函数体就退出了，所以循环也就中止
    了'''
        #return 'dong'  #写这里是错误的，会让循环失效

g=fib2(5)
# g.__next__()
# g.__next__()
# g.__next__()
# g.__next__()
# g.__next__()
# g.__next__()

while True:
    try:
        x=next(g)
        print(x)
    except StopIteration as e:
        print('当前返回值为',e)
        break

print('生产者和消费者'.center(50,'#'))
#send和next都可以调用生成器，但是send还可以给yield赋值
import time
def consumer(name):
    print('%s来吃包子啦'%name)
    while True:
        baozi=yield
        print('包子%s来了，被%s吃了！'%(baozi,name))
    return 'done'

'''这里要注意的是dd=consumer('sun)只是让dd变成一个生成器，
此时并不会执行consumer('sun')，因为它已经不是函数了，而只
有在执行next(dd)的时候，生成器才会开始执行'''
dd=consumer('sun')
next(dd)
#注意send不能在第一次调用生成器时就执行，否则会报错。
#第一次必需用next才行。
dd.send('梅菜扣肉包')
dd.send('肉包')

def aa():
    print('与生成器不同，函数在被变量引用时会被执行')
'''注意函数和生成器的不同，在定义a=aa()时，实际上已经执行了
aa()函数，而生成器则不会被执行'''
a=aa()

#循环并行示例
def producer(name):
    c=consumer('A')
    c2=consumer('B')
    c.__next__()
    c2.__next__()
    print('老子准备做包子啦')
    for i in range(1,4):
        time.sleep(1)
        print('每秒做两个，一人一个')
        c.send(i)
        c2.send(i+1)
producer('aa')
'''通过上面的结果看上去就像是两个任务在并行一样，
实际上是单线程'''
