#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
# s14-03-09
'''文件的修改主要包括两种方式，一种就是将文件全部读入内存，然后在内存里面对文件进行修改
修改完成后再写入磁盘，而不是直接对磁盘上的文件进行修改，vim就是这种方式，所以在打开大文件
时，会非常慢，因为要全加载到内存。另一种是将原文件的东西写入到另一个文件里面实现修改，这种
可以一行行读，然后一行行的写入到新文件'''
'''注意在进行write时，要在后面加上encoding，不然写入的中文在pychar中打开是乱码的。
里面aa.txt是没有加encoding的，aa2.txt是加了encoding的，可以对比两者中文的不同'''
file1=open('aa.txt','w')
file1.write('sun jie bin\n 罗小姐姐\n zhang')
file1.close()

f2=open('aa.txt','r')
f3=open('aa2.txt','w+',encoding='utf-8')

#for line in f2.readlines():
'''注意这里直接写f2,并没有写f2.readlines(),其实两者执行的结果是一样的，
但是执行过程是不一样的。直接写f2，那么for循环会一行行的读这个文件去执行，这样对内存的消耗并不大
如果写成f2.readlines()那么代表一下子把整合文件所有行都先加载到内存，再给for去循环，
在小文件时两者没啥区别，但如果读的文件非常大，那么readlines的方式会把机器内存用完，是不可取的'''
for line in f2:
    if "小姐" in line:
        line=line.replace('小姐','大姐')
    f3.write(line)
f3.seek(0)
print(f3.read())
f2.close()
f3.close()


