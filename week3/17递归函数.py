#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''递归函数：函数自己调用自己一直循环，就是递归函数
在return返回值中可以接函数，可以重复调用自己形成递归
递归函数有三个特性1，必需有明确的结束条件，否则会无限循环，
有把系统资源耗尽的风险；2，条件范围应每次循环不停的在缩小；
3，递归的效率比较低，递归过多会导致栈溢出，系统默认最大999次递归
'''

def func(n):
    print(n)
    n=n/2
    if n//2 >0:
        return func(n)
    print('最后一位数为',n)
func(10)

#注意下面的函数和上面函数是有区别的，下面函数会多返回一个1.25
def func2(n):
    print(n)
    if n//2>0:
        return func2(n/2)
    print(n)
func2(10)

