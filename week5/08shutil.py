#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

# 将week1下的文件打包放置当前程序目录
#先要导入shutil模块
import shutil
'''www为打包后压缩的文件名，不接路径代表当前目录;
zip表示压缩的格式，支持多种压缩格式,root_dir后面接
要压缩的文件夹路径'''
ret = shutil.make_archive('www','zip',root_dir='G:/python学习/s12/week1')

#用tar格式打包到g盘，注意用gztar的格式压缩后，用360压缩打不开
shutil.make_archive('G:/week1','tar',root_dir='G:/python学习/s12/week1')

#拷贝文件内容
shutil.copyfile('08shutil.py','08-copy.py')

#拷贝权限，这个命令好像只在Linux下生效
#shutil.copymode('aa.py','bb.py')

#递归拷贝文件
shutil.copytree('G:/python学习/s12/week1','G:/week1')

#递归删除文件
shutil.rmtree('G:/week1')

#递归移动文件
#shutil.move(src,dst)

'''还可以直接导入zipfile模块来进行压缩和解压，这对于压缩单个文件可以用'''
#将08shutilpy和08-copy.py压缩到zipfile.zip
import zipfile
z=zipfile.ZipFile('zipfile.zip','w')
z.write('08shutil.py')
z.write('08-copy.py')
z.close()

#解压文件
z=zipfile.ZipFile('zipfile.zip','r')
z.extractall()
z.close()

#同样的tarfile模块可以用来压缩和解压