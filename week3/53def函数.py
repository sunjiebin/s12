#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#函数会让代码更简洁，提高代码的重用性
#def代表定义函数，程序在遇到def时，不会执行里面的代码，而是把定义的这段代码放入内存，以备调用
#这时候下面定义的mail会被放入内存，变量名称就是mail
#()代表里面可以加参数  ：代表这是一个模块。
def mail():
    num=123
    num+=2
    print(num)
#执行函数mail
mail()
#可以让f引用mail，结果和执行mail一样
f=mail
f()

#return可以指定函数的返回值,返回值可以接收各种类型，当返回多个值的时候，会将返回的值装到一个元组里面
#try的功能是如果try里面的代码有执行失败的，就会进入到except里面执行
#即try里面的代码要是有错误，则执行ret=False
def test():
    ret=True
    try:
        num=123
        num+=2
        print(num)
 #       num.__add__(df)
    except Exception:
        ret=False
    return ret
def test2():
    print('测试返回多个return值')
    return 1,'2',['a','b'],{'a':1,'b':2}
x=test2()
print(x)
#执行函数，并将返回值赋值给result
#如果函数里面没有定义return，那么返回值将是None
result=test()
print(result)
if result:
    print('执行成功')
else:
    print('执行失败')

#0054-0055返回值
#return的作用一个是返回值，一个是中断函数的操作
#当函数里面遇到了return后，就会中断执行，后面部分不会执行
def aa():
    print('aa')
    return 0
    print('bb')
#执行上面的函数aa，只会打印aa，而bb则不会打印
aa()

#0056普通参数
#参数，定义行式参数name，简称行参，这个name相当于一个变量
def bb(name):
    print(name)
#执行函数，在形参中填入变量的值sun，即name='sun'，这个sun就叫实参
bb('sun')

#定义多个参数
def cc(n1,n2):
    print(n1)
    print(n2)
#执行cc时，必需给两个参数都赋值，如果少赋值了会报错
cc('sun','jie')

#0057默认参数
#针对上面的问题，我们可以给参数设置默认值，这样执行时就可以不给该参数赋值，而会采用默认值
#要注意默认参数必需放在最后，如果放前面是会报错的
#def dd(a2,a3=5,a1) 这是错误的写法,因为关键参数必须写在位置参数的后面
def dd(a1,a2,a3=5):
    print(a1,a2,a3)
#这里我没有给a3赋值，将采用默认值5
dd(11,22)
#也可以给a3赋值，则会覆盖原来的值
dd(11,22,33)
#执行时也可以指定参数
dd(a2='aa',a1=33,a3='bb')

#0058-0059动态参数
#可以将一个列表、元组等直接输入到参数里面
def ea(arg):
    print(arg,type(arg))
ea([1,2,3,])
#用*可以将输入的参数自动转换为元组，它接收的是位置参数
def ee(*arg):
    print(arg,type(arg))
ee(1,'a',22)
#用**可以将输入的参数转换为字典,它接收的是关键字参数，如a='b'这种
def ff(**arg):
    print(arg,type(arg))
#注意写法为a=b，不是a:b
#错误写法ff(11,22)
ff(n1=123,n2='cc',n3='sun')

#组合使用
def gg(*arg,**kwargs):
    print(arg, type(arg))
    print(kwargs,type(kwargs))
#这时候会自动根据输入的参数转换为对应的类型
#有=号的转换为字典，没有的转为元组
gg(11,22,'ab',a='b',c=22)
#但要注意写法,下面写法会报错
#要根据前面定义的函数的顺序写，前面写arg类型的，后面kwargs类型的
#gg(11,22,'ab',a='b',c=22,5,6)
#gg(a='b',5)

#0060传入字典或列表
#如果用下面的方式来传递，所有的元素会传到第一个参数里面,列表和字典都会成为元组的一个元素
l=[1,2,3]
d={'a1':1,'a2':2}
gg(l,d)
#正确的做法是如下
gg(*l,**d)

#也可以这样组合，将单个参数与多个组合
def aa(x,*bb):
    print(x)
    print(bb)
#执行时会将1赋值给x，将后面的参数赋值给bb，并以元组的方式返回
aa(1,2,3,'a',5)
#注意下面的调用是错误的，因为有关键字，不会被接受
#aa(1,a='b',b='c')

def bb(x,**kwargs):
    print(x)
    print(kwargs)
bb('sun',name='sun',name2='jie')
#错误写法
#bb('sun','jie')

def cc(x,age=18,*args):
    print(x,age,args)
cc('name',1,'sun',2)

def dd(x,age=18,*args,**kwargs):
    print(x,age,args,kwargs)
dd(1,2,3,4,a='b',c='d')
#注意下面的参数传入，*args的位置出现的是c='d'，这个是关键字参数，是不被*arge识别的，所以args会为空
dd('a','b',c='d',d='e')

#0061 lambda写法
#简单函数的简化写法
#hh为函数名称，arg为行参，：号后面接执行的命令，只能一行。并且将执行的结果return出来
hh=lambda arg:arg+1
print(hh(99))
#上面的写法相当于
def hh(arg):
    arg+=1
    return arg
print(hh(99))