#!/usr/bin/env python3
# Auther: sunjb
import json
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
                asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn')) #push asset id into reporting data before doing the mandatory check
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