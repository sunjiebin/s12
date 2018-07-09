#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
def fill(args):
    print(('%s测试区间'%args).center(20, '~'))
#all
#只要有一个条件为假，则为假
#False,None,0,''都为假
fill('all')
print(all([5,2,0]))
print(all(['',2,'a']))
print(all([None,2,'a']))
print(all(((1,'a',2))))
#注意空列表返回true
print(all([]))

#any
#只要有一个元素为真，则返回真
fill('any')
print(any({'a',None,'',False}))
print(any({0,None,'',False}))

#bool
#判断元素真假
fill('bool')
print(bool(None))
print(bool(False))
print(bool(0))
print(bool(''))
print(bool([1,2,0]))

#bin
#转换为二进制
fill('bin')
print(bin(128))

#bytearray
#转换为字节数组
fill('bytearray')
print(bytearray('test',encoding='utf-8'))
print(bytearray('你好',encoding='gbk'))
#bytes转换为字节字符串形式
print(bytes('你好',encoding='utf8'))

#callable
#判断是否可被调用
fill('callable')
b='aa'
print(callable(b))
print(callable(tuple))

#chr
#将数字转换为ascii码，可配合random生成随机字符
import random
fill('chr和ord')
print(chr(10),chr(1024),chr(50),chr(97))
for i in range(10):
    num=random.randint(99,130)
    print(chr(num))
#ord
#将字母转为数字
print(ord('a'))
print(ord('~'))

#enumerate
#给列表、字典、元组生成排序序号
fill('enumerate')
aa=list([1,2,3,'a'])
bb={1,2,3,4}
cc=((1,'a','b'))
#默认生成的结果不能直接显示，需要用tuple/set/list等转成可读类型
print(tuple(enumerate(cc,1)))
print(set(enumerate(cc)))
for i in enumerate(cc,10):  #10代表从10开始排序
    print(i)

#eval
#将字符串转换为有效表达式
'''当我们用input接收到一个字典、列表等输入时，
默认传进来的都是字符串型，这时候eval转义就会很有用'''
fill('eval')
aa='[1,2,3]'
bb="{'aa':'bb','k2':'a2'}"
print(type(aa))
print(type(eval(aa)))
print(type(eval(bb)))

#split
#分割字符
fill('split')
aa="it's a dog"
print(aa.split("'")[0])
print(aa.split('a'))

#map 映射
'''
用于批量处理列表生成新的列表、元组、集合等,
map会将函数的返回值输入到新的变量中，如果没
有定义返回值，则会将默认返回值None输出，map
是原变量有多少个元素，输出就有多少个元素，一个
也不会少
'''
fill('map')
a=[1,2,3,4,5]
add=lambda a:a+100
def  func(aa):
    if aa>3:
        return aa+100
    return aa-100
b=list(map(add,a))
c=list(map(func,a))
print(b)
print(c)

#filter 过滤
'''
用于对列表、元组等进行批量的过滤,
会根据函数的过滤条件，将函数中返回True
的结果输出到新的变量中，注意这里不是取函数
的返回值,而是取原变量里面的元素。filter后的
新变量元素可能会变少，因为不符合条件的将被过滤
'''
fill('filter')
a={'a',2,'3',4,'sun'}
def func(aa):
    if type(aa) is str:
        try:
            int(aa)
            return True
        except:
            return False
b=set(filter(func,a))
c=tuple(filter(func,a))
print(b,c)

#format
'''占位符'''
fill('format')
print('aa {}'.format('is dog'))
aa='{1} name is {0}'
print(aa.format('sun','my'))

fill('二八十进制转换')
#oct 八进制
print(oct(10))
#hex 十六进制
print(hex(10))
#bin 二进制
print(bin(10))

#max 取最大值，只能对数字有效
#min 取最小值
fill('max and min')
aa=[5,8,33,3.8,0,-1000.2,2**8]
print(max(aa))
print(min(aa))

#range
fill('range')
a=list(range(5,10))
print(a)

#round 四舍五入
print(round(5.8))
print(round(-102.2))

#sort 只对列表排序,只能对数字,会改变原列表
#sorted 也是排序，但不仅仅只对列表，不改变原列表
aa=[522,3,-222,2.8]
print(sorted(aa))
print(aa)
print(aa.sort(reverse=True))
print(aa)

#zip 对多个列表/字典/元组等根据顺序依次合并成一个个元组
#当每个变量里面的元素量不一样时，会取最少的那一个来输出
fill(zip)
aa=[1,2,22,'ab']
bb=['cc','d','a1',5,3]
cc={2,3,88}
dd=(('a',11,33,44))
print(list(zip(aa,bb,cc,dd)))
print(set(zip(aa,bb)))