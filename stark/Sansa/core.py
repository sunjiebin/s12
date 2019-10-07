#!/usr/bin/env python3
# Auther: sunjb
import json
from django.utils import timezone
from Sansa import models


class Asset(object):
    def __init__(self, request):
        self.request = request
        self.mandatory_fields = ['sn', 'asset_id', 'asset_type']  # 强制要求的字段,要求客户端传过来的数据必需包含这几种数据
        self.field_sets = {
            'asset': ['manufactory'],
            'server': ['model', 'cpu_count', 'cpu_core_count', 'cpu_model', 'os_type', 'os_distribution', 'os_release'],
            'networkdevice': []
        }
        self.response = {
            'error': [],
            'info': [],
            'warning': [],
        }

    def response_msg(self, msg_type, key, msg):
        if msg_type in self.response:  # 判断字典中是否存在msg_type的key
            self.response[msg_type].append({key: msg})
        else:
            raise ValueError

    def mandatory_check(self, data, only_check_sn=False):
        '''
        对传过来的数据进行合法性检测,如果数据不包含上面定义的强制检测的三个字段,那么就会将错误输入到self.response中,
        当对强制字段检测循环完成后,检查self.response,如果这里面有error,那么证明校验失败,返回False
        如果校验成功,则进入到下一步.
        在数据库中查询data里面提供的id和sn号,如果找到了数据,则返回True.证明服务器里面有该资产.并生成对应数据对象self.asset_obj
        如果数据库查询失败,并报了个ObjectDoesNotExist的异常,那么证明数据库中不存在此数据,则返回False,并将资产标记为待批准
        :param data:
        :param only_check_sn:
        :return:
        '''
        for field in self.mandatory_fields:
            if field not in data:
                self.response_msg('error', 'MandatoryCheckFailed',
                                  "The field [%s] is mandatory and not provided in your reporting data" % field)
        else:  # 当前面的for循环完成后,进入到else条件.如果for循环过程中出现了异常,比如触发了response_msg的异常,则走不到else条件就报错了
            if self.response['error']: return False
        try:
            # 如果only_check_sn=False,则通过id以及sn联合查询出对应的资产信息
            if not only_check_sn:  # only_check_sn = False
                self.asset_obj = models.Asset.objects.get(id=int(data['asset_id']), sn=data['sn'])
            else:  # 如果only_check_sn=True,代表只通过sn查询对应的资产信息
                self.asset_obj = models.Asset.objects.get(sn=data['sn'])
            return True  # 只要上面查询成功,则返回True
        # except models.Asset.DoesNotExist as e: #如果前面的数据库查询失败了,则抛出异常ObjectDoesNotExist
        # except ObjectDoesNotExist as e: #如果前面的数据库查询失败了,则抛出异常ObjectDoesNotExist
        except models.Asset.DoesNotExist as e:
            print('数据未找到', e)
            self.response_msg('error', 'AssetDataInvalid',
                              "Cannot find asset object in DB by using asset id [%s] and SN [%s] " % (
                              data['asset_id'], data['sn']))
            self.waiting_approval = True  # 如果在数据库里面查不到该数据,证明这是一台新机器,于是将等待批准状态设置为True
            return False

    def data_is_valid(self):
        '''先获取到数据,校验数据'''
        data = self.request.POST.get('asset_data')
        if data:
            try:
                data = json.loads(data)
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error', 'AssetDataInvalid', str(e))
        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")

    def get_asset_id_by_sn(self):
        '''When the client first time reports it's data to Server,
        it doesn't know it's asset id yet,so it will come to the server asks for
        the asset id first,then report the data again  '''

        data = self.request.POST.get("asset_data")
        # response = {}
        if data:  # 如果客户端传过来的asset_data有数据
            try:
                data = json.loads(data)  # 将数据load进来,然后给mandatory_check进行合法性验证
                if self.mandatory_check(data, only_check_sn=True):  # 这个资产已经存在,就会返回True
                    response = {
                        'asset_id': self.asset_obj.id}  # 如果资产在数据库里面存在,则查询资产id. self.asset_obj是从mandatory_check里面传来的
                else:  # 如果资产在数据库中不存在
                    # 在mandatory_check里面定义了self.waiting_approval=True,所以self里面就已经有了waiting_approval属性,这里hasattr检测就会通过
                    if hasattr(self, 'waiting_approval'):
                        response = {'needs_aproval': "你的资产需要管理员审批去创建一个新的资产ID."}
                        self.clean_data = data
                        print(self.clean_data)
                        self.save_new_asset_to_approval_zone()  # 在给客户端返回前,应该先把数据存在待审批区
                        print(response)
                    else:
                        response = self.response
            except ValueError as e:
                print('存入资产失败:', e)
                self.response_msg('error', 'AssetDataInvalid', str(e))
                response = self.response

        else:
            self.response_msg('error', 'AssetDataInvalid', "The reported asset data is not valid or provided")
            response = self.response
        return response

    def save_new_asset_to_approval_zone(self):
        asset_sn = self.clean_data.get('sn')
        # get_or_create代表查找或者创建,也就是说当数据库里面存在这条数据时,我就只是查找数据而不插入,如果不存在则插入数据.
        # 这样做避免了数据被重复创建

        # dic={}
        # dic.update(sn=asset_sn,
        #       data=json.dumps(self.clean_data),
        #       manufactory=self.clean_data.get(
        #           'manufactory'),
        #       model=self.clean_data.get(
        #           'model'),
        #       asset_type=self.clean_data.get(
        #           'asset_type'),
        #       ram_size=self.clean_data.get(
        #           'ram_size'),
        #       cpu_model=self.clean_data.get(
        #           'cpu_model'),
        #       cpu_count=self.clean_data.get(
        #           'cpu_count'),
        #       cpu_core_count=self.clean_data.get(
        #           'cpu_core_count'),
        #       os_distribution=self.clean_data.get(
        #           'os_distribution'),
        #       os_release=self.clean_data.get(
        #           'os_release'),
        #       os_type=self.clean_data.get(
        #           'os_type'),
        #       )
        # print(dic)
        # obj=models.NewAssetApprovalZone.objects.create(**dic)
        #
        # obj.save()

        asset_already_in_approval_zone = models.NewAssetApprovalZone.objects.get_or_create(sn=asset_sn,
                                                                                           data=json.dumps(
                                                                                               self.clean_data),
                                                                                           name=self.clean_data.get('name'),
                                                                                           manufactory=self.clean_data.get(
                                                                                               'manufactory'),
                                                                                           model=self.clean_data.get(
                                                                                               'model'),
                                                                                           asset_type=self.clean_data.get(
                                                                                               'asset_type'),
                                                                                           ram_size=self.clean_data.get(
                                                                                               'ram_size'),
                                                                                           cpu_model=self.clean_data.get(
                                                                                               'cpu_model'),
                                                                                           cpu_count=self.clean_data.get(
                                                                                               'cpu_count'),
                                                                                           cpu_core_count=self.clean_data.get(
                                                                                               'cpu_core_count'),
                                                                                           os_distribution=self.clean_data.get(
                                                                                               'os_distribution'),
                                                                                           os_release=self.clean_data.get(
                                                                                               'os_release'),
                                                                                           os_type=self.clean_data.get(
                                                                                               'os_type'),
                                                                                           )

        return True
    def data_is_valid_without_id(self):
        '''当资产没有id,就走这个函数
        如果是一个新的资产,则将sn存入到asset表里面,如果表里面有该sn的资产,则返回资产对象.
        然后执行强制性检查
        '''

        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)
                print('data:',data)
                #asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn'),name=data.get('sn')) #push asset id into reporting data before doing the mandatory check
                # 待验证,这里应该要有两个值才对,因为name设置了不允许为空,所以如果是新建数据,没有指明name实际上插入会报错.
                asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn'),name=data.get('name')) #push asset id into reporting data before doing the mandatory check
                print(asset_obj)
                data['asset_id'] = asset_obj[0].id      #把asset_id赋值是因为下面要进入mandatory_check检测,这个检测里面会要求必需有该字段
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error','AssetDataInvalid', str(e))
        else:
            self.response_msg('error','AssetDataInvalid', "The reported asset data is not valid or provided")

    def data_inject(self):
        '''在mandatory_check()校验成功后,进入到该函数.
        先判断是否为新资产,如果是新资产就走create,旧资产走update
        该函数调用插入数据的方法,将待审批区的资产正式的插入到每一个表里面
        '''

        #self.reformat_components('slot',self.clean_data.get('ram'))
        #self.reformat_components('name',self.clean_data.get('nic'))
        if self.__is_new_asset():
            print('\033[32;1m---new asset,going to create----\033[0m')
            self.create_asset()
        else:#asset already already exist , just update it
            print('\033[33;1m---asset already exist ,going to update----\033[0m')

            self.update_asset()

    def __is_new_asset(self):
        '''
        如果这是一个新资产,那么这条数据在其它的外键表里面是没有数据的,那么通过外键关联查询就
        查不到数据的.
        如果是一个已有的资产,那么就可以外键关联查询到数据.
        所以,通过hasattr来判断是否有外键关联查询来判断是否为新资产
        self.clean_data['asset_type'] 得到的是server,switch等
        self.asset_obj 得到的是Asset表里面的对象,通过这个对象可以反查关联表里面的数据.
        比如通过这个对象查server表里面的信息,可以这样写:
        self.asset_obj.server.os_type 就能够查到关联server表里面的os_type字段.
        如果server表里面没有这个数据,则会报错,if条件就不存在了.
        Sansa.models.Asset.server.RelatedObjectDoesNotExist: Asset has no server.
        可以如下验证(下面的a[0]就是self.asset_obj):
         from Sansa import models
         a=models.Asset.objects.all()
         a[0].server
         如果关联表没有数据(新资产),则报错Sansa.models.Asset.server.RelatedObjectDoesNotExist: Asset has no server.
         那么hasattr(self.asset_obj, self.clean_data['asset_type'])返回False.
         if not False则成立,return True
         如果有数据,则不会报错 if not True不成立,进入到else条件,所以return False
         综上所述: 如果是新资产,则返回True,如果是旧资产则返回False
        :return:
        '''
        #self.asset_obj为查询出来的asset对象,self.clean_data['asset_type']得到关联表对象名称,如server/switch等
        #也就是查询出来的数据在关联的外键表里面有对应的数据的话,就证明是一个已经插入过的对象,就是旧资产.hasattr返回True
        # hasattr相当于self.asset_obj.server  或者 self.asset_obj.switch 等
        if not hasattr(self.asset_obj, self.clean_data['asset_type']):#new asset
            return True
        else:
            return False

    def create_asset(self):
        '''
        invoke asset create function according to it's asset type
        :return:
        '''
        # 由于资产可能不止server,也可能是switch之类的,所以这里采用反射的方法,匹配到不同的方法
        func = getattr(self,'_create_%s' % self.clean_data['asset_type'])
        create_obj =func()

    def update_asset(self):
        '''更新资产'''
        func = getattr(self,'_update_%s'%self.clean_data['asset_type'])
        update_obj = func()

    def _update_server(self):
        '''调用__updata_asset_component方法,来更新每一张表的数据
        当更新网卡时
        传入self.clean_data['nic']即客户端传过来的网卡数据,
        传入nic_set,即通过asset表反查nic外键关联数据
        传入update_field即我们需要更新的字段.因为表里面有很多字段,有些字段并不需要程序更新的,比如创建时间,备注.所以只更新这里面的字段
        传入macaddress,用这个作为唯一标识,因为客户端网卡可能有多个,用mac地址区分每一条不同数据
        nic/disk/ram三者都有可能每台主机存在多条记录,有一定共性,所以都交给同一个函数处理
        '''
        nic = self.__update_asset_component(data_source=self.clean_data['nic'],
                                            fk='nic_set',
                                            update_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding'],
                                            identify_field = 'macaddress'
                                            )
        disk = self.__update_asset_component(data_source=self.clean_data['physical_disk_driver'],
                                             fk='disk_set',
                                            update_fields = ['slot','sn','model','manufactory','capacity','iface_type'],
                                            identify_field = 'slot'
                                            )
        ram = self.__update_asset_component(data_source=self.clean_data['ram'],
                                             fk='ram_set',
                                            update_fields = ['slot','sn','model','capacity'],
                                            identify_field = 'slot'
                                            )
        cpu = self.__update_cpu_component()
        manufactory = self.__update_manufactory_component()
        server = self.__update_server_component()

    def __update_asset_component(self,data_source,fk,update_fields,identify_field=None):
        '''
        将数据库里面对应的数据和客户端传过来的对应数据都分别拿出来循环,然后根据唯一值identify_field来进行比对,
        如果有相同的唯一值,则证明是同一条数据,那么就执行更新操作.
        如果数据库里面数据没有在传过来的字典里面,则证明客户端该硬件可能已经丢失或损坏了.


        data_source: the data source of this component from reporting data
        fk: which key to use to find the connection between main Asset obj and each asset component
        update_fields: what fields in DB will be compared and updated
        identify_field: use this field to identify each component of an Asset , if set to None,means only use asset id to identify
         '''
        print(data_source,update_fields,identify_field)
        try:
            '''self.asset_obj由来: 先是前端传来待批准资产的id,通过这个id获取到待批准资产的数据,通过这个数据查询到sn号和id号,通过
            sn号查询到asset表里面对应的对象.然后赋值给self.asset_obj. 所以self.asset_obj就是某条需要批准修改的asset表的数据对象.
            '''
            component_obj = getattr(self.asset_obj,fk) #asset_obj.nic_set
            if hasattr(component_obj,'select_related'): # asset_obj.nic_set.select_related
                objects_from_db = component_obj.select_related()    #查询出该资产相关联的网卡信息
                for obj in objects_from_db: #obj即每块网卡对象
                    key_field_data= getattr(obj,identify_field) #从nic表里面查到每块网卡的Mac地址.macaddress =u'40: 8D: 5C: 93: F1: DE'
                    #use this key_field_data to find the relative data source from reporting data
                    if type(data_source) is list:   #这里要求客户端传来的网卡信息为列表形式
                        for source_data_item  in data_source:   #对客户端传来的nic列表进行循环,
                            key_field_data_from_source_data = source_data_item.get(identify_field)  #获取传过来的网卡信息的mac
                            if key_field_data_from_source_data: #有可能客户端传来的数据没有mac地址,所以要先判断是否存在mac地址
                                if key_field_data == key_field_data_from_source_data: #将数据库里面的mac和客户端的mac比较
                                    #如果比对mac相等,调用__compare_componet开始正式的更新操作
                                   self.__compare_componet(model_obj=obj,   #nic表里面的网卡对象
                                                           fields_from_db=update_fields,    #要更新的字段
                                                           data_source=source_data_item)    #客户端的对应的网卡数据
                                   break #must break ast last ,then if the loop is finished , logic will goes for ..else part,then you will know that no source data is matched for by using this key_field_data, that means , this item is lacked from source data, it makes sense when the hardware info got changed. e.g: one of the RAM is broken, sb takes it away,then this data will not be reported in reporting data
                            else: #key field data from source data cannot be none
                                self.response_msg('warning','AssetUpdateWarning',"Asset component [%s]'s key field [%s] is not provided in reporting data " % (fk,identify_field) )

                        else:#触发该else条件证明上面的break没有执行,也就意味着nic表里面的该条网卡资产在客户端数据里面不存在了.可能被偷了?
                            print('\033[33;1mError:cannot find any matches in source data by using key field val [%s],component data is missing in reporting data!\033[0m' %(key_field_data) )
                            self.response_msg("error","AssetUpdateWarning","Cannot find any matches in source data by using key field val [%s],component data is missing in reporting data!" %(key_field_data))
                    else:
                        print('\033[31;1m in _update_asset_component传过来的数据不是列表格式,检测失败.\033[0m')
                #compare all the components from DB with the data source from reporting data
                self.__filter_add_or_deleted_components(model_obj_name=component_obj.model._meta.object_name,   #获取到关联表的表名
                                                        data_from_db=objects_from_db,   #关联表里面关联数据的对象
                                                        data_source=data_source,    #传过来的字典列表
                                                        identify_field=identify_field)  #校验字段

            else:#    this component is reverse fk relation with Asset model
                pass
        except ValueError as e:
            print('\033[41;1m%s\033[0m' % str(e) )

    def __compare_componet(self,model_obj,fields_from_db,data_source):  #网卡对象/更新字段/客户端网卡数据
        '''
        将数据库里面的列和字典里面的列都拿出来进行对比,
        如果列的值不一样,则修改该列的数据.并保存
        :param model_obj:
        :param fields_from_db:
        :param data_source:
        :return:
        '''
        print('---going to compare:[%s]' % model_obj,fields_from_db)
        print('---source data:', data_source)
        for field in fields_from_db: #update fields [name,sn,macaddress,ipaddress...]
            val_from_db = getattr(model_obj,field)  #在nic表查到这个网卡的更新字段的值
            val_from_data_source = data_source.get(field)   #在传过来的网卡信息里面也查到该字段值
            if val_from_data_source:    #如果传来的数据里面有这个值
                #if type(val_from_db) is unicode:val_from_data_source = unicode(val_from_data_source)#no unicode in py3
                #if type(val_from_db) in (int,long):val_from_data_source = int(val_from_data_source) #no long in py3
                # 先根据数据库里面的对应列的数据类型,将客户端传来的值做一个转换.让两者的数据类型保持一致.
                if type(val_from_db) in (int,):val_from_data_source = int(val_from_data_source)
                elif type(val_from_db) is float:val_from_data_source = float(val_from_data_source)
                elif type(val_from_db) is str:val_from_data_source = str(val_from_data_source).strip()
                # 当数据类型一致时,再进行比较.
                if val_from_db == val_from_data_source:# this field haven't changed since last update
                    pass
                    #print '\033[32;1m val_from_db[%s]  == val_from_data_source[%s]\033[0m' %(val_from_db,val_from_data_source)
                else:
                    print('\033[34;1m val_from_db[%s]  != val_from_data_source[%s]\033[0m' %(val_from_db,val_from_data_source),type(val_from_db),type(val_from_data_source) ,field)
                    db_field = model_obj._meta.get_field(field)     #获取到指定nic条目的指定field列对象
                    #下面的语句即修改model_obj表的field列的数据为val_from_data_source.
                    db_field.save_form_data(model_obj, val_from_data_source)    #更新该列数据,注意更新后要model_obj.save()保存才会生效
                    model_obj.update_date = timezone.now()
                    #model_obj.save()   #将里将数据的保存放在了循环完成后再执行,避免了每次循环都要保存一次数据,增加数据库的开销
                    log_msg = "Asset[%s] --> component[%s] --> field[%s] has changed from [%s] to [%s]" %(self.asset_obj,model_obj,field,val_from_db,val_from_data_source)
                    self.response_msg('info','FieldChanged',log_msg)
                    log_handler(self.asset_obj,'FieldChanged',self.request.user,log_msg,model_obj)
            else:
                self.response_msg('warning','AssetUpdateWarning',"Asset component [%s]'s field [%s] is not provided in reporting data " % (model_obj,field) )

        model_obj.save()
    def __update_server_component(self):
        update_fields = ['model','raid_type','os_type','os_distribution','os_release']
        if hasattr(self.asset_obj,'server'):
            self.__compare_componet(model_obj=self.asset_obj.server,
                                    fields_from_db=update_fields ,
                                    data_source=self.clean_data)
        else:
            self.__create_server_info(ignore_errs=True)

    def __update_cpu_component(self):
        update_fields = ['cpu_model','cpu_count','cpu_core_count']
        if hasattr(self.asset_obj,'cpu'):   #如果这个资产条目已经有了cpu,则更新cpu信息.
            self.__compare_componet(model_obj=self.asset_obj.cpu,
                                    fields_from_db=update_fields,
                                    data_source=self.clean_data)
        else:   #如果没有对应的cpu,则创建cpu
            self.__create_cpu_component(ignore_errs=True)

    def __update_manufactory_component(self):
        self.__create_or_update_manufactory(ignore_errs=True)

    def _create_server(self):
        '''调用不同的函数,创建各类数据
        不同的函数插入不同的数据到对应的表里面,实现将数据插入到不同的表之中
        在每一个create函数里面,会有一个verify_field函数用于校验数据的合法性,
        校验通过后,才执行插入数据的操作
        '''
        self.__create_server_info()
        self.__create_or_update_manufactory()
        self.__create_cpu_component()
        self.__create_disk_component()
        self.__create_nic_component()
        self.__create_ram_component()

        log_msg = "Asset [<a href='/admin/assets/asset/%s/' target='_blank'>%s</a>] has been created!" % (self.asset_obj.id,self.asset_obj)
        self.response_msg('info','NewAssetOnline',log_msg )

    def __verify_field(self,data_set,field_key,data_type,required=True):    #field_key='model',data_type=str
        '''根据传进来的数据,或者到数据字典里面的model对应的值,判断这个值必需不为空,
        当不为空时,将get('model')的值 str()转换.如果转换不成功则报错.
        '''
        field_val = data_set.get(field_key)
        if field_val or field_val==0:
            try:
                data_set[field_key] = data_type(field_val)
            except ValueError as e:
                self.response_msg('error','InvalidField', "The field [%s]'s data type is invalid, the correct data type should be [%s] " % (field_key,data_type) )

        elif required == True:
                self.response_msg('error','LackOfField', "The field [%s] has no value provided in your reporting data [%s]" % (field_key,data_set) )

    def __create_server_info(self, ignore_errs=False):
        """创建server表里的相关信息"""
        try:
            self.__verify_field(self.clean_data, 'model', str)  #校验model字段的值,将其强制转换为str格式,只有转换成功才进行下一步
            #如果转换失败或者model的值为空,那么self.response['error'])就不为空.len就不为0.就不满足if not len(xxx)
            if not len(
                    self.response['error']) or ignore_errs == True:  # no processing when there's no error happend
                data_set = {
                    'asset_id': self.asset_obj.id,
                    'raid_type': self.clean_data.get('raid_type'),
                    # 'model':self.clean_data.get('model'),
                    'os_type': self.clean_data.get('os_type'),
                    'os_distribution': self.clean_data.get('os_distribution'),
                    'os_release': self.clean_data.get('os_release'),
                }

                obj = models.Server(**data_set)
                # 这里注意,在asset表里面是没有model字段的,这相当于给obj.asset这个实例赋了个变量model
                obj.asset.model = self.clean_data.get('model')
                obj.save()
                return obj
        except Exception as e:
            self.response_msg('error', 'ObjectCreationException', 'Object [server] %s' % str(e))
    def __create_or_update_manufactory(self,ignore_errs=False):
        '''由于厂商信息是一个外键,而且可以不同的机器共用,所以对于一个新的资产,厂商信息有可能早就已经存在了
            所以先得判断厂商信息是否存在,如果存在,则获取对应数据的厂商信息对象obj
            如果不存在,则创建厂商数据,并获取到该条数据的对象obj.
            将该对象插入到asset表的manufactory字段,即实现asset表与manufactory表的外键的关联.
        '''
        try:
            self.__verify_field(self.clean_data,'manufactory',str)
            manufactory = self.clean_data.get('manufactory')
            if not len(self.response['error']) or ignore_errs == True: #no processing when there's no error happend
                obj_exist = models.Manufactory.objects.filter(manufactory=manufactory)  #在表里面查询传过来的厂商信息
                if obj_exist:   #如果查询到有数据,证明厂商已经在表里面有了
                    obj = obj_exist[0]  #获取到厂商信息,由于厂商表做了uniq唯一约束,所以数据只会出现一条,取[0]即可
                else:   #如果没有
                    obj = models.Manufactory(manufactory=manufactory)   #创建一个厂商,存入厂商表里面
                    obj.save()      #保存厂商表
                self.asset_obj.manufactory = obj    #将资产表的manufactory字段存入Manufactory表的对象,即实现外键关联
                self.asset_obj.save()   #保存资产表
        except Exception as e:
            self.response_msg('error','ObjectCreationException','Object [manufactory] %s' % str(e) )
    def __create_cpu_component(self,ignore_errs=False):
        try:
            self.__verify_field(self.clean_data,'model',str)
            self.__verify_field(self.clean_data,'cpu_count',int)
            self.__verify_field(self.clean_data,'cpu_core_count',int)
            if not len(self.response['error']) or ignore_errs == True: #no processing when there's no error happend
                data_set = {
                    'asset_id' : self.asset_obj.id,
                    'cpu_model': self.clean_data.get('cpu_model'),
                    'cpu_count':self.clean_data.get('cpu_count'),
                    'cpu_core_count':self.clean_data.get('cpu_core_count'),
                }

                obj = models.Cpu(**data_set)
                obj.save()
                log_msg = "Asset[%s] --> has added new [cpu] component with data [%s]" %(self.asset_obj,data_set)
                self.response_msg('info','NewComponentAdded',log_msg)
                return obj
        except Exception as e:
            self.response_msg('error','ObjectCreationException','Object [cpu] %s' % str(e) )
    def __create_disk_component(self):
        disk_info = self.clean_data.get('physical_disk_driver')
        if disk_info:
            for disk_item in disk_info:
                try:
                    self.__verify_field(disk_item,'slot',str)
                    self.__verify_field(disk_item,'capacity',float)
                    self.__verify_field(disk_item,'iface_type',str)
                    self.__verify_field(disk_item,'model',str)
                    if not len(self.response['error']): #no processing when there's no error happend
                        manufactory_obj=models.Manufactory.objects.get_or_create(manufactory=disk_item.get('manufactory'))
                        print(manufactory_obj)
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'sn': disk_item.get('sn'),
                            'slot':disk_item.get('slot'),
                            'capacity':disk_item.get('capacity'),
                            'model':disk_item.get('model'),
                            'iface_type':disk_item.get('iface_type'),
                            'manufactory':manufactory_obj[0],
                        }

                        obj = models.Disk(**data_set)
                        obj.save()

                except Exception as e:
                    self.response_msg('error','ObjectCreationException','Object [disk] %s' % str(e) )
        else:
                self.response_msg('error','LackOfData','Disk info is not provied in your reporting data' )
    def __create_nic_component(self):
        nic_info = self.clean_data.get('nic')
        if nic_info:
            for nic_item in nic_info:
                try:
                    self.__verify_field(nic_item,'macaddress',str)
                    if not len(self.response['error']): #no processing when there's no error happend
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'name': nic_item.get('name'),
                            'sn': nic_item.get('sn'),
                            'macaddress':nic_item.get('macaddress'),
                            'ipaddress':nic_item.get('ipaddress'),
                            'bonding':nic_item.get('bonding'),
                            'model':nic_item.get('model'),
                            'netmask':nic_item.get('netmask'),
                        }

                        obj = models.Nic(**data_set)
                        obj.save()

                except Exception as e:
                    self.response_msg('error','ObjectCreationException','Object [nic] %s' % str(e) )
        else:
                self.response_msg('error','LackOfData','NIC info is not provied in your reporting data' )
    def __create_ram_component(self):
        ram_info = self.clean_data.get('ram')
        if ram_info:
            for ram_item in ram_info:
                try:
                    self.__verify_field(ram_item,'capacity',int)
                    if not len(self.response['error']): #no processing when there's no error happend
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'slot': ram_item.get("slot"),
                            'sn': ram_item.get('sn'),
                            'capacity':ram_item.get('capacity'),
                            'model':ram_item.get('model'),
                        }

                        obj = models.Ram(**data_set)
                        obj.save()

                except Exception as e:
                    self.response_msg('error','ObjectCreationException','Object [ram] %s' % str(e) )
        else:
                self.response_msg('error','LackOfData','RAM info is not provied in your reporting data' )

    def __filter_add_or_deleted_components(self,model_obj_name,data_from_db,data_source,identify_field):
        '''该函数用于处理新增或删除资产
        model_obj_name  关联表的表名,比如nic
        data_from_db    关联表里面查询出来的对象
        data_source     客户端传来的关联数据,比如网卡数据列表
        identify_field  校验字段
        '''
        '''This function is filter out all  component data in db but missing in reporting data, and all the data in reporting data but not in DB'''
        print(data_from_db,data_source,identify_field) #关联表里面的数据对象,传过来的数据列表,校验字段
        data_source_key_list = [] #save all the idenified keys from client data,e.g: [macaddress1,macaddress2]
        if type(data_source) is list:   #如果是列表,就对数据循环,并取出列表里面每个字典里面对应的校验字段的值
            for data in data_source:
                data_source_key_list.append(data.get(identify_field))
        # elif type(data_source) is dict:
        #     for key,data in data_source.items():
        #         if data.get(identify_field):
        #             data_source_key_list.append(data.get(identify_field))
        #         else:#workround for some component uses key as identified field e.g: ram
        #             data_source_key_list.append(key)
        print('-->identify field [%s] from data source  :',data_source_key_list)
        print('-->identify[%s] from db:',[getattr(obj,identify_field) for obj in data_from_db] )

        data_source_key_list = set(data_source_key_list)    #把传来的对应字段的列表转为集合

        data_identify_val_from_db = set([getattr(obj,identify_field) for obj in data_from_db])  #查询库里面关联行对应字段的值

        data_only_in_db= data_identify_val_from_db - data_source_key_list #delete all this from db  求差集,如果有值,证明db数据多了
        data_only_in_data_source=  data_source_key_list - data_identify_val_from_db #add into db
        print('\033[31;1mdata_only_in_db:\033[0m' ,data_only_in_db)
        print('\033[31;1mdata_only_in_data source:\033[0m' ,data_only_in_data_source)
        self.__delete_components(all_components=data_from_db,
                                 delete_list = data_only_in_db,
                                 identify_field=identify_field )
        if data_only_in_data_source: #add data in to db
            self.__add_components(model_obj_name=model_obj_name,
                                  all_components=data_source,
                                  add_list = data_only_in_data_source,
                                  identify_field=identify_field )

    def __delete_components(self,all_components, delete_list , identify_field ):
        '''All the objects in delete list will be deleted from DB'''
        deleting_obj_list = []
        print('--deleting components',delete_list,identify_field)
        for obj in all_components:
            val  = getattr(obj,identify_field)
            if val in delete_list:
                deleting_obj_list.append(obj)

        for i in deleting_obj_list:
            log_msg = "Asset[%s] --> component[%s] --> is lacking from reporting source data, assume it has been removed or replaced,will also delete it from DB" %(self.asset_obj,i)
            self.response_msg('info','HardwareChanges',log_msg)
            log_handler(self.asset_obj,'HardwareChanges',self.request.user,log_msg,i)
            i.delete()

    def __add_components(self,model_obj_name,all_components,add_list,identify_field ):
        '''
        新增资产到数据库里面.
        :param model_obj_name: 为关联表的类名,如Nic  来源于:component_obj.model._meta.object_name
        :param all_components: 客户端传来的对应模块的数据列表
        :param add_list:    客户端多出来的数据标识,即要添加的数据,注意这里不是完整的数据,只是一个标识,如mac地址
        :param identify_field:  校验字段
        :return:
        '''
        model_class = getattr(models,model_obj_name)    #eg: models.nic
        will_be_creating_list = []
        print('--add component list:',add_list)
        if type(all_components) is list:
            for data in all_components: #对传来的数据列表循环
                if data[identify_field] in add_list:    #从传过来的列表数据里面查找,找到多出来的那部分数据
                    #print data
                    will_be_creating_list.append(data)
        try:
            for component in will_be_creating_list: #对这部分要添加的数据进行循环
                data_set = {}
                '''这里的auto_create_fields是在创建models的时候在各个类里面定义的,如我们在models的Nic类里面就定义了
                    auto_create_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding']
                    所以能够通过Nic.auto_create_fields来获得这个字段的列表.
                    这样做的目的在于,我们对每一个表并不是所有的字段都需要更新的,所以我们先在每一个models类里面就定义
                    好这个变量来决定哪些字段是需要更新的,这样下次更新表的时候,就可以直接从这个变量里面读对应的列名,
                    免得每次写更新代码时一个个字段都要写,那这样可以减少很多代码量,处理起来也更加灵活.
                '''
                for field in model_class.auto_create_fields:
                    data_set[field] = component.get(field)  #生成一个字典,Key就是列名,value就是从客户端数据(component)里面取到的对应列名的数据

                if 'manufactory' in data_set:
                    manufactory_obj=models.Manufactory.objects.get_or_create(manufactory=component.get('manufactory'))
                    if manufactory_obj[0]:
                        data_set['manufactory']=manufactory_obj[0]
                data_set['asset_id'] = self.asset_obj.id    #每个关联表里面都会有一个外键列asset_id,要给这个列加入对应的id,这样才能实现和asset表的外键关联
                obj= model_class(**data_set)    #将字典数据传入到这个model类里面,即将数据插入到表里面
                obj.save()
                print('\033[32;1mCreated component with data:\033[0m', data_set)
                log_msg = "Asset[%s] --> component[%s] has justed added a new item [%s]" %(self.asset_obj,model_obj_name,data_set)
                self.response_msg('info','NewComponentAdded',log_msg)
                log_handler(self.asset_obj,
                            'NewComponentAdded',
                            self.request.user,
                            log_msg,
                            model_obj_name)

        except Exception as e:
            print("\033[31;1m %s \033[0m"  % e )
            log_msg = "Asset[%s] --> component[%s] has error: %s" %(self.asset_obj,model_obj_name,str(e))
            self.response_msg('error',"AddingComponentException",log_msg)

def log_handler(asset_obj,event_name,user,detail,component=None):
    '''
    将日志数据存入到数据库里面去
        (1,u'硬件变更'),
        (2,u'新增配件'),
        (3,u'设备下线'),
        (4,u'设备上线'),'''
    log_catelog = {
        #  这里的1,2要与models.py里面定义的eventlog里面定义的event_type_choice.类型一致
        1 : ['FieldChanged','HardwareChanges'],
        2 : ['NewComponentAdded'],
    }
    if not user.id:
        user = models.UserProfile.objects.filter(is_admin=True).last()
    event_type = None
    for k,v in log_catelog.items():
        if event_name in v:
            event_type = k
            break
    log_obj = models.EventLog(
        name =event_name,
        event_type = event_type,
        asset_id = asset_obj.id,    #在eventlog表里面是外键,所以是asset_id.
        component = component,
        detail = detail,
        user_id = user.id
    )

    log_obj.save()
