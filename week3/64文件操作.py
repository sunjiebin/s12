#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
aa=open('aa.txt','w')
aa.write('你好fkjld\nsdflkjd\rlkjdf')
aa.close()
#rU r+U 用于自动将\r\n转换为\r,解决windows和linux下换行符转换的问题
bb=open('aa.txt','rU')
print(bb.read())
bb.close()
#rb/wb/ab表示处理二进制文件,在ftp传文件是有用,将文件转换为二进制读取.
#read代表读几个字节
cc=open('aa.txt','r')
#read读前面两个字符,而不是字节,这里汉字也是一个字符.
#注意这里和python2不同,python2是读2个字节,而汉子是两个字节组成一个字,所以要read(2)才能读一个汉字.
#读前面两个字
ret=cc.read(2)
print(ret)
#tell查看指针的当前位置
#注意tell却又是按照字节来取的,所以两个汉字在tell显示的指针的位置就是4
print(cc.tell())
#seek指定指针的当前位置
cc.seek(0)
print(cc.tell())
#我们将读取的起始位置定位第三个字节,这时候相当于把第二个汉子读了一半,汉字肯定会乱码.
cc.seek(3)
print(cc.readline())
print(cc.tell())
cc.close()
#truncate清除指定字符后面的内容,只保留前面的内容。
# 这个操作会直接修改文件。所以要用可写的模式执行该命令。默认会从第一个字符开始截取
dd=open('aa.txt','r+')
dd.truncate(5)
print('truncate后的aa.txt值为',dd.read())
#打印文件名
print(dd.name)
#seekable判断文件是否可以移回去
print(dd.seekable())
#判断文件是否可写
print(dd.writable())
print(dd.readable())
dd.close()
#如果只想截取其中一段，而不是从第一个字符开始截取，我们可以先seek到指定位置，再trunate
#w+打开写读模式，当文件不存在时，会新建文件；r+读写；a+追加的同时可读
aa=open('aa.txt','w+',encoding='utf-8')
aa.write("sun jie bin lets go")
print('当前位置为',aa.tell())
aa.seek(0)
print('截取前的内容为',aa.read())
aa.seek(5)
aa.truncate(10)
print('截取后的内容为',aa.read())
aa.close()
#flush将写入的数据立即更新到磁盘，在执行close()时会将内存数据写入磁盘
"""在我们向文件写入数据时，数据并不会实时的落地到硬盘上，而是会先到内存，到一定量后再写入到磁盘,
如果这时候突然断电，就有可能造成写入的数据丢失，flush则强制将内存里面的数据落地到磁盘，对于重要数据
不允许丢失的,比如存钱操作，可以用这个功能。
验证方法：可以先write一个文件，在未close的情况下，用别的工作打开这个文件，会发现write的数据并没有在文件里面，
这时候执行下flush，再打开文件就发现数据已经写入了。
注意encoding加上后，用python写入的文本打开就不会乱码，不然会乱码"""
ee=open('aa.txt','w',encoding='utf-8')
ee.write('sdf')
ee.flush()
#closed判断文件是否关闭
print('文件是否关闭',ee.closed)
ee.close()
print('文件是否关闭',ee.closed)
#可以用下面的方式来验证flush
import sys,time
for i in range(10):
    #sys.stdout.write表示将输入的内容输出到标准输出，即一边输入一边在屏幕显示
    sys.stdout.write('#')
    time.sleep(0.1)
    #当下面行注释时，会在所有#号全写到内存后，再一下子打印出来
    #当执行下面行时，每0.5秒就会打印一个#号，就像vim里面的安装进度条一样
    sys.stdout.flush()

'''在py3里面网络传输全部只能用二进制模式传输，在py2里面还能用字符。  '''
f=open('aa.txt','w')
f.write('sdfsf\nlkjlfkjds\n你好dfkj')
f.close()
#以二进制的方式来打开
a=open('aa.txt','rb')
print(a.read())
a.close()
'''wb二进制写'''
b=open('aa.txt','wb')
'''这里要在后面加上encode()进行转码，将它转成二进制byte类型。
encode()当后面的()为空时，代表用程序默认的编码进行转码，这里默认编码是utf8，
所以就是将前面的字符以utf-8转码为二进制类型。
encode()等同于encode('utf-8')
如果不加这个，就是以字符串类型写，这是写不进的，会报错。'''
b.write('heelo,你df\n'.encode())
b.close()
#这时候文件是以二进制来编码形式来写入的，并不代表文件就是二进制的。所以读出来还是原来的文字
