#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import os,socket,time,hashlib
server=socket.socket()
server.bind(('localhost',6969))
server.listen()
print('listen....')
while True:
    conn,addr=server.accept()
    print('new conn',addr)
    while True:
        data=conn.recv(1024)
        if not data:
            print('客户端无数据')
            break
        cmd,filename=data.decode().split()
        print(filename)
        if os.path.isfile(filename):
            f = open(filename, 'rb')
            m = hashlib.md5()
            file_size=os.path.getsize(filename)
            #os.stat(filename).st_size
            conn.send(str(file_size).encode())
            conn.recv(1024)  #等待客户端回应
            for line in f:
                m.update(line)
                '''读取的时候已经是wb打开，所以传输时不需要再转码'''
                conn.send(line)
            print('file.md5',m.hexdigest())
            f.close()
            conn.send(m.hexdigest().encode())  #send md5
            print('send done')
server.close()
