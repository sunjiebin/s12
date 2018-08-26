#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import pika,time
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
channel.queue_declare(queue='hello')

channel.basic_qos(prefetch_count=1) #开启权重，表示客户端如果有队列未处理完，就不给该客户端分配下一个消息，服务端不用修改代码
def callback(ch,method,properties,body):
    print('开始处理消息',body)
    time.sleep(5)
    print('recived',ch,method,property,body)
    print('消息处理完毕')
    ch.basic_ack(delivery_tag=method.delivery_tag)
'''
ch.basic_ack代表客户端收到消息后返回确认给mq服务端，保证消息不丢失。
如果不返回那么服务端无法得知客户端是否已经收到数据，当客户端在处理
收到的消息时，如果此时客户端出现异常而导致消息并未完全接收，那么作
为服务端是无法得知这个结果的，消息也不会重发，此时该消息就直接丢失了。
当采用默认时，即客户端会返回一个消息确认，那么当消息失败时，mq的服务
端则不会判定消息发送成功，这时候会选择重发消息到其它的接收端，这样就
保证了消息能够被正确消费，而不会丢失。
同一个channel里面，发送端会轮循的发送到各个接收端，与负载均衡类似
'''
'''
no_ack=True时，客户端即使消费了消息，该消息依然是存在的，会导致这个
消息一直存在于服务端，不会被删除
'''
channel.basic_consume(callback,queue='hello')
#下面的方式在消息执行后，消息仍然会存在。
#channel.basic_consume(callback,queue='hello',no_ack=True)
print('waiting for message,block press ctrl+c')
channel.start_consuming()