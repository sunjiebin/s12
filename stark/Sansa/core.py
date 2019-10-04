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
        #self.asset_obj为asset对象,self.clean_data['asset_type']得到关联表对象名称,如server/switch等
        if not hasattr(self.asset_obj, self.clean_data['asset_type']):#new asset
            return True
        else:
            return False
    def data_inject(self):
        '''save data into DB,the data_is_valid() must returns True before call this function'''

        #self.reformat_components('slot',self.clean_data.get('ram'))
        #self.reformat_components('name',self.clean_data.get('nic'))
        if self.__is_new_asset():
            print('\033[32;1m---new asset,going to create----\033[0m')
            self.create_asset()
        else:#asset already already exist , just update it
            print('\033[33;1m---asset already exist ,going to update----\033[0m')

            self.update_asset()