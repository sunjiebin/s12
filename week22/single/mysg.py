from django import dispatch

single=dispatch.Signal(providing_args=['arg1','arg2'])

def func(sender,**kwargs):
    print('进入自定义信号')
    print(sender,kwargs)
    return kwargs
single.connect(func)
