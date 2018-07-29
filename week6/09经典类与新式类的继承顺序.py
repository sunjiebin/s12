#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''
d先继承b，再继承c；b继承e，c继承a
1、当d自己有构造函数时，则不会执行bc的构造函数
2、当d没有时，则先找b，再找c。
3、当bc都没有时，再由B来找它的继承，即e
4、当bc都没有时，且b本身也没有继承谁时，再由C来找它的继承
这叫广度优先算法，python3都是用这种算法
python2中，对于经典类，采用深度优先算法，对于新式类，采用广度优先算法
'''

class A(object):
    def __init__(self):
        print("A")
class E(object):
    def __init__(self):
        print('E')
class B(E):
    pass
#   def __init__(self):
#         print("B")
class C(A):
    pass
    # def __init__(self):
    #     print("C")
class D(B,C):
    pass
 #   def __init__(self):
 #       print("D")


obj = D()

