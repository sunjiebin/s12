#!/usr/bin/env python
print('下面是strip的用法')
'''strip默认去掉前后空格'''
a=' hello  '.strip()
print(a)

'''lstrip去掉左边空格,rstrip去掉右边空格'''
a='   hello '.lstrip()
print(a)

''''strip还可以去掉指定字符'''
a='wang hello laowang'.strip('wang')

