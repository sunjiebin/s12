#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import pika,time
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
channel.exchange_declare(exchange='logs',exchange_type='fanout')
#定义一个随机的唯一性的queue名称，用于接收广播，在消息接收完后自动销毁
result=channel.queue_declare(exclusive=True)
#获取随机queue的名称
queue_name=result.method.queue
print('随机名称',queue_name)
channel.queue_bind(exchange='logs',queue=queue_name)

channel.basic_qos(prefetch_count=1) #开启权重，表示客户端如果有队列未处理完，就不给该客户端分配下一个消息，服务端不用修改代码
def callback(ch,method,properties,body):
    print('开始处理消息',body)
    time.sleep(5)
    print('recived',ch,method,property,body)
    print('消息处理完毕')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(callback,queue=queue_name)
#下面的方式在消息执行后，消息仍然会存在。
#channel.basic_consume(callback,queue='hello',no_ack=True)
print('waiting for message,block press ctrl+c')
channel.start_consuming()