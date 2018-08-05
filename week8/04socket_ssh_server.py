#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import socket,os
server=socket.socket()
server.bind(('localhost',6900))
server.listen(10)
print('开始听电话')
conn, addr = server.accept()
while True:

    print(conn,addr)
    bytes_data=conn.recv(10240)
    data=bytes_data.decode()
    if not data:print('连接已断开')
    print(data)
    senddata=os.popen(data).read()
    #print(senddata)
    datalen=len(senddata)
    print(datalen)
    '''不能直接传输数字，要转成字符，字符不能直接传，转为字符后要转码才能发送'''
    datalen_bytes=str(datalen).encode('utf-8')
    conn.send(datalen_bytes)
    print(datalen_bytes)
    conn.send(senddata.encode())
    print(senddata.encode())

server.close()