#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import os,zipfile,re,shutil,stat

def targz(dirname):
    file_list=os.walk(dirname)
    for root,dir,file in file_list:
        os.chdir(root)
        for i in file:
            print(i)
            abs_file=os.path.join(root,i)
            zip_file=zipfile.ZipFile('%s.zip'%(i),'w')
            zip_file.write(i)
            zip_file.close()

targz(r'L:\ra\s12')

def rmfile(dirname):
    file_list=os.walk(dirname)
    for root,dirname,file in file_list:
        os.chdir(root)
        for i in dirname:
            #print(root,dirname)
            print(i)
            aa=re.search('\..+',i)
            if aa is None:
                print(i)
            else:
                print('发现隐藏文件')
                os.chmod(i, stat.S_IWRITE)
                shutil.rmtree(i)
#rmfile(r'L:\ra\s12')