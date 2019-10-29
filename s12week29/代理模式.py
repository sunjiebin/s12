#!/usr/bin/env python3
# Auther: sunjb

#
# 代理模式
# 应用特性：需要在通信双方中间需要一些特殊的中间操作时引用，多加一个中间控制层。
# 结构特性：建立一个中间类，创建一个对象，接收一个对象，然后把两者联通起来
'''
agent_class就是一个代理，我们要在原来的类send_class前面加点操作，而又不想改变send_class代码，那么就可以
这么写，比如我们在agent_class里面做了一个print操作，然后再执行send_class。
'''
class sender_base:
    def __init__(self):
        pass

    def send_something(self, something):
        pass


class send_class(sender_base):
    def __init__(self, receiver):
        self.receiver = receiver

    def send_something(self, something):
        print("SEND " + something + ' TO ' + self.receiver.name)


class agent_class(sender_base):
    def __init__(self, receiver):
        '''先将send_class实例化'''
        self.send_obj = send_class(receiver)

    def send_something(self, something):
        '''增加一个print操作,然后执行send_class实例'''
        print('agent_send_something')
        self.send_obj.send_something(something)


class receive_class:
    def __init__(self, someone):
        self.name = someone


if '__main__' == __name__:
    receiver = receive_class('Alex')
    agent = agent_class(receiver)
    agent.send_something('agentinfo')

    print(receiver.__class__)
    print(agent.__class__)