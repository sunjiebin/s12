#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import socket,os,hashlib,json
class FtpClient(object):
    def __init__(self):
        self.client=socket.socket()
    def help(self):
        msg='''
        useage:
        ls
        pwd
        cd 
        get filename
        put filename
        '''
        print(msg)
    def connect(self,ip,port):
        self.client.connect((ip,port))
    def interactive(self):
        #self.authentication()   #登录认证
        while True:
            cmd = input(">>").strip()
            if len(cmd)==0:continue
            cmd_str=cmd.split()[0]
            if hasattr(self,cmd_str):
                func=getattr(self,cmd_str)
                func(cmd)
            else:
                self.help()
    def put(self,*args):
        cmd_split=args[0].split()
        print(cmd_split,args)
        if len(cmd_split)>1:
            filename=cmd_split[1]
            if os.path.isfile(filename):
                filesize=os.stat(filename).st_size
                msg_dic={
                    "action":'put',
                    "filename":filename,
                    "size":filesize,
                    "Overridden":True
                }
                self.client.send(json.dumps(msg_dic).encode())
                #防止粘包，等服务器确认
                self.client.recv(1024)
                '''这里服务端返回的数据应该具有一定的意义，当客户端发送要Put的数据
                及大小时，服务端应该判断用户磁盘是否满、是否可上传等相关参数，然后
                返回一个状态码，这个状态码可以客户端和服务端同时约定好'''
                f=open(filename,'rb')
                for line in f:
                    self.client.send(line)
                else:
                    print('file send done')
            else:
                print('%s is not exist'%filename)

    def get(self,*args):
        cmd_split = args[0].split()
        if len(cmd_split)>1:
            filename=cmd_split[1]
            msg_dic={
                "action":"get",
                "filename":filename,
                "Overridden":True
            }
            self.client.send(json.dumps(msg_dic).encode())

ftp=FtpClient()
ftp.connect('localhost',6900)
ftp.interactive()
