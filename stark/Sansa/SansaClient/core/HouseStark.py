#!/usr/bin/env python3
# Auther: sunjb
#from stark import settings
import datetime,os,json,urllib,urllib3,sys
from core import info_collection
from conf import settings
class ArgvHandler(object):
    def __init__(self,argv_list):
        self.argv=argv_list
        self.parse_argv()
    def parse_argv(self):
        if len(self.argv)>1:
            if hasattr(self,self.argv[1]):
                func=getattr(self,self.argv[1])
                func()
            else:
                self.help_msg()
        else:
            print('没有参数')
            self.help_msg()

    def help_msg(self):
        msg='''
        collect_data
        run_forever
        get_asset_id
        report_asset        
        '''
        print(msg)

    def collect_data(self):
        '''收集资产信息,只收集不汇报'''
        obj=info_collection.InfoCollection()
        asset_data=obj.collect()
        print('collect_data',asset_data)
    def run_forever(self):
        pass
    def __attach_token(self):

        user=settings.Params['auth']['user']
        token_id=settings.Params['auth']['token']

    def load_asset_id(self,sn=None):
        '''获取本机的asset_id
        首先会去本地的conf/settings.py里面查看asset_id参数,得到存放
        asset_id文件的具体位置.然后判断文件是否存在,如果存在则读取文件,
        如果读取的是数字,则返回该数字.
        其它情况则不会返回asset_id
        '''
        asset_id_file=settings.Params['asset_id']
        has_asset_id=False
        if os.path.isfile(asset_id_file):
            asset_id=open(asset_id_file).read().strip()
            try:
                id=int(asset_id)
                return asset_id
            except Exception as e:
                print('id必需是数字',e)
                has_asset_id=False
        else:
            has_asset_id = False

    def __update_asset_id(self,new_asset_id):
        '''更新资产id
        先到setttings里面取出id对应的文件路径,然后将传过来的资产id写入到该文件
        '''
        asset_id_file=settings.Params['asset_id']
        with open(asset_id_file,'w') as f:
            f.write(str(new_asset_id))
            f.close()
    def report_asset(self):
        '''
        该方法用于连接指定url汇报资产信息,并获取对应url的返回结果
        客户端连接到服务器后,服务器会返回一个资产id到客户端,客户端拿到资产id后,
        会存到一个指定的文件里面. 下次客户端再次联系服务器端时,就会带着这个资产id,
        这样服务器端就知道客户端是台老机器. 这样服务器端就根据这个id拿数据库里面的数据
        进行比对,如果有不一样的就更新一下资产信息.
        如果客户端没有资产id发过去,那么证明客户端是第一次连接服务器,服务器端就认为这是一台新加入的机器.
        当我们批准这台机器加入后,服务器端会返回一个id给客户端,这样下次客户端再连接时就有资产id了
        '''
        obj=info_collection.InfoCollection()
        # asset_data包含了cpu/内存/主机类型/网卡等各种信息的字典
        asset_data=obj.collect()
        #如何确定这台机器是新机器呢?就是看你有没有传资产id在服务端,如果有,则不是新机器,如果没有则是第一次连接
        asset_id=self.load_asset_id(asset_data['sn'])
        if asset_id:    #如果有id,证明之前汇报过
            asset_data['asset_id']=asset_id
            post_url='asset_report'
        else:   #第一次连接server,如果没有资产id,则向另一个url汇报
            asset_data['asset_id']=None
            post_url='asset_report_with_no_id'
        print('post_url',post_url)
        data={'asset_data':json.dumps(asset_data)}
        # 将数据以post的方法提交到submit_data函数,该函数会请求指定的url,将客户端的数据提交上去,并获取返回的结果
        response=self.__submit_data(post_url,data,method='post')
        print('response:',response)
        if 'asset_id' in response:
            self.__update_asset_id(response['asset_id'])
        self.log_record(response)

    def __submit_data(self, url_name, data, method):
        '''
        根据请求的名称,去settings里面找到对应的请求地址,并生成完整的请求地址.
        如果是get,则拼接成get请求的完整URL,如果是POST,则生成对就的POST地址,并将data数据传递过去
        然后取返回值,将url返回的数据return
        :param url_name:
        :param data:
        :param method:
        :return:
        '''
        print(settings.Params['urls'])
        if url_name in settings.Params['urls']:
            if type(settings.Params['port']) is int:
                #print(settings.Params['server'],settings.Params['port'],settings.Params['urls'][url_name])
                url='http://%s:%s%s/'%(settings.Params['server'],settings.Params['port'],settings.Params['urls'][url_name])
            else:
                url='http://%s%s/'%(settings.Params['server'],settings.Params[url_name])
            #url=self.__attach_token(url)    #api认证
            print('连接%s'%url)
            if method == 'get':
                args = ""
                for k,v in data.items():
                    args += "&%s=%s"%(k,v)  #将后面的请求参数拼接成get的形式,即?a=b&c=d这样
                ''' 
                args[1:]代表从第一个字符开始取,直到最后一个,我们生成拼接的字符串时,第一个字符是&,
                我们生成的url应该是www.baidu.com?aa=1&bb=2&cc=3这样的,而拼接出来的是&aa=1&bb=2&cc=3
                所以第一个&要去掉.
                '''
                args=args[1:]
                url_with_args="%s?%s"%(url,args)    #将url和参数拼接成一个完整的请求地址
                try:
                    http=urllib3.PoolManager()
                    req_data=http.request('GET',url_with_args)
                    callback=req_data.data.decode()

                    # req=urllib3.Request(url_with_args)
                    # req_data=urllib3.urlopen(req,timeout=settings.Params['request_timeout'])
                    # callback=req_data.read()
                    print('server response-->',callback)
                    return json.loads(callback)
                except urllib3.URLError as e:
                    sys.exit('访问url出错',e)
            elif method == 'post':
                try:


                    http = urllib3.PoolManager()
                    r = http.request('post', url, fields=data)
                    print(r.status)
                    callback=r.data.decode()
                    callback=json.loads(callback)
                    #print(method, url, callback)
                    # print(callback)
                    # data_encode=urllib.parse.urlencode(data)
                    # req=urllib3.Request(url=url,data=data_encode)
                    # res_data=urllib3.urlopen(req,timeout=settings.Params['request_timeout'])
                    # callback=res_data.read()
                    #callback=json.loads(callback)
                    #print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" %(method, url, callback))
                    print('callback:',type(callback),callback)
                    return callback
                except Exception as e:
                    sys.exit("\033[31;1m%s\033[0m"%e)
        else:
            print(settings.Params['urls'])
            raise KeyError

    def log_record(self,log,action_type=None):
        f=open(settings.Params['log_file'],'a+')
        if log is str:
            pass
        if type(log)  is dict:
            if 'info' in log:
                for msg in log['info']:
                    log_format='%s\tINFO\t%s\n'%((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),msg)
                    f.write(log_format)
            if 'error' in log:
                for msg in log['error']:
                    log_format='%s\tINFO\t%s\n'%((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),msg)
                    f.write(log_format)
            if 'warning' in log:
                for msg in log['warning']:
                    log_format='%s\tINFO\t%s\n'%((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),msg)
                    f.write(log_format)
        f.close()

