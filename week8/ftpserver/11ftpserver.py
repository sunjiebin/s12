#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import  os,socketserver,json
class MyTcpHandler(socketserver.BaseRequestHandler):
    print('等待客户端连接')
    def put(self, *args):
        '''接收客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic['filename']
        filesize = cmd_dic['size']
        if os.path.isfile(filename):
            f = open(filename + ".new", 'wb')

        else:
            print('file not exist', filename)
            f = open(filename, 'wb')
        self.request.send(b'200,ok')
        recieve_size = 0
        while recieve_size < filesize:
            data = self.request.recv(1024)
            f.write(data)
            recieve_size += len(data)
        else:
            print('file [%s] has uploaded' % filename)
            f.close()

    def handle(self):
        while True:
            try:

                self.data=self.request.recv(1024).strip()
                print("{} wrote".format(self.client_address[0]))
                print(self.data)
                cmd_dic=json.loads(self.data.decode())
                action=cmd_dic['action']
                if hasattr(self,action):
                    func=getattr(self,action)
                    func(cmd_dic)


            except ConnectionResetError as e:
                print('Err',e)
                break
if __name__ == '__main__':
    HOST,PORT='localhost',6900
    server=socketserver.ThreadingTCPServer((HOST,PORT),MyTcpHandler)
    server.serve_forever()

