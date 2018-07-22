#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import configparser

config=configparser.ConfigParser()
'''生成配置文件'''
config['DEFAULT']={'server':'127.0.0.1',
                   'compression':'yes',
                   'compressionLevel':'9'}
config['DEFAULT']['ForwardX11']='yes'
config['bucket.org']={}
config['bucket.org']['user']='hg'

config['topsecrt.server.com']={}
topsecrt=config['topsecrt.server.com']
topsecrt['HostPort']='5022'
topsecrt['ForwardX11']='no'

with open('example.ini','w') as i:
    config.write(i)


'''读配置文件'''
config.read('example.ini')
#将DEFAULT标签里面的配置读出来
print(config.defaults())
#读取标签名，除DEFAULT之外
print(config.sections())
#读取指定sections下面的user的值
print(config['bucket.org']['user'])
print(config['DEFAULT']['server'])
port=config['topsecrt.server.com']
print(port['hostport'])

#判断是否存在标签名
print('bucket.org' in config)
print('hg' in config['bucket.org']['user'])
print('hg' in config['DEFAULT']['server'])


'''修改配置文件'''
#删除bucket.org这个标签及内容
sec=config.remove_section('bucket.org')
config.write(open('example.ini','w'))
#增加bucket2.org
config.add_section('sun.org')
config['sun.org']['age']='30'
config.write(open('example.ini','w'))
