#!/usr/bin/env python3
# Auther: sunjb

import wmi
myWmi= wmi.WMI()
for cls in myWmi.classes:
    #print(cls) #打印所有支持的方法

    cpuArr = myWmi.Win32_Processor()

    for cpu in cpuArr:
        print('cpu:', cpu.loadPercentage, cpu.numberOfCores, cpu.name, cpu.maxClockSpeed/1000)
