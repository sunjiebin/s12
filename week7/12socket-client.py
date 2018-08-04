#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import socket

client=socket.socket()
client.connect(('localhost',6900))
#client.send(b'hello word!')
client.send('我要传中文'.encode('utf-8'))
data=client.recv(1024)
print('recv:',data)
client.close()