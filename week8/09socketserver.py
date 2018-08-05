#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import  socketserver
class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                self.data=self.request.recv(1024).strip()
                print("{} wrote".format(self.client_address[0]))
                print(self.data)
                self.request.send(self.data.lower())
            except ConnectionResetError as e:
                print('Err',e)
                break
if __name__ == '__main__':
    HOST,PORT='localhost',6900
    '''TCPServer是单线程的，即同时只能处理一个请求，一个客户端连接后，其它连接就
    是挂起的状态，得等那个连接断开后，才会到下一个连接'''
 #   server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
    '''ForkingTCPServer是开启多进程，和下面的线程类似，只适用于linux，因为windows
    没有os.fork功能'''
  #  server=socketserver.ForkingTCPServer((HOST,PORT),MyTcpHandler)
    '''ThreadingTCPServer是多线程，可以同时处理多个连接'''
    server=socketserver.ThreadingTCPServer((HOST,PORT),MyTcpHandler)
    server.serve_forever()