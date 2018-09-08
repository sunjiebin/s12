#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
from conf import action_registers
from modules import utils

def help_msg():
    print('\033[31:1mAvailable commands:\033[0m')
    for key in action_registers.actions:
        print('\t',key)

def excute_from_command_line(argvs):
    if len(argvs) < 2:
        help_msg()
        exit()
    if argvs[1] not in action_registers.actions:
        utils.print_err("Command [%s] does not exist!" % argvs[1], quit=True)
    '''actions[argvs[1]]中通过key(argvs[1])获取到actions字典的value，再对获取的value进行调用，调用的参数为(argvs[1:])
    由于actions里面写的value是一个方法，而不是字符串，所以是能够用()调用的，argvs[1:]代表传入的第二个及以后的值作为参数'''
    action_registers.actions[argvs[1]](argvs[1:])