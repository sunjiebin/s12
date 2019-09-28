#!/usr/bin/env python3
# Auther: sunjb
#from modules.base_module import BaseSaltModule
from modules.base_module import BaseSaltModule
import shutil,os
from urllib import request

class FileModule(BaseSaltModule):
#    def __init__(self):
#        pass


    def func_directory(self,*args,**kwargs):
        module_data=kwargs.get('module_data')
        print('\033[41;1m 目录数据:\033[0m',module_data)
    def func_user(self,*args,**kwargs):
        pass
    def func_group(self,*args,**kwargs):
        pass
    def func_mode(self,*args,**kwargs):
        pass
    def func_managed(self,*args,**kwargs):
        '''
        从下载的文件目录拷贝文件到yml配置文件指定的目录
        :param args:
        :param kwargs:
        :return:
        '''
        print('in files func_managed')
        module_data = kwargs.get('module_data')
        print('\033[41;1m module_data:\033[0m',module_data)
        target_filepath = module_data['section']
        if self.has_source:
            if self.source_file is not None:
                if not os.path.isdir(os.path.dirname(target_filepath)):
                    os.makedirs(os.path.dirname(target_filepath))
                shutil.copyfile(self.source_file,target_filepath)
                print(f'从{self.source_file}复制文件到{target_filepath}')
        if os.path.isfile(target_filepath):
            print('文件复制成功')
            return [0]
        else:
            return [1]

    def download_http(self,file_path):
        '''
        根据获取的数据拼接url，生成一个完成的Url
        使用urllib从生成的url获取数据并下载下来，
        生成对应的临时文件保存的目录。将数据放到该目录
        :param file_path:
        :return:
        '''
        print('download from http:',file_path)
        print('download with urllib2')
        '''
        self.task_obj在基类base_module.py里面定义了self.task_obj=task_obj --> files.py里面的FileModule类继承了基类-->main.py里面的TaskHandle类的filehandle方法
        实例化了file.FileModule(self)-->得出file.FileModule(self)中的self为TaskHandle实例-->得出基类BaseSaltModule里面的self.task_obj即TaskHandle实例
        所以：self.task_obj.task_body = TaskHandle.task_body
        self.task_obj.main_obj --> TaskHandle.main_obj --> TaskHandle里面定义了self.main_obj=main_obj -->Needle类下面实例化了TaskHandle,task=TaskHandle(self,task_body)
        -->TaskHandle下面接收了两个参数def __init__(self,main_obj,task_body)，所以main_obj=前面的self，即Needle实例。
        所以: self.task_obj.main_obj = Needle实例
        self.task_obj.main_obj.configs.FILE_SERVER = Needle.configs.FILE_SERVER
        '''
        #print('main_obj',self.task_obj.main_obj.configs)
        http_server=self.task_obj.main_obj.configs.FILE_SERVER['http']  # localhost:8000
        url_arg=f'file_path={file_path}'    #url路径
        file_name=file_path.split('/')[-1]
        url=f'http://{http_server}{self.task_obj.main_obj.configs.FILE_SERVER_BASE_PATH}?{url_arg}' #http://localhost:8000/salt/file_center?file_path=//apache/httpd.conf
        print('\033[45;1mhttpserver\033[0m',url,self.task_obj.task_body['id'])
        f = request.urlopen(url)
        data=f.read()

        file_save_path='%s%s'%(self.task_obj.main_obj.configs.FILE_STORE_PATH,self.task_obj.task_body['id'])
        if not os.path.isdir(file_save_path):
            os.makedirs(file_save_path)
        with open(f'{file_save_path}/{file_name}','wb') as e:
            e.write(data)
        return file_save_path+'/'+file_name

    def download_salt(self,file_path,file_name):
        print('暂未开发download_salt',file_path)

    def func_source(self,*args,**kwargs):
        '''获取到配置文件中的http://apache/httpd.conf并解析，
        得到对应的方法download_salt，download_http方法，
        将得到的值传入方法中执行download_http(//apache/httpd.conf),
        将download_http(//apache/httpd.conf)赋值给self.source_file，
        所以self.source_file实际上就是download_http()返回的值，
        也就是文件路径file_save_path+'/'+file_name
        '''
        fileurl=args[0]
        print('下载..',fileurl)
        download_typ,file_path=fileurl.split(':')
        file_download_func=getattr(self,f'download_{download_typ}')
        self.source_file=file_download_func(file_path)
        print('source_file:',self.source_file)
        self.has_source=True

    def func_sources(self,*args,**kwargs):
        '''用于下载多个文件，循环读取每个文件，交给func_source一个个执行'''
        for file_source in args[0]:
            self.func_source(file_source)

    def func_recurse(self,*args,**kwargs):
        pass




