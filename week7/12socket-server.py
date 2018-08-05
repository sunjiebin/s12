#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import socket
server=socket.socket()
server.bind(('localhost',6900))
server.listen()
print('开始等电话')
while True:

    # conn就是客户端连过来后，在服务器端为其生成的一个实例
    conn, addr = server.accept()
    print(conn, addr)
    print('电话来了')

    while True:
        data=conn.recv(1024)
        if not data:break
        #print('recv:',data)
        print('recv:',data.decode())
        conn.send(data.upper())
server.close()