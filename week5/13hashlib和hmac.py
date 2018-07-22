#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import hashlib
#hashlib主要用于加密
m1=hashlib.md5()
m1.update(b'hello word')
#hexdigest表示用16进制的方式来显示加密的字符串
print(m1.hexdigest())
'''注意这里再次update实际上是对m1进行了拼接，
实际上是对 hello wordhello,girl 进行md5'''
m1.update(b'hello,girl')
print(m1.hexdigest())

#验证上面确实为拼接
m2=hashlib.md5()
m2.update(b'hello wordhello,girl')
#打印m2会发现和第二个m1的值一样
print(m2.hexdigest())

#sha512加密
m3=hashlib.sha512()
m3.update(b'hello word')
print(m3.hexdigest())

'''注意对中文的加密要转码'''
m4=hashlib.sha256()
m4.update('你好'.encode(encoding='utf-8'))
print(m4.hexdigest())

print('hmac测试'.center(50,'#'))
import hmac
'''hmac是双重加密'''
#注意都要用b转码成bytes类型，默认是unicode码不支持加密
'''前面的helo是加密密钥，相当于在hello word上又加了个helo一起加密
相当于加盐的方式'''
h=hmac.new(b'helo',b'hello word')
print(h.hexdigest())
#或者转成utf8
h.update('hi,girl'.encode(encoding='utf-8'))
print(h.hexdigest())

#转成utf8再加密
h2=hmac.new('helo'.encode(encoding='utf-8'),'hello word'.encode(encoding='utf-8'))
print(h2.hexdigest())
#中文不支持byte类型，所以必需转成utf8
h2.update('你好'.encode(encoding='utf-8'))
print(h2.hexdigest())

import re