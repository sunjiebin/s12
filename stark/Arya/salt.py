#!/usr/bin/env python3
# Auther: sunjb

import os
import django
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stark.settings')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(BASE_DIR,sys.path)
    # 将stark加入到运行的环境变量中,如果不加，会导致无法通过from Arya导入模块，因为Arya的上级stark没有在环境变量中,所以直接写Arya会找不到这个目录
    # 提示错误：ModuleNotFoundError: No module named 'Arya'
    sys.path.append(BASE_DIR)
    django.setup()
    # print(sys.path)
    from Arya.backends.utils import ArgvManagement
    obj=ArgvManagement(sys.argv)
    obj.argv_parse()


if __name__ == '__main__':
    main()
