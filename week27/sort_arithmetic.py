#!/usr/bin/env python3
# Auther: sunjb
import  sys,random,copy

#归并排序
# 将列表分成两边，两个都是有序的集合，然后把这两边归并在一起。
def merge(li,low,mid,heigh):
    '''
     data=[1,4,5,6,2,3,7,8,9]
     merge(data,0,3,8)
     '''
    i=low
    j=mid+1
    ltmp=[]
    while i<=mid and j<=heigh:
        if li[i] < li[j]:
            ltmp.append(li[i])
            i += 1
        else:
            ltmp.append(li[j])
            j += 1
    while i<=mid:
        ltmp.append(li[i])
        i += 1
    while j<=heigh:
        ltmp.append(li[j])
        j += 1
    li[low:heigh+1]=ltmp
    # print(li)


def mergsort(li,low,high):
    '''
    先分解再合并
    :param li:
    :param low:
    :param high:
    :return:
    '''
    if low<high:
        mid=(low+high)//2
        mergsort(li,low,mid)    #分解左边的
        mergsort(li,mid+1,high) #分解右边的
        merge(li,low,mid,high)  #合并分解的
    return li
data=list(range(5000))
random.shuffle(data)
data1=copy.deepcopy(data)
# data=[5,9,3,1,4,8,6,7,2]
# data=[1,4,5,6,2,3,7,8,9]
# merge(data,0,3,8)
print(mergsort(data,0,len(data)-1))

#运行速度： 快排>归并>堆排

# python自带了堆排序的函数heapq，利用这个函数就可以直接进行堆排序
import heapq

heap=[]
for num in data1:
    heapq.heappush(heap,num)        #将数组变成一个堆，得到的数组将是一个小根堆（顶层是0）
print(heap)
heap_sort=[]
for i in range(len(heap)):
    num=heapq.heappop(heap)         #对堆进行排序，会按照序列从小到大依次输出
    heap_sort.append(num)
print(heap_sort)                    #得到一个排列好的有序数组

print(data1)
print(heapq.nsmallest(10,data1))    #得到无序数组里面前十个最小的元素
print(heapq.nlargest(10,data1))     #得到最大的十个元素

#找出列表里面相同连续元素的下标
#二分查找法
def bin_search(data_set,val):
    low=0
    high=len(data_set)-1
    while low<=high:
        mid=(low+high)//2
        if data_set[mid]==val:
            left=mid
            right=mid
            while left>=0 and data_set[left]==val:
                left -=1
            while right<len(data_set) and data_set[right] == val:
                right +=1
            return (left+1,right-1)
        elif data_set[mid]<val:
            low = mid+1
        else:
            high=mid-1
li=[1,2,2,3,3,3,4,4,5]
print(bin_search(li,3))