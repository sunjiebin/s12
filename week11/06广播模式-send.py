#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import pika
'''广播模式就像收音机一样，广播不停的发，但它不管客户端是否已经启动，如果
发送端先发了消息，而客户端没启动则收不到消息，只有当客户端启动之后才能收到
这之后发来的广播消息，之前的消息是收不到的'''
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel() #声明一个管道
'''fanout为广播模式'''
channel.exchange_declare(exchange='logs',exchange_type='fanout')
message='info:hello'
'''广播模式不需要指定routing_key名称，因为它是发送到所有的queue'''
channel.basic_publish(exchange='logs',routing_key='',body=message)
print('广播成功')

connection.close()