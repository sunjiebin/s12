#!/usr/bin/env python3
# Auther: sunjb
from Arya.backends.base_module import BaseSaltModule
import os


class State(BaseSaltModule):

    def load_state_files(self, state_filename):
        '''
        该函数用于读取yaml格式的文件并解析成字典格式
        依赖pyyaml模块，所有先要安装这个模块
        :param state_filename:
        :return:
        '''
        from yaml import load, dump
        try:
            from yaml import CLoader as Loader, CDumper as Dumper
        except ImportError:
            from yaml import Loader, Dumper
            # 在settings.py里面定义一个配置文件，用于指定配置文件的路径
        state_file_path = "%s/%s" % (self.settings.SALT_CONFIG_FILES_DIR, state_filename)
        if os.path.isfile(state_file_path):
            with open(state_file_path) as f:
                data = load(f.read(), Loader=Loader)
                return data
        else:
            exit("%s is not a valid yaml config file" % state_filename)

    # def process(self):
    #     pass

    def apply(self):
        '''
        1. load the configueration file
        2. parse it
        3. create a task and send it to the MQ
        4. collect the result with task-callback id
        :return:
        '''

        if '-f' in self.sys_argvs:
            yaml_file_index = self.sys_argvs.index('-f') + 1
            try:
                yaml_filename = self.sys_argvs[yaml_file_index]
                state_data = self.load_state_files(yaml_filename)
                print('state data:', state_data)
                #根据不同的操作系统循环，生成不同的配置文件。这个config_data_dic是从基类base_module里面继承而来的
                for os_type, os_type_data in self.config_data_dic.items():
                    for section_name, section_data in state_data.items():
                        print('Section:', section_name)
                        for mod_name, mod_data in section_data.items():
                            base_mod_name=mod_name.split('.')[0]    #截取前面的部分，也就是模块文件名
                            plugin_file_path=f'{self.settings.SALT_PLUGINS_DIR}{base_mod_name}.py'

                            if os.path.isfile(plugin_file_path):
                                module_mem=__import__(f'plugins.{base_mod_name}')   #加载到内存，这里并没有将模块真正的import进来
                                print(module_mem)
                                module_file=getattr(module_mem,base_mod_name)        #这里才是真的导入模块
                                specical_os_module_name=f'{os_type.capitalize()}{base_mod_name.capitalize()}'        #capitalize()将首字母大写
                                # print(specical_os_module_name)
                                #判断模块下是否存在specical_os_module_name方法
                                if hasattr(module_file,specical_os_module_name):
                                    module_instance=getattr(module_file,specical_os_module_name)    #获取方法
                                else:
                                    module_instance=getattr(module_file,base_mod_name.capitalize())
                                #调用模块
                                # print(module_instance)
                                module_obj=module_instance(self.sys_argvs,self.db_models,self.settings)
                                #调用基类里面的语法检测函数
                                module_obj.syntax_parser(section_name,mod_name,mod_data)
                            else:
                                exit(f'模块文件{base_mod_name}不存在')
                           # print(" ", mod_name, mod_data)
                           # for state_item in mod_data:
                           #     print("\t", state_item)
            # 出现IndexError异常说明超出了索引边界，也就是self.sys_argvs[yaml_file_index]报错了，yaml_file_index这个索引并没有值，也就是-f后面没有值
            except IndexError as e:
                exit('超出索引边界，-f后面必须指定文件')
        else:
            exit('-f要指定')
