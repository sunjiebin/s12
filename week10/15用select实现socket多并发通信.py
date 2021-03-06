#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import select,socket,queue
server=socket.socket()
server.bind(('localhost',6900))
server.listen(1000)
server.setblocking(False)   #开启非阻塞模式，即没有数据传过来时不等待

inputs=[server,]    #select.select第一次监听时，要监听一个实例，首次运行时，监听server自己这个实例。
'''inputs在客户端第一次连时里面只有server，当建立连接后，会在inputs里面追加conn进来，所以后面
再循环时，inputs里面可能就有server和conn，这时候哪个活跃select就会返回哪个
当select再返回一个server时，代表此时又有新的客户端连进来，这时候我们会将新的conn2再次append到
inputs里面。
当select返回的不是server,而是conn时，代表这是一个已经建立好连接的客户端发送数据过来了。这时候
应该交给conn.recv来负责接收数据，而不是建立连接。
'''
#inputs=[server,conn,conn2,]
msg_dic={}
outputs=[]
'''进来的连接会输出到readable,出现的异常会输出到excepptional
select.select()里面会接三个参数
第一个inputs：你想让内核参数给你监听哪些连接，就比如你要监听100个连接，只要有一个活的就返回数据，
inputs是你要监听的列表。
第二个outputs: 这个是用来接收返回值的,就是你向outputs里面输入什么，它就会监测到并返回什么
第三个inputs:这个是用来监测异常的，比如我有100个连接，你想知道哪5个断了就是在这里写。
由于我们也需要监控这100个连接的异常，所以我们也需要将inputs写在这里。代表监测inputs列表
里面的异常
'''
'''当select监测到有数据到来时，会返回三个数据
readable是活动的数据列表，一开始新来的连接就会返回在这里。
writeable 是监测outputs的输入，当outputs里面输入数据时，select会立刻监测到，并输出到这个变量
exceptional 这个代表有异常的就会出现在这里，比如100个连接有2个异常了，就会输出到这个变量里面（未验证）
'''
while True:     #我们需要让select循环监听，如果不用while循环，那么程序触发一次就结束了，不会持续监听
    readable,writeable,exceptional=select.select(inputs,outputs,inputs)
    print(readable,writeable,exceptional)
    # conn, addr = server.accept()
    # print(conn, addr)
    for r in readable:
        if r is server: #代表来了一个新连接，注意这里是is,不是=，因为server是一个实例。
            conn,addr=server.accept()
            print('来了个新连接',addr)
            # print(conn,addr)
            '''由于我们前面使用了非阻塞模式，所以不会等待客户端传数据过来，这时候我们如果用conn.recv收数据，
            则会报错，因为此时客户端并没有传数据过来'''
            #print('recieve data:',conn.recv(1024))
            '''所以此时我们应该把建立好连接的实例conn也加入到select的监听中，这样当有这个conn监听实例有数据
            传过来时，再利用select立即通知程序来接收数据'''
            '''这样做是因为新建立的连接还没有数据发送过来，现在立马就接收的话会报错，所以要实现客户端发数据
            过来时server能够立马知道，就需要用select再监测这个conn实例'''
            inputs.append(conn)
            '''将建立好的连接放入一个字典的key里面，value为一个队列'''
            msg_dic[conn]=queue.Queue()
        else:
            '''try语句是为了解决windows下，当客户端断开连接时，程序会直接抛出异常，利用try捕获异常，并清除客户端连接'''
            try:
                data=r.recv(1024)
                print(data)
                '''if语句是为了解决在linux下，当客户端断开连接时，data会为空，而不会抛异常，此时server则需要清除客户端连接数据'''
                if data:
                    print('收到数据',data)
                    msg_dic[r].put(data)
                    #r.send(data)
                    #print('发送成功',data)
                    outputs.append(r)
                else:
                    print('客户端断开连接',r)
                    if r in outputs:
                        outputs.remove(r)
                    inputs.remove(r)
                    r.close()
                    del msg_dic[r]
            except Exception as e:  #处理windows下客户端断开后的异常
                print(e)
                print('客户端断开连接',r)
                if r in outputs:
                    outputs.remove(e)
                r.close()
                inputs.remove(r)
                del msg_dic[r]

    for w in writeable: #要返回给客户端的连接列表
        print('测试')
        send_data=msg_dic[w].get()
        w.send(send_data)
        outputs.remove(w)   #确保下次循环时不再返回已经返回过的数据
        print('发送成功',send_data)
    '''注意下面这段exceptional代码实际上一直不会被执行，不管在哪个环境下，
    客户端断开连接都不会触发exceptional，所以这个有什么用至今未知'''
    for e in exceptional:
        print(e)
        if e in outputs:
            outputs.remove(e)
        e.close()
        inputs.remove(e)
        del msg_dic[e]