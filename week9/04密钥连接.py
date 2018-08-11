#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import paramiko
'''可以用ssh-copy-id来直接将公钥拷贝至服务器'''
#ssh-copy-id "-p22 root@10.10.1.1"

#指定私钥的位置
private_key=paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
#创建ssh对象
ssh=paramiko.SSHClinet()
#允许连接不在know_hosts文件中的主机，即第一次连接不需要确认
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接服务器
ssh.connect(hostname='10.1.1.1',port=2800,username='root',pkey=private_key)
#执行命令
stdin,stdout,stderr=ssh.exec_command('df')