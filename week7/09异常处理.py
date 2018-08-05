#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''异常处理，程序出错时会抛出有规律的报错，
如字典key找不到会招聘KeyError
列表的索引找不到会抛出IndexError
当程序遇到错误时，则不会执行下面的函数
exception是抓不到缩进错误，语法错误的，因为当
代码语法有问题时，代码根本不能被编译执行，
try本身也是代码，是建立在语法正确的
基础上的，所以无法捕获。
'''
name=['alex','jack']
data={}

try:
    name[3]
    data['name']
except KeyError as e:
    print('没有这个key',e)
except IndexError as e:
    print('列表错误',e)

'''将错误类型写到一个except里面'''
try:
    name[3]
    data['name']
except (KeyError,IndexError) as e:
    print('字典或列表错误',e)

'''不管什么错，只要有错就执行下面print'''
try:
    name[3]
    data['name']
except Exception as e:
    print('出错了',e)

'''可以三者结合用'''
try:
    #name[3]
    #data['nasdf']
    #open('aaa.tt')
    #os.system('ls')
    pass
except (KeyError,IndexError) as e:
    print('字典或列表错',e)
except IOError:
    print('IO错误')
except Exception as e:
    print('未知错误',e)
else:
    print('前面都没错时，则执行，表示一切正常')
finally:
    print('不管有错没有错，均执行')

'''自定义异常'''
'''定义一个可以自传错误信息的异常，
msg即自己传的异常内容'''
class SunError(Exception):
    def __init__(self,msg):
        self.msg=msg
'''定义一个固定报错的异常'''
class MiError(Exception):
    def __str__(self):
        return '脑子已经被烧坏'

'''raise用于调用异常，当用raise调用异常后，
就能够被exception捕获到'''
def aa(name):

    if name == 'mi':
        raise SunError('非法的参数%s'%name)
    else:
        print('aa laila')

def bb():
    print('烧坏前')
    raise MiError()
    '''当raise调用异常后，相当于程序出错了，下面的语句则不会被执行'''
    print('烧坏后')

try:
    aa('mi')
    bb()
    #raise SunError('数据库连接失败')
except SunError as e:
    print('自定义异常出现',e)
except MiError as e:
    print('MiError',e)

'''assert断言用于判断字符类型是否为指定的类型，如果是的则通过继续
执行下面的语句，如果不是的，则报错，下面的语句中断执行
这个功能和if判断类似，只是写法更简洁点'''
num=15
assert type(num) is int
print(num/2)
assert type(num) is str
print('num is str?')