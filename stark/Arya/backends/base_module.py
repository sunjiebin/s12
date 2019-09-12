#!/usr/bin/env python3
# Auther: sunjb

class BaseSaltModule(object):
    '''
    定义公共类，这个类会被其他的类调用，用于向其他内传递参数
    注意：其他类在引用了公共类之后，如果也定义了__init__，会
    把这个公共类的__iinit__方法覆盖掉，导致公共类里面的方法
    不生效.如果要继承，应该用super方法重构公共类
    '''
    def __init__(self,sys_argvs,db_models,settings):
        self.settings=settings
        self.sys_argvs=sys_argvs
        self.db_models=db_models

    def get_selected_os_type(self):
        #self.fetch_hosts()
        print('in get_select_os_type')
        print(self.host_list)
        data={}
        #生成一个空的操作系统字典，用户后续将对应的主机加到字典里面，得到每个系统对应的主机
        for host in self.host_list:
            data[host.os_type]=[]
        print('data',data)
        return data

    def process(self):
        print('in process')
        self.fetch_hosts()
        self.config_data_dic=self.get_selected_os_type()

    def fetch_hosts(self):
        print('--fetch--')
        host_list=[]
        if '-h' in self.sys_argvs or '-g' in self.sys_argvs:
            if '-h' in self.sys_argvs:
                host_str_index=self.sys_argvs.index('-h')+1
                # 定义参数长度必须大于索引长度，也就是说，如果-h后面不能为空，如果没有参数，那么就是等于，就提示必须接参数。
                if len(self.sys_argvs) <= host_str_index:
                    print('-h后面必须接参数')
                else:   #如果后面有参数，则提取里面的主机名称
                    host_str=self.sys_argvs[host_str_index]
                    host_str_list=host_str.split(',')
                    print(host_str,host_str_list)
                    # hostname__in相当于 where hostname in xxx 。去数据库把匹配的主机查询出来
                    host_list+=self.db_models.Host.objects.filter(hostname__in=host_str_list)

                    # print('host list:',host_list)
            if '-g' in self.sys_argvs:
                group_str_index=self.sys_argvs.index('-g')+1
                # 定义参数长度必须大于索引长度，也就是说，如果-h后面不能为空，如果没有参数，那么就是等于，就提示必须接参数。
                if len(self.sys_argvs) <= group_str_index:
                    print('-g后面必须接参数')
                else:   #如果后面有参数，则提取里面的组名称
                    group_str=self.sys_argvs[group_str_index]
                    group_str_list=group_str.split(',')
                    print(group_str,group_str_list)
                    # hostname__in相当于 where hostname in xxx 。去数据库把匹配的主机查询出来
                    group_list=self.db_models.HostGroup.objects.filter(name__in=group_str_list)
                    # 将查找到的组列表循环，获取里面的主机，并和前面的主机合并
                    for group in group_list:
                        host_list+=group.hosts.select_related()
            self.host_list=set(host_list)       #将host_list设置成全局的，所有函数都可以调用
            print('host list:',host_list)
        else:
            exit('-h or -g 参数是必须的')
    #获取主机和操作系统信息，这个不是所有模块都要调用的，所以改为手动触发


    def syntax_parser(self,section_name,mod_name,mod_data):
        print('syntax_parser',section_name,mod_name,mod_data)
