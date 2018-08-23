#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import selectors,socket

server=socket.socket()
server.bind(('localhost', 6900))
server.listen()
server.setblocking(False)
sel=selectors.DefaultSelector()

def accept(server, mask):
    conn,addr=server.accept()
    print('accept',conn,addr,mask)
    conn.setblocking(False)
    sel.register(conn,selectors.EVENT_READ,read)

def read(conn,mask):
    try:
        data=conn.recv(1024)
        if data:
            print('收到数据',repr(data),conn)
            conn.send(data)
        else:
            print('客户端断开连接',conn)
            sel.unregister(conn)
            conn.close()
    except Exception:
        print('客户端断开连接', conn)
        sel.unregister(conn)
        conn.close()

sel.register(server, selectors.EVENT_READ, accept)


while True:
    events=sel.select()
    print('events',events)
    for key,mask in events:
        callback=key.data
        print('callback',callback)
        callback(key.fileobj,mask)