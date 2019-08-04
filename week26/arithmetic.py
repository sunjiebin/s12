import random,copy,sys

def fun(x):
    if x>0:
        fun(x-1)
        print(x)

#fun(5)      #返回1,2,3,4,5

def timmer(func):
    def wrappen(*args,**kwargs):
        import time
        starttime=time.time()
        result=func(*args,**kwargs)
        endtime=time.time()
        print('total time',endtime-starttime)
        return result
    return wrappen



#递归查找，时间很久
@timmer
def line_search(data_set,value):
    for i in data_set:
        # print(i)
        if i == value:
            return (i)
    return ('递归完毕')

# 二分查找，速度快很多倍
@timmer
def bin_search(data_set,value):
    low=0
    high=len(data_set)-1
    while low<=high:
        mid=(low+high)//2
        if data_set[mid] == value:
            return mid
        elif data_set[mid]>value:
            high=mid-1
        else:
            low=mid+1

#使用这两个算法要注意，首先输入的基数要大，然后要查找的值要大，这样才会循环足够多次
aa=range(100440000)
line_search(aa,50060300)
# print(line_search(aa,50060300))
#print(bin_search(aa,50060300))

#排序算法

#冒泡排序      时间复杂度o(n平方)
'''从最下面的数开始，前面的数要是比它小，那就向上进1（将前面的数和这个数位置互换）,如果比它大则不动，进入下一次冒泡循环
下面的函数就时不管传入的数据是否有序，都会把所有的数字循环一遍
'''
@timmer
def bubble_sort(li):
    for i in range(len(li)-1):
        for j in range(len(li)-i-1):
            if li[j]>li[j+1]:
                li[j],li[j+1] = li[j+1],li[j]
    print('冒泡排序完成')

'''
改进的冒泡排序，如果一次i循环中，嵌套的j循环没有一次进入过if条件，即整个循环数字位置都没有变动，证明数列已经是
从小到大正确的排序了，那么exchange=False，所以就跳出循环，不在对后面的i进行循环了。也就是不需要再排序了。
我们实际排序中，不一定次次都要执行到最后一个数才会排好，有时候排到一定次数，刚好就全部排好了，这时候这个函数就
会节省很多不必要的循环。
当传入的数据如果是排序好了的，这个函数就只会循环一次了。
'''
@timmer
def bubble_sort1(li):
    for i in range(len(li)-1):
        exchange=False
        for j in range(len(li)-i-1):
            if li[j]>li[j+1]:
                li[j],li[j+1] = li[j+1],li[j]
                exchange=True
        if not exchange:
            break
    print('sort1冒泡排序完成')


#data=list(range(8000))
#random.shuffle(data)
#print(data)
#bubble_sort(data)
#bubble_sort1(data)
#print(data)

#选择排序 时间复杂度o(n平方)
'''
先取第一个数，假设它是最小的，给它位置为1，然后向后面继续查找，如果后面的数比它小，那么就把位置1给后面的数，然后继续查找，以此类推，
所以选择排序要走n-1趟，
'''
@timmer
def select_sort(li):
    for i in range(len(li)-1):
        min_loc=i
        for j in range(i+1,len(li)):
            if li[min_loc]>li[j]:
                min_loc=j
        li[i],li[min_loc] = li[min_loc],li[i]
    print('选择排序完成')

# data=list(range(8000))
# random.shuffle(data)
# select_sort(data)
# print(data)

#插入排序
'''
原理跟打扑克是插入扑克牌一样，去除一个个数字，然后和已经排序好的进行对比，按顺序插入到有序的序列里面
'''
def insert_sort(li):
    for i in range(1,len(li)):
        tmp=li[i]
        j=i-1
        while j>=0 and tmp<li[j]:
            li[j+1]=li[j]
            j=j-1
        li[j+1]=tmp
# data=list(range(8000))
# random.shuffle(data)
# select_sort(data)
# print(data)

#快速排序  复杂度nlogn
'''
速度比前面三种快几个数量级
'''

'''
注意这是一个递归函数，所以不能直接用装饰器来装饰，否则递归的函数也会被装饰，递归多少次装饰器就会执行多少次。
如何解决呢：假设递归函数为A，那么可以在A函数上层再加一个函数B，然后这个函数B通过return来调用A()。然后对B函数加上
装饰器即可。
对于快排，
        最好情况    一般情况    最坏情况
快排    o(nlogn)    o(nlogn)    o(n平方)    当序列为倒序是，就是n^2。因为没法对里面的元素进行二分法，这是最坏的情况。如 8 7 6 5 4 3 2 1
冒泡    o(n)        o(n平方)    o(n平方)    当序列为已经排好的序列时，就只用对所有数列执行一次冒泡就好. 如 1 2 3 4 5
''' 
def quck_sort(data,left,right):
    if left<right:
        mid=partition(data,left,right)
        quck_sort(data,left,mid-1)
        quck_sort(data,mid+1,right)

def partition(data,left,right):
    tmp=data[left]      #这里要写Left不能写0，因为递归分为两部分，一部分从0开始，另一半从中间位置+1开始
    while left<right:     #当左边小于右边时，一直循环
        while left<right and data[right]>=tmp:      #当右边的数大于或者等于取到的数时
            right = right-1                         #将右边的游标right向左移动一位
        data[left]=data[right]
        while left<right and data[left]<=tmp:
            left += 1
        data[right]=data[left]
    data[left]=tmp
    return left

#由于quck_sort是递归函数，不能直接用装饰器来装饰，所以外面加了一层quck_sort_timer，然后对它进行装饰。
@timmer
def quck_sort_timer(data):
    return quck_sort(data,left=0,right=len(data)-1)     #如果这里的right写死，比如写10，那么排序就只会对前11个数字排序，后面的就不会再排序了。

'''系统的sort使用c写的，这个速度又比python快了1个数量级，最快的就是系统的这个sort'''
@timmer
def sys_sort(data):
    return data.sort()

data=list(range(1000))
random.shuffle(data)
data1=copy.deepcopy(data)
data2=copy.deepcopy(data)
data3=copy.deepcopy(data)
#print(data)
# data=[13, 10, 0, 14, 6, 3, 16, 12, 11, 1, 19]
#可以设置最大递归深度，比如这里1000次
#sys.setrecursionlimit(1000)
quck_sort_timer(data1)
bubble_sort1(data2)
sys_sort(data3)
# print(data1)
# print(data2)
# print(data3)


#堆排序
def shift(data,low,heigh):      # data整个数组列表 low数组第一个节点下标 heigh最后节点下标
    i=low                       #父节点下标
    j=2*low+1                   #左子节点下标
    tmp=data[i]                 #父节点的元素
    while j<=heigh:             #如果子节点下标小于等于最后节点下标
        if j<heigh and data[j]<data[j+1]:       #如果子节点下标小于最后节点下标，代表树的右边还有节点。那么就和右边节点比较，如果小于右边节点
            j=j+1                               #那就右边节点被选中，用于和父节点比较大小。 这样就完成了子节点大小的比较，大的被选举出来
        if tmp<data[j]:                         #如果父节点小于选举出来的最大的子节点
            data[i]=data[j]                     #那么将父节点位置的数字替换成子节点的数字，即子节点的数字上位。
            i=j                                 #循环走到子节点，将子节点变成父节点，即进入下一级继续循环
            j=2*i+1                             #孙子节点变成子节点
        else:
            break                               #如果父节点的数字大于子节点的数字，那么退出本次循环
    data[i]=tmp                                 #所有循环完毕后，将拿出的父节点的数字放回到i的位置。i的位置可能有两个，当父节点小于子节点，那么i就是子节点的位置，如果大于，i就还是原来的位置。

def head_sort(data):
    n=len(data)
    #建堆
    for i in range(n//2-1,-1,-1):       #最后一个有子节点的堆的下标是n//2-1,直到最后下标为0（堆的根节点的元素），每次i都减少1，证明堆在从底部一个个的循环，直到最顶层根结点代表堆的排序结束。
        shift(data,i,n-1)               #data代表整个需要排序的数组，i代表一个循环里面的父节点，n-1就是heigh，代表数组里面最后一个节点
    #挨个出数
    for i in range(n-1,-1,-1):
        data[0],data[i]=data[i],data[0]     # 将最上面下位的数字和最下面上位的数字位置互换
        shift(data,0,i-1)                   #互换位置后，最下面位置的下标从循环中踢出，即整个参与出数的个数-1.因为下位的数不再参与循环，所以参与出数的个数会越来越少
    print(data)
    '''也可以用下面的方法，只是要多申请个内存，然后生成的是倒序的'''
    # li=[]
    # for i in range(n-1,-1,-1):
    #     li.append(data[0])
    #     data[0]=data[i]
    #     shift(data,0,i-1)
    # print(li)
head_sort([3,8,2,1,9,7,6,5])
# data=list(range(1000))
# random.shuffle(data)
#head_sort(data)