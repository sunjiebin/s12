#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import os,socket,hashlib

client=socket.socket()
client.connect(('localhost',6969))
while True:
    cmd=input('>>:')
    if len(cmd)==0:
        continue
    if cmd.startswith('get'):
        client.send(cmd.encode())
        server_response=client.recv(1024)
        print('server response',server_response)
        client.send('ready to recv file'.encode())
        file_total_size=int(server_response.decode())
        recive_size=0
        filename=cmd.split()[1]
        f=open(filename+'.new','wb')
        m=hashlib.md5()

        while recive_size<file_total_size:
            if file_total_size-recive_size>1024:
                size=1024
            else:
                size=file_total_size-recive_size
                print('last recv:',size)
            data=client.recv(size)
            recive_size+=len(data)
            m.update(data)
            f.write(data)
            #print(file_total_size,recive_size)
        else:
            new_file_md5=m.hexdigest()
            print('file recv done',recive_size,file_total_size)
            f.close()
            server_file_md5=client.recv(1024)
            print('server file md5:',server_file_md5)
            print('client file md5',new_file_md5)

client.close()
