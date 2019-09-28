#!/usr/bin/env python3
# Auther: sunjb
import os
class BaseSaltModule(object):
    '''
    定义公共类，这个类会被其他的类调用，用于向其他内传递参数
    注意：其他类在引用了公共类之后，如果也定义了__init__，会
    把这个公共类的__iinit__方法覆盖掉，导致公共类里面的方法
    不生效.如果要继承，应该用super方法重构公共类
    '''

    def __init__(self, sys_argvs, db_models, settings):
        self.settings = settings
        self.sys_argvs = sys_argvs
        self.db_models = db_models
        self.require_list=[]


    def get_selected_os_type(self):
        # self.fetch_hosts()
        print('in get_select_os_type')
        print(self.host_list)
        data = {}
        # 生成一个空的操作系统字典，用户后续将对应的主机加到字典里面，得到每个系统对应的主机
        for host in self.host_list:
            data[host.os_type] = []
        print('data', data)
        return data

    def process(self):
        print('in process')
        self.fetch_hosts()
        self.config_data_dic = self.get_selected_os_type()


    def fetch_hosts(self):
        '''
        获取到数据库里面的主机以及主机组
        :return:
        '''
        print('--fetch--')
        host_list = []
        if '-h' in self.sys_argvs or '-g' in self.sys_argvs:
            if '-h' in self.sys_argvs:
                host_str_index = self.sys_argvs.index('-h') + 1
                # 定义参数长度必须大于索引长度，也就是说，如果-h后面不能为空，如果没有参数，那么就是等于，就提示必须接参数。
                if len(self.sys_argvs) <= host_str_index:
                    print('-h后面必须接参数')
                else:  # 如果后面有参数，则提取里面的主机名称
                    host_str = self.sys_argvs[host_str_index]
                    host_str_list = host_str.split(',')
                    print(host_str, host_str_list)
                    # hostname__in相当于 where hostname in xxx 。去数据库把匹配的主机查询出来
                    host_list += self.db_models.Host.objects.filter(hostname__in=host_str_list)

                    # print('host list:',host_list)
            if '-g' in self.sys_argvs:
                group_str_index = self.sys_argvs.index('-g') + 1
                # 定义参数长度必须大于索引长度，也就是说，如果-h后面不能为空，如果没有参数，那么就是等于，就提示必须接参数。
                if len(self.sys_argvs) <= group_str_index:
                    print('-g后面必须接参数')
                else:  # 如果后面有参数，则提取里面的组名称
                    group_str = self.sys_argvs[group_str_index]
                    group_str_list = group_str.split(',')
                    print(group_str, group_str_list)
                    # hostname__in相当于 where hostname in xxx 。去数据库把匹配的主机查询出来
                    group_list = self.db_models.HostGroup.objects.filter(name__in=group_str_list)
                    # 将查找到的组列表循环，获取里面的主机，并和前面的主机合并
                    for group in group_list:
                        host_list += group.hosts.select_related()
            self.host_list = set(host_list)  # 将host_list设置成全局的，所有函数都可以调用
            print('host list:', host_list)
        else:
            exit('-h or -g 参数是必须的')

    # 获取主机和操作系统信息，这个不是所有模块都要调用的，所以改为手动触发

    def syntax_parser(self, section_name, mod_name, mod_data,os_type):
        '''解析并执行yaml里面的方法'''
        print('syntax_parser', section_name, mod_name, mod_data)

        self.raw_cmds = []
        self.single_line_cmds = []
        # 对yaml里面模块下面的数据一行行的循环，得到state_item={'uid':10}这样的数据
        for state_item in mod_data:     # mod_data=[{'uid': 87}, {'gid': 87},{'require': [{'group': 'apache'}, {'pkg': 'httpd'}]}]
            # 对字典state_item循环，得到key=uid,val=10
            for key, val in state_item.items():
                # 这里的self就代表实例本身，当循环到yaml里面的user模块时，在state.py里面我们实例化了类User，所以这里self就是代表User类
                if hasattr(self, key):  # 这里就是判断User类下面是否有uid的方法 self=User
                    state_func = getattr(self, key)  # 获取到对应的方法User下面的uid方法
                    state_func(val,section=section_name,os_type=os_type)  # 执行uid(val),require()等方法
                else:
                    exit('模块%s没有方法%s' % (self, key))
        else:  # 当上面的循环结束后，执行下面的语句
            if '.' in mod_name: # mod_name=user.present 即yaml里面定义的模块及要执行的方法 如user.present,group.present
                base_mod_name, mod_action = mod_name.split('.')
                if hasattr(self, mod_action):  # 获取到"."后面的参数,得到同名的方法。 比如 user模块下的present方法
                    mod_action_func = getattr(self, mod_action)
                    #cmd_list = mod_action_func(val,section=section_name,os_type=os_type)   #执行user下面的present()方法
                    cmd_list = mod_action_func(section=section_name,mod_data=mod_data)   #执行user下面的present()方法
                    data = {
                        'cmd_list':cmd_list,
                        'require_list':self.require_list
                    }
                    if type(cmd_list) is dict:  # 文件模块file.managed返回的cmd_list是字典形式，如果是字典格式，就代表这是文件模块
                        data['file_module']=True
                        data['sub_action']=cmd_list.get('sub_action')
                    return data
                    #上面代表一个section里面具体的一个module已经解析完毕
                else:
                    exit(f'{mod_name}不存在方法{mod_action}')
            else:
                exit(f'模块{mod_name}的方法必须提供')

    def argv_validation(self, name, val, datatype):
        if type(val) is not datatype:
            exit('%s值的格式不正确' % name)

    def require(self,*args,**kwargs):
        '''
        syntax_parser里面利用hasattr动态调用了该方法
        调用对应模块里面的is_required方法，生成依赖条件检测命令，追加到require_list列表里面
        require方法是使用getattr动态调用的，所以pycharm用alt+f7无法追踪到是谁调用了这个方法。
        '''
        print('in require'.center(60,'#'))
        print(args,kwargs)
        for item in args[0]:   # args[0] = ([{'group': 'apache'}, {'pkg': 'httpd'}],)
            for mod_name,mod_val in item.items():   # mod_name=group mod_val=apache
                module_obj=self.get_module_instance(base_mod_name=mod_name,os_type=kwargs.get('os_type'))
                require_condition=module_obj.is_required(mod_name,mod_val)
                print('require_condition',require_condition)
                self.require_list.append(require_condition)
                #print(module_obj)
        print('require_list',self.require_list)
        print('out require'.center(60,'#'))

    def is_required(self,*args,**kwargs):
        exit(f'{args[0]}模块is_required是必须的')


    def get_module_instance(self,*args,**kwargs):
        '''
        被require()调用
        根据yaml里面的语法，找打对应的模块文件，获取到对应的类里面的方法，执行该方法，并获取返回结果
        比如：
        get_module_instance(base_mod_name=group,os_type='linux')
        将找到group.py模块里面的RedhatGroup()方法，并执行该方法，获取到该方法的返回值，并返回
        :param args:
        :param kwargs:
        :return:
        '''
        base_mod_name=kwargs.get('base_mod_name')
        os_type=kwargs.get('os_type')
        plugin_file_path = f'{self.settings.SALT_PLUGINS_DIR}{base_mod_name}.py'    #找打对应的模块文件
        if os.path.isfile(plugin_file_path):  # 如果存在该模块文件user.py
            module_mem = __import__(f'plugins.{base_mod_name}')  # 加载到内存，这里并没有将模块真正的import进来
            print(module_mem)
            # 导入user.py模块文件
            module_file = getattr(module_mem, base_mod_name)  # 这里才是真的导入模块
            # 得到模块里面的方法名，方法名为操作系统+模块名，比如RedhatGroup，capitalize()将首字母大写
            specical_os_module_name = f'{os_type.capitalize()}{base_mod_name.capitalize()}'
            print('special_os_module_name',specical_os_module_name)
            # 判断模块下是否存在specical_os_module_name方法
            if hasattr(module_file, specical_os_module_name):  # 如果存在UbuntuUser方法
                module_instance = getattr(module_file, specical_os_module_name)  # 获取到user.py的UbuntuUser()方法
            else:
                module_instance = getattr(module_file, base_mod_name.capitalize())  # 获取到user.py的User()方法
            # 调用模块
            # print(module_instance)
            # 调用User()或者UbuntuUser()方法，由于继承了base_module，所以需要传入基类里面的三个参数
            module_obj = module_instance(self.sys_argvs, self.db_models, self.settings)
        else:
            exit(f'模块文件{base_mod_name}不存在')
        return module_obj