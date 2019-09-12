#!/usr/bin/env python3
# Auther: sunjb

from Arya import action_list
import django
django.setup()
#先执行上面两条，把django的models引用进来，再执行import models
from Arya import models
from stark import settings
import sys, os


class ArgvManagement(object):
    '''
    接收用户指令并分配到相应的模块
    '''
    def __init__(self, argvs):
        self.argvs = argvs

    def help_msg(self):
        print('Usage:')
        for registered_module in action_list.actions:
            print(f'{registered_module}')
        exit()      #定义了退出，所以只要执行了这个方法，后面的代码就不会执行了，因为退出了
    def argv_parse(self):
        # print(self.argvs)
        if len(self.argvs) < 2:
            self.help_msg()
        model_name = self.argvs[1]
        # print(model_name)
        if '.' in model_name:
            mod_name,mod_method=model_name.split('.')
            # print('mod_name:%s,mod_method:%s'%(mod_name,mod_method))
            # print(action_list.actions)
            module_instance=action_list.actions.get(mod_name)
            print('module_instance',module_instance)
            if module_instance:
                print('in if')
                module_obj=module_instance(self.argvs,models,settings)
                print('2')
                module_obj.process()  # 执行base_module里面的获取主机
                # print('ostype',module_obj.process())
                #hasattr判断module_obj里面是否有mod_method属性(变量)或方法，有则返回true，注意mod_method必须为字符串
                if hasattr(module_obj,mod_method):
                    #getattr获取module_obj里面的方法mod_method。注意这里mod_method同样时字符串，如果要直接调用里面的方法，应该写成getattr(module_obj(),mod_method)()
                    module_method_obj=getattr(module_obj,mod_method)
                    module_method_obj() #调用指定的指令
                else:
                    exit(f"{mod_name}不存在{mod_method}方法")
            else:
                print('method is not exist')
        else:
            exit('invalid module name argument')
