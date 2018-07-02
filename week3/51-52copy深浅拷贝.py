#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import copy
a1='abcede'
a2=a1
a3=copy.copy(a1)
print(a1,a2,a3)
print(id(a1),id(a2),id(a3))
#将a1重装赋值
a1='dsfklj'
#可看到a1变了，其它没变
print(a1,a2,a3)
#查看内存地址，a1指向了其它地址
print(id(a1),id(a2),id(a3))

#列表、元组、字典则不一样了
n1={'k2': 123, 'k1': 'wu', 'k3': ['alex', 45]}
n2=n1
n3=copy.copy(n1)
n4=copy.deepcopy(n1)
print(n1,n2,n3,n4)
#这里就能看到n2和n1是指向的同一个内存地址，n3由于是拷贝的，指向了不同的地址
print(id(n1),id(n2),id(n3),id(n4))
#查看里面的k3的地址,发现n3都是一样的，n4则不一样，也就是浅拷贝只拷贝了第一层，而深拷贝则连下一层也拷贝了
print(id(n1.get('k3')),id(n2.get('k3')),id(n3.get('k3')),id(n4.get('k3')))
#改变n1第一层的值
n1['k2']='abc'
#这时候可看到n3,n4并没有跟随着n1而改变
print(n1,n2,n3,n4)
#改变n1内嵌的k3列表里面的值
n1['k3'][0]='sun'
#再次打印发现n1-n3都变成sun了，n4没变
#因为n3的内存地址并没有改变，所以对嵌套的列表进行修改时，还是读的同一块内存区域
print(n1,n2,n3,n4)

#实际用就示例，比如要建立监控模块，可以用到这个功能
dic = {
    'cpu':[70,80,],
    'mem':[70,90,],
    'disk':[80,90,]
}
print(dic)
dic1=copy.copy(dic)
dic2=copy.deepcopy(dic)
dic['cpu'][1]=90
print('改变后',dic)
print('浅copy',dic1)
print('深copy',dic2)