#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import pika
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel() #声明一个管道
channel.queue_declare(queue='hello')    #声明一个queue,相当于队列名称
channel.basic_publish(exchange='',routing_key='hello',body='my god!')
print('body send')
connection.close()
