#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''当我们要存入一个字典时，我们可以用str转换为字符格式再写入，
同样的读取时我们可以用eval再转成字典'''
a_dic={'k': 'a', 'a':1, 2:3}
with open('dic','w') as f,open('dic','r') as r:
    f.write(str(a_dic))
    f.flush()
    print(r.read())
    r.seek(0)
    data=eval(r.read())
    print(data.get('k'))
'''更常用的方法是用json进行序列化
但json序列化只能作用于常用的数据类型，像内存地址
这种东西是不能被序列化的'''
import json
print(a_dic)
with open('dic','w+') as f:
    print(json.dumps(a_dic))  #注意是dumps,不是dump
    f.write(json.dumps(a_dic))

with open('dic','r') as r:
    data=json.loads(r.read()) #注意是loads,不是load
    print(data)

import pickle
'''pickle是Python专有的序列化模块，可以序列化各种数据，
如函数的内存地址,pickle生成的数据是不可读的，而且写和读
都要用二进制的方式'''
def aa():
    print('aa')
with  open('dic','wb') as f :
    print(pickle.dumps(aa))
 #   f.write(pickle.dumps(dic))
    f.write(pickle.dumps(aa))
with open('dic','rb') as r:
    print(pickle.loads(r.read()))
'''还可以用load,dump的方式'''
with open('dic','wb+') as f:
    pickle.dump(a_dic, f)
    f.flush()
    f.seek(0)
#    print(f.read())
    print('pickle.load的值为：')
    print(pickle.load(f))
