#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''当我们对队列和消息都持久化之后，当rabbitmq出现问题停止或重启后，能够保证数据不丢失，
默认情况下消息是存在内存里面的，重启进程队列就丢失了
注意队列和消息都要持久化，如果只对列持久化durable，那么队列名称重启后依然存在，但消息没
有了，那是没有意义的'''
'''可以手动重启rabbitmq的服务来模拟故障重启'''
import pika
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel() #声明一个管道
channel.queue_declare(queue='hello2',durable=True)    #durable队列持久化
channel.basic_publish(exchange='',routing_key='hello2',body='my god!',
                      properties=pika.BasicProperties(delivery_mode=2,))    #delivery_mode=2消息持久化
print('body send')
connection.close()
