#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import socket
server=socket.socket()
server.bind(('localhost',6900))
server.listen()
print('listen...')
'''
注意在windows下，当客户端断开时socket会直接抛出异常，而不是conn.recv为空，
所以要让程序在windows下能够正确处理客户端断开的问题，那么就要用try的方法来
捕获出现的exception异常，并对异常进行处理，以防止程序直接报错退出。
在linux下，当客户端断开时，socket并不会抛出异常，而是conn.recv会接收到一个
空字符串，此时可以通过if判断接收的数据是否为空，如果为空则证明客户端已经断开
'''
while True:
    conn,addr=server.accept()
    print(conn,addr)
    while True:
        '''用try来捕获windows下客户端断开时的异常'''
        try:
            data=conn.recv(1024)
            '''用if来处理linux下客户端断开时的问题'''
            if not data:
                print('客户端断开连接')
                break
            print(data)
            conn.send(data)
        except ConnectionResetError:
            print('客户端断开连接')
            break
        except Exception as e:
            print(e)
            break
conn.close()