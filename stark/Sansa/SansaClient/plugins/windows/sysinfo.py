#!/usr/bin/env python3
# Auther: sunjb
import subprocess,os,platform
# wmi用于windows的硬件信息收集,依赖于WMI包,wmi同时依赖于pypiwin32
# win32com用于执行一些windows指令,依赖于pypiwin32包
import win32com,wmi
def collect():
    #生成汇报给服务器端的字典data
    data={
        'os_type':platform.system(),
        'os_release':f'{platform.release(),platform.architecture()[0],platform.version()}',
        'os_distribution':'Microsoft',
        'asset_type':'server',
    }
    '''
    对data字典进行update更新以及合并,update()里面可以直接接字典,实现对date的更新以及新增.
    如果传入的key字段和原字典里面的一样,那么则实现更新该key的value,如果key/value不存在,那么就新增该键值对.
    所以win32obj.get_cpu_info()返回的肯定是一个字典.
    调用不同的方法去获取主机的cpu/ram/disk等信息,并更新data字典
    '''
    win32obj=Win32Info()
    data.update(win32obj.get_cpu_info())
    data.update(win32obj.get_ram_info())
    data.update(win32obj.get_server_info())
    data.update(win32obj.get_disk_info())
    data.update(win32obj.get_nic_info())

    return data

class Win32Info(object):
    def __init__(self):
        '''创建一个windows api的连接,连上windows的win32 api接口,调用windows的应用查询数据都是通过这个来的'''
        self.wmi_obj=wmi.WMI()
        self.wmi_service_obj = win32com.client.Dispatch('WbemScripting.SWbemLocator')
        self.wmi_service_connector =self.wmi_service_obj.ConnectServer(".","root\cimv2")

    def get_cpu_info(self):
        data={}
        cpu_lists=self.wmi_obj.Win32_Processor()    #拿到cpu的相关信息对象
        cpu_core_count=0
        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores #cpu的核数
            cpu_model = cpu.Name    #cpu名字
        data['cpu_count']=len(cpu_lists)    #物理cpu个数,我这里是1个
        data['cpu_model']=cpu_model #cpu名字
        data['cpu_core_count']=cpu_core_count   #cpu核心数
        # print('get_cpu_info:',data)
        return data
    def get_ram_info(self):
        '''
        获取内存,由于内存可以有多条,所以这里先弄了个data列表,然后循环后将每一条内存的信息append到列表
        里面,所以最后的data就是列表里面多个字典,每一个字典就是一根内存信息
        :return:
        '''
        data=[]
        ram_collections=self.wmi_service_connector.ExecQuery("Select * from Win32_PhysicalMemory")
        #print('ram_collections',ram_collections)
        for item in ram_collections:
            mb=int(1024*1024)
            ram_size=int(item.Capacity)/mb
            item_data={
                'slot':item.DeviceLocator.strip(),
                'capacity':ram_size,
                'model':item.Caption,
                'manufactory':item.Manufacturer,
                'sn':item.SerialNumber,
            }
            data.append(item_data)
        return {'ram':data}     #由于我们前面要update字典,所以传过去的必需是字典形式
    def get_server_info(self):
        computer_info = self.wmi_obj.Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = {}
        data['manufactory'] = computer_info.Manufacturer
        data['model'] = computer_info.Model
        data['wake_up_type'] = computer_info.WakeUpType
        data['sn'] = system_info.SerialNumber
        # print data
        return data
    def get_disk_info(self):
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():
            #print  disk.Model,disk.Size,disk.DeviceID,disk.Name,disk.Index,disk.SerialNumber,disk.SystemName,disk.Description
            item_data = {}
            iface_choices = ["SAS","SCSI","SATA","SSD","WDC"]
            for iface in iface_choices:
                if iface in disk.Model:
                    item_data['iface_type']  = iface
                    break
            else:
                item_data['iface_type']  = 'unknown'
            item_data['slot']  = disk.Index
            item_data['sn']  = disk.SerialNumber
            item_data['model']  = disk.Model    #型号,华为这台电脑显示的是WDC
            item_data['manufactory']  = disk.Manufacturer   #制造商,笔记本上没有显示制造商
            item_data['capacity']  = int(disk.Size ) / (1024*1024*1024)
            data.append(item_data)
        return {'physical_disk_driver':data}
    def get_nic_info(self):
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = {}
                item_data['macaddress'] = nic.MACAddress
                item_data['model'] = nic.Caption
                item_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    item_data['ipaddress'] = nic.IPAddress[0]
                    item_data['netmask'] = nic.IPSubnet
                else:
                    item_data['ipaddress'] = ''
                    item_data['netmask'] = ''
                bonding = 0
                # print nic.MACAddress ,nic.IPAddress,nic.ServiceName,nic.Caption,nic.IPSubnet
                # print item_data
                data.append(item_data)
        return {'nic': data}

if __name__ == '__main__':
    collect()