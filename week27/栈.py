#!/usr/bin/env python3
# Auther: sunjb

stack=[1,2,3,4,5]
#栈：就像是一堆叠起来的东西，你只能往这个堆上面一层层的添加和取东西。最后添加的东西最先被取出。
#一个列表也就是一个栈，栈是后进先出的。如我们append一个数，再pop。
#查看栈底，即列表的最后一个元素
print(stack[-1])



def check_kuohao(s):
    '''
    一个判断输入括号语法是否正确的函数,正反括号必须是相邻的
    []4() True
    [li]( False
    []) False
    )() False


    '''
    stack=[]
    dic={'{':'}','[':']','(':')'}
    for i in s:
        if i in dic.keys():         #如果字符里面有左括号，则添加到stack列表里面
            stack.append(i)
        for k,v in dic.items():     #k,v是一对括号
            if i == v:              #如果是任意右括号
                if len(stack)>0 and stack[-1] == k:     #列表里面要有元素,即出现右括号前必须现有左括号，且最后一个元素为对应的左括号
                    stack.pop()     #如果上面的条件成立，即最后一个元素是对应的左括号，那么将最后的左括号取出来
                else:
                    return False    #如果列表为空，或者最后一个元素不是对应的左括号，那么返回False
    if len(stack)==0:               #当上面的循环完成后，如果stack为空，代表所有的括号都被匹配了，那就证明匹配成功
        return True
    else:
        return False                #当上面的循环完成后，如果还有剩下的符号，那证明最后一个是个左括号，没有右括号匹配

print(check_kuohao('()8(*)'))

from collections import deque

queue = deque()
queue.append(1)
queue.append(2)
print(queue.popleft())      #出1  后进先出


#链表
class  Node(object):
    def __init__(self,item=None):
        self.item=item
        self.next=None
a=Node(10)
a.next=Node(20)
a.next.next=Node(30)
print(a.next.next.item)
#单链表尾插法
def createlinklistr(li):
    l=Node()
    r=l
    for num in li:
        s=Node(num)
        r.next=s
        r=s
#  #删除
# def linkdel(curNode):
#      p=curNode.next
#      curNode.next=curNode.next.next
#      del p

#遍历链表
def traversal(head):
    curNode=head
    while curNode is not None:
        print(curNode.item)
        curNode=curNode.next
#给链表赋值,10-->20--30
head=Node(10)
b=Node(20)
c=Node(30)
head.next=b
b.next=c
traversal(head)

#双链表
class  Node(object):
    def __init__(self,item=None):
        self.item=item
        self.next=None
        self.prior=None
#双链表尾插法
def createlinkR(li):
    l=Node()
    r=l
    for num in li:
        s=Node(num)
        r.next=s
        s.prior=r
        r=s
    return l,r


