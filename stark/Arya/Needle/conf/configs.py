#!/usr/bin/env python3
# Auther: sunjb

import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALT_MASTER='localhost'

#文件服务器地址
FILE_SERVER={
    'http':f'{SALT_MASTER.strip()}:8000',
    'salt':SALT_MASTER,
}

FILE_SERVER_BASE_PATH='/salt/file_center'
#数据下载下来后存放目录
FILE_STORE_PATH=f'{BASE_DIR}/var/dowonloads/'
#客户端的id 这个id与self.callback_queue_name="TASK_CALLBACK_%s"%self.task_id要相同，代表客户端到相同的队列里面拿消息
#正确的处理方式应该是这个id由服务端返回给客户端，然后客户端再保存id，而不是写死。因为客户端有很多，不同的客户端id也会不一样
NEEDLE_CLIENT_ID=3

MQ_CONN={
    'host':'localhost',
    'port': 5672,
    'user':'admin',
    'pass':'sunjiebin',
    'vhost':'stark'
}
