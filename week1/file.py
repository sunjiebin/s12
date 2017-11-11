#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''写模式，会将源文件清空'''
a=open('file.txt','w')
a.write('hello,1 line\n')
a.write('hello,2 lines\n')
a.close()

a=open('file.txt', 'r')
for line in a:
    if '1' in line:
        print('this is the first line')
    print(line)
a.close()
'''追加'''
a=open('file.txt','a')
a.write('3lines\n')
a.write('4 lines\n')
a.close()
a=open('file.txt','r')
print(a.read())
'''读写模式，依然会将文件给清除掉，这个模式使用的非常少'''
a=open('file.txt','w+')
a.write('5lines\n')
a.close()
a=open('file.txt','r+')
print(a.read())