#!/usr/bin/env python3
# Auther: sunjb

#from conf.configs import registered_modules
import pika
import platform
import subprocess
import json,threading
from modules import files
from conf import configs

class CommandManagement(object):
    def __init__(self,argvs):
        self.argvs=argvs[1:]
        self.argv_handle()

    def argv_handle(self):
        if len(self.argvs) ==0:
            exit('启动或停止:start/stop')
        if hasattr(self,self.argvs[0]):
            func=getattr(self,self.argvs[0])
            func()
        else:
            exit('CommandManagement不存在此方法')

    def start(self):
        client_obj=Needle()
        client_obj.listen()

    def stop(self):
        pass

class Needle(object):
    def __init__(self):
        #self.configs=configs
        self.makeconnections()
        self.client_id=self.get_needle_id()
        self.task_queue_name=f'TASK_Q_{self.client_id}'

    def get_needle_id(self):
        '''去服务器端取自己的Id'''
        return configs.NEEDLE_CLIENT_ID
    def listen(self):
        '''开始监听服务'''
        self.msg_consume()

    def makeconnections(self):
        '''创建连接'''
        credentails=pika.PlainCredentials(configs.MQ_CONN['user'],configs.MQ_CONN['pass'])
        self.mq_conn=pika.BlockingConnection(pika.ConnectionParameters(
            configs.MQ_CONN['host'],
            configs.MQ_CONN['port'],configs.MQ_CONN['vhost'],credentails
        ))
        self.mq_channel = self.mq_conn.channel()



    def msg_callback(self,ch,method,properties,body):
        '''每一个任务单独启动一个线程'''
        print('msg_callback接收消息')
        #启动一个线程，并把body作为参数传递进去
        thread=threading.Thread(target=self.start_thread,args=(body,))
        thread.start()
    def start_thread(self,task_body):
        print('启动线程')
        task=TaskHandle(self,task_body) #这里的self就是Needle类实例化后的实例
        task.processing()

    def msg_consume(self):
        '''开始监听消息，有消息过来则接收消息，没有就挂起'''
        print('msg_consume task_queue_name:',self.task_queue_name)
        self.mq_channel.queue_declare(queue=self.task_queue_name)
        self.mq_channel.basic_consume(self.task_queue_name,self.msg_callback,False)
        self.mq_channel.start_consuming()

class TaskHandle(object):
    def __init__(self,main_obj,task_body):
        # 这里的main_obj就是Needle object，因为是Needle类里面的start_thread调用的TaskHandle(self,task_body)，这里的self就是指Needle实例本身
        # 在消息收到后，要返回数据给队列，利用Needle里面建立好的队列再返回消息
        self.main_obj=main_obj
        # python3的所有socket传输都是以byte字节流的方式发送了，而json只能解析字符串，是不能解析二进制的字节流的，所以要decode先转成字符串
        self.task_body=json.loads(task_body.decode())

    def processing(self):
        print('in handle processing')
        check_res = self.check_data_validation()
        if check_res:
            self.current_os_type, data = check_res
            self.parse_task_data(self.current_os_type, data)

    def check_data_validation(self):
        '''
        确保服务端发过来的任务在本地是可以执行的

        '''
        # platform用来获取本地操作系统类型,在linux上，下面的命令将返回操作发行版本，如centos,unbuntu
        os_version=platform.version().lower()
        for os_type,data in  self.task_body['data'].items():    #os_type=redhat  data=[{cmd_list...}]
            print(os_version,os_type)
            if os_type not in os_version:
                print(os_type,data)
                return os_type,data
            else:
                print('不支持的操作系统')

    def parse_task_data(self,os_type,data):
        '''
        解析任务数据并执行
        :param os_type:
        :param data:
        :return:
        '''
        applied_list=[] #所有已经执行了的子任务section都放在这里面
        applied_result=[]   #把所有应用的section的执行结果放在这里面
        last_loop_len = len(applied_list)
        '''
        while用于一次次的循环执行，用于解决各个模块件相互依赖的问题.不论依赖是否全部满足，最终都会走到break里面退出循环。
        比如d-->b-->c-->a的依赖关系，a无依赖。
        循环1：dbc都不满足，a执行成功，applied_list=[a] if中last_loop_len=0 不等于len(applied_list)=1 循环完成后设置last_loop_len=len(applied_list)
        循环2: db不满足，c由于依赖的a已经执行，所以c执行成功 applist=[a,c] last_loop_len=1  len(applied_list)=2 循环完后last_loop_len=2
        循环3: d不满足，由于c上次循环执行成功，所以本次b执行成功 applist=[a,c,b] last_loop_len=2 len=3 循环完后last_loop_len=3
        循环4：d执行成功 applist=[a,c,b,d] last_loop_len=3 len=4    循环完后last_loop_len=4
        循环5：全部成功，所以applied_list的长度不会增加， last_loop_len=4 len=4 .  
                len(applied_list) == last_loop_len成立，break退出循环。 
        
        如果有元素执行失败，比如b失败了，那么
        循环1：a成功 [a] last_loop_len=0 len=1
        循环2: c成功 [a,c] last_loop_len=1 len=2
        循环3: b失败 [a,c] last_loop_len=2 len=2  -->触发break退出循环      
        '''
        while True:
            for section in data:    #对data=[{cmd_list...},{cmd_list...}]，所以section就是一个个{cmd_list:xxx}的字典
                if section.get('called_flag'):  #代表已经执行过，如果执行过一次，就给这个字典添加这个key，这样后面就不会在重复循环了，这样每次循环就能缩小范围
                    print('已经执行过了')
                else:
                    apply_status,result=self.apply_section(section) # apply_status=True/False result=res
                    print('apply_status,result:',apply_status,result)
                    if apply_status==True:  #如果为True，代表命令执行成功了
                        applied_list.append(section)    #如果成功，那么就将section添加到列表里面，所以applied_list列表都是执行成功的section
                        applied_result+=result  #收集结果，并累加，成功的result会是0
                        if result == [0]:
                            print('这是一条执行成功的命令',section)
                        else:
                            print('这条命令失败了:',section)

            '''
            如果长度没有变化，那么证明apply_statue不等于True，或者全部都有section.get('called_flag')=True的标记,
            当全部都是called_flag=True的标记时，证明所有的依赖都已经正确执行了（因为只有依赖返回为0时，才会添加True标记）
            如果apply_statue != True，证明依赖条件不满足，执行依赖失败了。
            所以总共就两者情况会满足下面的if条件，要么执行玩了，要么有依赖执行失败
            '''
            if len(applied_list) == last_loop_len:
                print('parse_task_data循环完成：',applied_list,last_loop_len)
                print('applied_result:',applied_result)
                break
            last_loop_len=len(applied_list)
        #接下来把结果返回给服务器
        print('将结果发送给服务器')
        self.task_callback(self.task_body['callback_queue'],applied_result)

    def apply_section(self,section_data):
        '''执行指定的task section
        被parse_task_data方法调用
        '''
        print('应用section_data',section_data['require_list'])
        #首先判断执行的section是否有依赖

        if section_data['require_list'] != []:    #判断是否有依赖
            #将require_list依赖的命令传给check_pre_requisites方法，如果返回0，代表依赖条件全部满足
            if self.check_pre_requisites(section_data['require_list']) ==0:     #依赖满足
                if section_data.get('file_source')==True:   #如果有文件，就交给文件处理函数file_handle处理
                    res=self.file_handle(section_data)  #{cmdline:xx}
                else:
                    res=self.run_cmd(section_data['cmd_list'])
                section_data['called_flag']=True    #执行完成后，加上一个标记，说明已经执行过,parse_task_data里面会通过这个标记判断是否已执行
                return [True,res]   #返回True,以及命令执行的结果res
            else:
                print('依赖条件不满足')
                return [False,None]
        else:
            print('依赖条件不存在')
            return [False,None]

    def run_cmd(self,cmd_list):
        '''执行传过来的命令
        被apply_section函数调用
        '''
        cmd_result=[]
        for cmd in cmd_list:
            print('run_cmd',cmd)
            cmd_res=subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            if platform.system() == 'Windows':
                cmd_result.append(cmd_res.returncode)
            else:
                cmd_result.append(int(cmd_res.stdout.decode().strip()))
            #cmd_result.append(int(cmd_res.stdout.decode().strip()))
            print('cmd_result:',cmd_result)
            return cmd_result
    def file_handle(self,section_data):     #section_data就是{cmd_list:...}
        '''对文件进行操作'''

        file_module_obj= files.FileModule(self)
        file_module_obj.process(section_data)
        return []




    def check_pre_requisites(self,conditions): #conditions=['id apache;echo $?', 'rpm -qa |grep httpd;echo $?']
        '''
        检测依赖条件是否满足，如果全部成了则返回0
        被apply_section方法调用
        :param conditions:
        :return:
        '''
        print('检测依赖条件',conditions)
        conditions_result=[]
        for condition in conditions:
            print('condition',condition)
            #condition='dir && echo 0 || echo 1'
            # 调用shell执行conditions命令，将正确的和错误的结果都输出到一个PIPE管道中去，这样我们才能获取到输出的结果
            cmd_res=subprocess.run(condition,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            #int(cmd_res.stdout.decode().strip())这里就限定了我们客户端返回的stdout结果必须是0或者1，不能返回别的字符串，否则没法int
            #注意在py3里面subprocess返回的是byte格式的数据，所以必须先decode()转成字符串，然后才能进一步处理
            if platform.system() == 'Windows':
                conditions_result.append(cmd_res.returncode)
            else:
                conditions_result.append(int(cmd_res.stdout.decode().strip()))
            print('conditions_result:',conditions_result)
            return sum(conditions_result)   #对结果进行求和，如果全是0，那么return的结果也就是0
    def task_callback(self,callback_queue,callback_data):
        pass
