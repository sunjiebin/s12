#!/usr/bin/env python3
# Auther: sunjb

from Arya.backends.base_module import BaseSaltModule


class User(BaseSaltModule):
    def uid(self, *args, **kwargs):
        self.argv_validation('uid', args[0], int)
        cmd = f"-u {args[0]}"
        self.raw_cmds.append(cmd)

    def gid(self, *args, **kwargs):
        self.argv_validation('gid', args[0], int)
        cmd = f"-g {args[0]}"
        self.raw_cmds.append(cmd)

    def shell(self, *args, **kwargs):
        self.argv_validation('shell', args[0], str)
        cmd = f"-s {args[0]}"
        self.raw_cmds.append(cmd)

    def home(self, *args, **kwargs):
        self.argv_validation('home', args[0], str)
        cmd = f"-d {args[0]}"
        self.raw_cmds.append(cmd)

    # def require(self, *args, **kwargs):
    #     '''
    #     其他依赖条件
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     '''
    #     pass

    def password(self,*args,**kwargs):
        username=kwargs.get('section')
        password=args[0]
        cmd = '''echo "%s:%s"|chpasswd '''%(username,password)
        self.single_line_cmds.append(cmd)

    def present(self,*args,**kwargs):
        '''将前面各个函数生成的命令归总到一个列表里面'''
        # print(self.raw_cmds)
        # print(self.single_line_cmds)
        username=kwargs.get('section')  #获取section_name，即用户名
        self.raw_cmds.insert(0,f'user add {username}')  #在生成的命令列表最前面添加user add username
        cmd_list=[]
        raw_cmd=' '.join(self.raw_cmds) #将列表里面的所有字符串形式的元素拼接成一条字符串，以空格隔开
        cmd_list.append(raw_cmd)
        cmd_list.extend(self.single_line_cmds)  #extend用于两个列表和合并。这样single_line_cmds列表里面的元素就会合并到新的cmd_list里面。
        print('cmd_list',cmd_list)
        return cmd_list
    def is_required(self,*args,**kwargs):
        print('is required',args,kwargs)
        cmd=f"id {args[1]};echo $?"
        return cmd


    def __str__(self):
        return 'User'


class UbuntuUser(User):
    def home(self, *args, **kwargs):
        print('in ubnutn home ')

    def __str__(self):
        return 'UbuntuUser'

class WindowsUser(BaseSaltModule):
    def uid(self, *args, **kwargs):
        pass
    def gid(self, *args, **kwargs):
        pass

    def shell(self, *args, **kwargs):
        pass

    def home(self, *args, **kwargs):
        pass

    def password(self,*args,**kwargs):
        username=kwargs.get('section')
        password=args[0]
        cmd = '''echo "%s:%s" '''%(username,password)
        self.single_line_cmds.append(cmd)

    def present(self,*args,**kwargs):
        '''将前面各个函数生成的命令归总到一个列表里面'''
        # print(self.raw_cmds)
        # print(self.single_line_cmds)
        username=kwargs.get('section')  #获取section_name，即用户名
        self.raw_cmds.insert(0,f'net user {username}')  #在生成的命令列表最前面添加user add username
        cmd_list=[]
        raw_cmd=' '.join(self.raw_cmds) #将列表里面的所有字符串形式的元素拼接成一条字符串，以空格隔开
        cmd_list.append(raw_cmd)
        cmd_list.extend(self.single_line_cmds)  #extend用于两个列表和合并。这样single_line_cmds列表里面的元素就会合并到新的cmd_list里面。
        print('cmd_list',cmd_list)
        return cmd_list
    def is_required(self,*args,**kwargs):
        print('windows is required',args,kwargs)
        cmd="net user"
        return cmd
    def __str__(self):
        return 'User'