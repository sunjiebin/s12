#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''可以通过Pipe管理实现进程间的通信
调用Pipe后，会传递两个值，在子进程里面
用send发送数据，在父进程里面用recv接收
数据，就可以实现子进程数据传递到父进程了
'''
from multiprocessing import Process,Pipe
def f(conn):
    conn.send([42,None,'test'])
    conn.close()
if __name__ == '__main__':
    parent_conn,child_conn=Pipe()
    p=Process(target=f,args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()