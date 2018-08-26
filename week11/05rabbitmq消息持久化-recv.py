#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import pika,time
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
'''当发送端用durable持久化之后，接收端也要匹配着写上durable方式来接收，
如果不写durable则会报错'''
channel.queue_declare(queue='hello2',durable=True)

def callback(ch,method,properties,body):
    print('开始处理消息',body)
    #time.sleep(20)
    print('recived',ch,method,property,body)
    print('消息处理完毕')

channel.basic_consume(callback,queue='hello2')
#下面的方式在消息执行过程中失败后，不会重发消息。
#channel.basic_consume(callback,queue='hello')
print('waiting for message,block press ctrl+c')
channel.start_consuming()