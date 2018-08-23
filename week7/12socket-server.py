#!/usr/bin/env python3
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
        '''注意if not data这个仅在linux下生效，在windows下，当客户端断开连接时，
        conn.recv直接就会报错了，所以根本不会走到if语句这里，如果要让代码兼容windows,
        建议用try,except的方式来捕获并处理异常,但linux下try方法又不适用
        所以，在windows下用try，在linux下用if not data'''
        if not data:
            print('客户端断开连接')
            break
        #print('recv:',data)
        print('recv:',data.decode())
        conn.send(data.upper())
    conn.close()