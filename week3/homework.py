#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
def select():
    select_num=input('''
     请选择你要的操作：
     1：增加一行
     2：删除一行
     3：修改一行
     ''')
   # select_num="1"
    try:
        num=eval(select_num)
        if num in range(1,4):

            if num==1:
                insert()
            elif num==2:
                delete()
            else:
                replace()
        else:
            exit(1)
    except:
        print('你输入的不正确,请输入以上数字')

def insert():
    line=eval(input("""请用字典形式输入你要插入的数据，例如：
              {"backend":"ttt.oldboy.org","record":{"server":"100.1.7.8","weight":"20","maxconn":"3000"}}
                """))
    #line={"backend":"ttt.oldboy.org","record":{"server":"100.1.7.9","weight":"20","maxconn":"3000"}}  #临时调试用
    #print(type(line))
    line=dict(line)
    print(line.get('record'))

    with open('config','r') as oldfile, open('config-new','w') as newfile:
         #   newfile.write(oldfile.read())
            for i in oldfile:
                newfile.write(i)
                if 'backend' and line.get('backend') in i :
                    server=line.get('record')
                    for j,k in server.items():
                        a='{} {} {}'.format('       ',j,k)
                        newfile.write(a)
                    newfile.write('\n')

def delete():
    line=eval(input("""请用字典形式输入你要删除的数据，例如：
              {"backend":"ttt.oldboy.org","record":{"server":"100.1.7.8","weight":"20","maxconn":"3000"}}
                """))
    #line = {"backend": "ttt.oldboy.org", "record": {"server": "100.1.7.9", "weight": "20", "maxconn": "3000"}}  # 临时调试用
    line=dict(line)
    with open('config','r') as oldfile, open('config-new','w') as newfile:
        for i in oldfile:
            if 'server' and 'weight' not in i:
                newfile.write(i)
            else:
                print(i.strip())
                oldline=i.strip()
                server=line.get('record')
                a=str()
                for j,k in server.items():
                    a = '{} {} {}'.format(a, j, k)
                print(a.strip())
                delline=a.strip()
                if oldline == delline:
                    pass
                else:
                    newfile.write(i)

def replace():
    src_line=eval(input('''请输入你要替换的源字符
    示例：{"backend": "ttt.oldboy.org", "record": {"server": "100.1.7.9", "weight": "20", "maxconn": "3000"}}'''))
    line=eval(input('''请输入你要替换的目标字符
    示例：{"backend": "ttt.oldboy.org", "record": {"server": "100.1.7.2", "weight": "20", "maxconn": "3000"}}'''))
  #  src_line={"backend": "ttt.oldboy.org", "record": {"server": "100.1.7.9", "weight": "20", "maxconn": "3000"}}  # 临时调试用
 #   line = {"backend": "ttt.oldboy.org", "record": {"server": "100.1.7.20", "weight": "20", "maxconn": "3000"}}  # 临时调试用
    src_line=dict(src_line)
    line = dict(line)
    with open('config','r') as oldfile, open('config-new','w') as newfile:
        for i in oldfile:
            if 'server' and 'weight' not in i:
                newfile.write(i)
            else:
                oldline = i.strip()
                src_server=src_line.get('record')
                server=line.get('record')
                a=str()
                src_a=str()
                for j,k in server.items():
                    a = '{} {} {}'.format(a, j, k)
                replace_line=a.strip()
                for j,k in src_server.items():
                    src_a = '{} {} {}'.format(src_a, j, k)
                match_line=src_a.strip()
              #  print(match_line)
             #   print(oldline)
                if match_line == oldline:
                    i=i.replace(match_line,replace_line)
                newfile.write(i)


#replace()
#insert()
#delete()
select()