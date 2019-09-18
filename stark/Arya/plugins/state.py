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
                # 根据不同的操作系统循环，生成不同的配置文件。这个config_data_dic是从基类base_module里面继承而来的
                for os_type, os_type_data in self.config_data_dic.items():
                    # 对整个yaml文件循环，得到section_name=apache,section_data=apache下面的数据，这是一个字典
                    for section_name, section_data in state_data.items():
                        print('Section:', section_name)
                        # 对apache下面的数据循环，mod_name=user.present,mod_data=[user.present下面的数据]
                        for mod_name, mod_data in section_data.items():
                            base_mod_name = mod_name.split('.')[0]  # 截取前面的部分，也就是模块文件名user
                            # 通过上面得到的文件名，获取到对应的具体的模块user.py文件的绝对路径
                            module_obj = self.get_module_instance(base_mod_name=base_mod_name, os_type=os_type)
                            # 调用基类里面的语法检测函数，传入apache,user.present,以及user.present下面的数据。
                            module_parse_result = module_obj.syntax_parser(section_name, mod_name, mod_data,os_type)
                            self.config_data_dic[os_type].append(module_parse_result)
                print(self.config_data_dic)
                    # print(" ", mod_name, mod_data)
                    # for state_item in mod_data:
                    #     print("\t", state_item)
                # 出现IndexError异常说明超出了索引边界，也就是self.sys_argvs[yaml_file_index]报错了，yaml_file_index这个索引并没有值，也就是-f后面没有值
            except IndexError as e:
                exit('超出索引边界，-f后面必须指定文件')
        else:
            exit('-f要指定')
