#!/usr/bin/env python3
# Auther: sunjb

class BaseSaltModule(object):

    def __init__(self,task_obj):
        self.task_obj=task_obj

    def process(self,module_data,*args,**kwargs):
        print('in base_module.py process')

        print('module_data:',module_data)
        section_name=module_data['cmd_list']['section'] # apache or /etc/httpd/conf/httpd.conf
        section_data=module_data['cmd_list']['mod_data']  # [{'source': 'salt://apache/httpd.conf'}, {'user': 'root'}, {'group': 'root'}, {'mode': 644}]
        sub_action=module_data['cmd_list'].get('sub_action')
        os_type=kwargs.get('os_type','linux')
        print('section_name:',section_name)
        for mod_item in section_data:   # [{'source': 'salt://apache/httpd.conf'}, {'user': 'root'}, {'group': 'root'}, {'mode': 644}]
            for key,val in mod_item.items():    #key=source val= 'salt://apache/httpd.conf'; key=user value=root
                if hasattr(self, f'func_{key}'):  # 这里就是判断files.py里面FileModule类下面是否有对应Key的方法 self=files.FileModule对象
                    state_func = getattr(self, f'func_{key}')  # 获取files.py下面FileModule类下面的func_xx方法
                    state_func(val)  # 执行uid(val),require()等方法
                    # state_func(val,section=section_name,os_type=os_type)  # 执行uid(val),require()等方法
                else:
                    exit('模块%s没有方法%s' % (self, key))
        if sub_action:  #如果有则执行，只针对文件模块,这里就是调用manager,其他模块没有定义这个字段
            sub_action_func=getattr(self,f'func_{sub_action}')
            res=sub_action_func(module_data=module_data['cmd_list'])
            return res

    def func_require(self,*args,**kwargs):
        print('require:',*args,**kwargs)


