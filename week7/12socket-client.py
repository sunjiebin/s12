#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import socket

client=socket.socket()
client.connect(('localhost',6900))
while True:
    '''如果传英文，要转成二进制的方式传输，前面要加上b
    如果前面加b，则只能传ascii码里面的字符，即只能传英文'''
    #client.send(b'hello word!')
    '''传中文时，用encode转成utf-8形式，然后它会再把中文转成byte
    类型的发送过去，用encode的方式不管中文还是英文都适用'''
    senddata=input('>>:').strip()
    #如果输入的是空，则重新循环
    if len(senddata) ==0:continue
    client.send(senddata.encode('utf-8'))
    data=client.recv(1024)
    '''接收到的中文要解码成unicode，不然收到的是b开头的byte类型。'''
    print('recv:',data.decode())
client.close()