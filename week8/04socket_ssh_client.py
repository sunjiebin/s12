#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import os,socket
client=socket.socket()
client.connect(('localhost',6900))

while True:
    cmd=input('input your command')
    if len(cmd)==0:continue
    client.send(cmd.encode('utf-8'))
    datalen=client.recv(10240)
    data=client.recv(10240)
    revc_datalen=len(data)
    print('服务器发送长度',datalen)
    print('客户端收到的长度',revc_datalen)
    print(data.decode())

client.close()