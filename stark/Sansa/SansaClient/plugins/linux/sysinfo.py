#!/usr/bin/env python3
# Auther: sunjb
import subprocess, os, re


def collect():
    '''
    调用操作系统的dmidecode命令,获取到系统信息,并根据提供的filter_keys里面的字段,进行grep过滤
    出需要的数据,将生成的数据添加到raw_data字典里面
    '''
    filter_keys = ['Manufactuer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
    raw_data = {}
    for key in filter_keys:
        try:
            cmd_res = subprocess.run('dmidecode -t system|grep %s' % (key), shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            cmd_res = cmd_res.stdout.decode().strip()

            res_to_list = cmd_res.split(':')
            if len(res_to_list) > 1:
                raw_data[key] = res_to_list[1].strip()
            else:
                raw_data[key] = -1
        except Exception as e:
            print('collect执行出错了:', e)
            raw_data[key] = -2
    # 这个写死用于区分这是什么数据,这里是服务器的数据,所以写的server,如果是网络设备,就写其它的值
    data = {'asset_type': 'server'}
    data['manufactory'] = raw_data['Manufactuer']
    data['sn'] = raw_data['Serial Number']
    data['model'] = raw_data['Product Name']
    data['uuid'] = raw_data['UUID']
    data['wake_up_type'] = raw_data['Wake-up Type']

    data.update(cpuinfo())
    data.update(osinfo())
    data.update(raminfo())
    data.update(nicinfo())
    return data


def diskinfo():
    obj = DiskPlugin()
    return obj.liunx()


def nicinfo():
    raw_data = subprocess.getoutput('ifconfig -a')  # 得到返回结果,以\n将结果进行分隔
    raw_data = raw_data.split('\n')  # 得到列表形式的命令结果
    nic_dic = {}
    next_ip_line = False
    last_mac_addr = None
    for line in raw_data:
        if next_ip_line:
            next_ip_line = False
            nic_name = last_mac_addr.splict()[0]
            mac_addr = last_mac_addr.split('ether')[1].strip()
            raw_ip_addr = line.split('inet')
            raw_bcast = line.split('broadcast')
            raw_netmask = line.split('netmask')
            if len(raw_ip_addr) > 1:
                ip_addr = raw_ip_addr[1].split()[0]
                network = raw_bcast[1].split()[0]
                netmask = raw_netmask[1].split()[0]
            else:
                ip_addr = None
                netmask = None
                network = None
            if mac_addr not in nic_dic:
                nic_dic[mac_addr] = {'name': nic_name,
                                     'macaddress': mac_addr,
                                     'netmask': netmask,
                                     'network': network,
                                     'bounding': 0,
                                     'model': 'unknown',
                                     'ipaddress': ip_addr}
            else:
                if f'{mac_addr}_bonding_addr' not in nic_dic:
                    random_mac_addr = f'{mac_addr}_bonding_addr'
                else:
                    random_mac_addr = f'{mac_addr}_bonding_addr2'
                nic_dic[random_mac_addr] = {
                    'name': nic_name,
                    'macaddress': random_mac_addr,
                    'netmask': netmask,
                    'network': network,
                    'bounding': 1,
                    'model': 'unknown',
                    'ipaddress': ip_addr,
                }
            next_ip_line = True
            last_mac_addr = line
    nic_list = []
    for k, v in nic_dic.items():
        nic_list.append(v)
    return {'nic': nic_list}


def raminfo():
    raw_data = subprocess.getoutput('dmidecode -t 17')  # 取内存
    raw_list = raw_data.split('\n')
    raw_ram_list = []
    item_list = []
    for line in raw_list:
        if line.startswith('Memory Device'):
            raw_ram_list.append(item_list)
            item_list = []
        else:
            item_list.append(line.strip())
    ram_list = []
    for item in raw_ram_list:
        item_ram_size = 0
        ram_item_to_dic = {}
        for i in item:
            data = i.split(':')
            if len(data) == 2:
                key, v = data
                if key == 'Size':
                    if v.strip() != 'No Module Installed':
                        ram_item_to_dic['capacity'] = v.split()[0].strip()
                        item_ram_size = int(v.split()[0])
                    else:
                        ram_item_to_dic['capacity'] = 0
                if key == 'Type':
                    ram_item_to_dic['model'] = v.strip()
                if key == 'Serial Number':
                    ram_item_to_dic['sn'] = v.strip()
                if key == 'Manufacturer':
                    ram_item_to_dic['manufactory'] = v.strip()
                if key == 'Asset Tag':
                    ram_item_to_dic['asset_tag'] = v.strip()
                if key == 'Locator':
                    ram_item_to_dic['slot'] = v.strip()
        if item_ram_size == 0:
            pass
        else:
            ram_list.append(ram_item_to_dic)
    raw_total_size = subprocess.getoutput('cat /proc/meminfo |grep MemTotal')
    ram_data = {'ram': ram_list}
    if len(raw_total_size) == 2:
        total_mb_size = int(raw_total_size[1].split()[0] / 1024)
        ram_data['ram_size'] = total_mb_size
    return ram_data


def osinfo():
    distributor = subprocess.getoutput('lsb_release -a|grep Distributor')
    release = subprocess.getoutput('lsb_release -a|grep Description')
    data_dic = {
        'os_distribution': distributor[1].strip() if len(distributor) > 1 else None,
        'os_release': release[1].strip() if len(release) > 1 else None,
        'os_type': 'linux',
    }
    return data_dic


def cpuinfo():
    base_cmd = 'cat /proc/cpuinfo'
    raw_data = {
        'cpu_model': f'{base_cmd}|grep "model name"|head -1',
        'cpu_count': f'{base_cmd}|grep "cpu cores"|head -1|wc -l',
        'cpu_core_count': "%s|grep processor|tail -1|awk -F: '{print $2+=1}'" % (base_cmd),
    }
    for k, cmd in raw_data.items():
        try:
            cmd_res = subprocess.getoutput(cmd)
            raw_data[k] = cmd_res.strip()
        except ValueError as e:
            print(e)
    data = {
        'cpu_count': raw_data['cpu_count'],
        'cpu_core_count': raw_data['cpu_core_count']
    }
    cpu_model = raw_data['cpu_model'].split(':')
    if len(cpu_model) > 1:
        data['cpu_model'] = cpu_model[1].strip()
    else:
        data['cpu_model'] = -1
    return data


class DiskPlugin(object):
    def linux(self):
        result = {'physical_disk_driver': []}
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
            shell_command = f'{script_path}/MegaCli -PDList -aALL'
            output = subprocess.getstatusoutput(shell_command)
            result['physical_disk_driver'] = self.parse(output[1])
        except Exception as e:
            print(e)

    def parse(self, content):
        '''
        解析shell命令的返回结果
        :param content: 传来的shell命令
        :return: 返回后的结果
        '''
        response = []
        result = []
        for row_line in content.split('\n\n\n\n'):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            for row in item.split('\n'):
                # 如果数据是空的,那么if not null就成立了,就continue到下一次循环,也就是说如果数据为空,则进入下次循环
                if not row.strip():
                    continue
                # 如果格式不是xx:xx格式的,也跳到下一次循环
                if len(row.split(':')) != 2:
                    continue
                key, value = row.split(':')
                name = self.mega_patter_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)'.value.strip())
                        if raw_size:
                            temp_dict[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        temp_dict[name] = value.strip()
            if temp_dict:
                response.append(temp_dict)
        return response

    def mega_patter_match(self, needle):
        grep_patten = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquire': 'inquire'}
        for key, value in grep_patten.items():
            if needle.startswith(key):
                pass
