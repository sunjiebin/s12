#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

with open('aa.txt','r') as f:
    for i in f:
        print(i)

#下面的代码在读取aa2.txt时会报编码错误
# with open('aa.txt','r') as f, \
#      open('aa2.txt','r') as j:
#     print(f.readlines())    #用readlines读出来的是列表形式
#     print(j.readlines())    #当里面的中文编码不对时，这里会报错
'''为什么读aa.txt没报错，读aa2.txt时会报错?原因在于我们写入aa2.txt时，用了encoding='utf-8'，这时候会用utf8进行编码，
在我们读的时候，又没有指定编码，那么系统会用默认的编码来读取该文件，在windows下默认的编码是gbk，所以当用gbk读utf-8时
就会报错，解决办法就是在读的时候也加上对应的utf-8编码，再读就不会报错了'''

#下面在读取时加上了encoding，就不会报错了
    with open('aa2.txt','r',encoding='utf-8') as a, open('aa3.txt','w') as b:
        for line in a:
            if 'sun' in line:
                line=line.replace('sun','luo')
            b.write(line)
    with open('aa3.txt','r') as c:
        print('aa3.txt的内容为：',c.read())
