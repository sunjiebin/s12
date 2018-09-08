#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import  os,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from modules.actions import excute_from_command_line
    excute_from_command_line(sys.argv)