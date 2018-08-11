#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import threading,time

event=threading.Event()
def lighter():
    count=0
    event.set()
    while True:
        if count>5 and count<10:  #改为红灯
            event.clear()  #把标志位清空
            print('\033[41;1mred light...\033[0m')
        elif count>10:
            event.set()     #变绿灯
            print('aa')
            count=0
        else:
            print('\033[42;1mgreen light...\033[0m')
        time.sleep(1)
        count += 1

def car(name):
    while True:
        if event.is_set():  #代表绿灯
            print('%s running'%name)
            time.sleep(1)
        else:
            print('%s wating...'%name)
            #time.sleep(1)
            event.wait()
            print('green light is on start going!')



light=threading.Thread(target=lighter)
light.start()

car1=threading.Thread(target=car,args=('tesla',))
car1.start()