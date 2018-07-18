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
'''用dump/load的另一种写法，
和上面的效果是一样的，只是写法不一样，
下面的写法更常用，更简洁'''
with open('dic','w') as f:
    json.dump(a_dic,f)
'''注意python3这里dump不能是多次，如果多次dump之后，load就会报错,
在python2里面，是可以dump多次的，同时load的时候也要load多次
才行，且要按顺序来load，这样做其实没什么用。所以建议在dump时，
一个文件只dump一次，然后load，再用的时候重新dump。如果要dump
多次，建议每个dump都单独一个文件，就像虚拟机的快照一样，一个
快照一个文件，相互独立'''
 #   json.dump('helo',f)
with open('dic','r') as r:
    print('jsonload的值为：')
    print(json.load(r))


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
