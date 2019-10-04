#!/usr/bin/env python3
# Auther: sunjb

from plugins.linux import sysinfo


def LinuxSysInfo():
    return sysinfo.collect()

def WindowsSysInfo():
    """
    下面的模块应该写在这个类里面,而不是写在脚本最上面,这样就只有当系统是windows的时候才会import这个模块
    如果写在最上面,那么在Linux系统下也会执行该import命令,但是这个模块导入会依赖一些widnows的包,而在Linux
    下是没有这些包的,那么就会导致在linux下导入模块报错,脚本就没法运行了
    """
    from plugins.windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()