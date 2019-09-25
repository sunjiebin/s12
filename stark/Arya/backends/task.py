#!/usr/bin/env python3
# Auther: sunjb
import pika,json

class TaskHandle(object):
    '''
    用于生成以及处理消息
    被state.py里面的apply方法调用
    '''
    def __init__(self,db_model,task_data,settings,module_obj):
        self.db_model=db_model
        self.task_data=task_data
        self.settings=settings
        # new_task_obj = TaskHandle(self.db_models, self.config_data_dic, self.settings, self) 所有module_obj就是self，也就是State()实例
        # module_obj就是调用TaskHandle的实例本身，谁调用了TaskHandle，module_obj就是水。State()类调用了TaskHandle，那么module_obj=Stata实例
        self.modulle_obj=module_obj
        self.make_connection()
    def apply_new_task(self):
        '''在数据库里面创建任务记录并返回任务Id'''
        # 每一次调用都生成一个新的id插入到这个表里面，因为id是自增的，这样就实现了task_id自增，不会重复
        new_task_obj=self.db_model.Task()
        new_task_obj.save()
        self.task_id=new_task_obj.id
        return True

    def dispatch_task(self):
        '''任务格式化,调用发送函数发送消息'''
        # 当任务处理完成后，会返回数据到一个队列，服务的监听这个队列，获取到返回的数据
        if self.apply_new_task():
            print('send task to:',self.modulle_obj.host_list)
            #生成消息队列名称，每次调用都是不同的id
            self.callback_queue_name="TASK_CALLBACK_%s"%self.task_id
            print('callback_queue_name:',self.callback_queue_name)
            data={
                'data':self.task_data,
                'id':self.task_id,  #这个task_id就是数据库task表里面的自增id
                'callback_queue':self.callback_queue_name,
                'token':None
            }
            print('data:',self.task_data)
            # 给每一个匹配到的主机发送消息
            for host in self.modulle_obj.host_list:
                self.publish(data,host)
            #等待任务结果
            self.wait_callback()

    def make_connection(self):
        '''创建mq链接'''
        # 将mq的链接参数配置在setting.py里面了
        # self.mq_conn=pika.BlockingConnection(pika.ConnectionParameters(self.settings.MQ_CONN['host']))
        # self.mq_channel=self.mq_conn.channel()

        credentails=pika.PlainCredentials(self.settings.MQ_CONN['user'],self.settings.MQ_CONN['pass'])
        self.mq_conn=pika.BlockingConnection(pika.ConnectionParameters(
            self.settings.MQ_CONN['host'],
            self.settings.MQ_CONN['port'],self.settings.MQ_CONN['vhost'],credentails
        ))
        self.mq_channel=self.mq_conn.channel()

    def publish(self,task_data,host):
        '''发送消息'''
        print('发布消息')
        queue_name='TASK_Q_%s'%host.id
        #创建queue
        self.mq_channel.queue_declare(queue=queue_name)
        print('消息内容',json.dumps(task_data).encode())
        # 发送queue，routing_key代表将消息发送到那个队列，body代表发送的内容
        self.mq_channel.basic_publish(exchange='',routing_key=queue_name,body=json.dumps(task_data))
        print(f'发送task to queue {queue_name}')

    def close_connection(self):
        '''关闭队列'''
        self.mq_conn.close()

    def task_callback(self,ch,method,properties,body):  #ch管道内存对象地址，method指定各项参数
        print(body)

    def wait_callback(self):
        '''消费消息，监听队列，等待新消息'''
        # 声明一个队列,这个队列要和发送发指定的一致，一个发，一个收
        self.mq_channel.queue_declare(self.callback_queue_name)
        # 定义消费消息的参数，self.task_callback代表接收到消息后的回调函数，self.callback_queue_name代表从这个queue里面接收消息，False不发送ack确认给服务端
        self.mq_channel.basic_consume(self.callback_queue_name,self.task_callback,False)
        # 下面的写法时老版本的Pika的写法
        # 定义消费消息的参数，self.task_callback代表接收到消息后的回调函数，quque代表从这个queue里面接收消息，no_ack=True不发送ack确认给服务端
        # self.mq_channel.basic_consume(self.task_callback,queue=self.callback_queue_name,no_ack=True)
        print('等待callback')
        # 开始监听消息，如果没有消息则挂起，有则执行上面self.mq_channel.basic_consume定义的操作
        self.mq_channel.start_consuming()

