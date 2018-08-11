#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import paramiko

transport=paramiko.Transport(('hostname',22))
transport.connect(username='root',password='123')
sftp=paramiko.SFTPClient.from_transport(transport)
#将Local.py上传至服务器/tmp/test.py
sftp.put('/tmp/local.py','/tmp/test.py')
#将remove_path下载到本地local_path
sftp.get('remove_path','local_path')
transport.close()