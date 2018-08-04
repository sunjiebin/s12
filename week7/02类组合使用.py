#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''我们可以直接在构造函数里面将一个实例化的对象传进去,
这样就相当于实现了类的继承,这对于多个参数不同的函数继承
是很有用的'''
class School(object):
    def __init__(self,name,addr):
        self.name=name
        self.addr=addr
        self.students=[]
        self.teacher=[]
        self.staffs=[]
    def enroll(self,stu_obj):
        print('为学员%s办理入学手续'%stu_obj.name)
        self.students.append(stu_obj)
    def hire(self,staff_obj):
        print('%s机构为老师%s办理入职手续'%(self.name,staff_obj.name))
        self.staffs.append(staff_obj)
class SchoolMember(object):
    def __init__(self,name,age,sex):
        self.name=name
        self.age=age
        self.sex=sex
    def tell(self):
        pass
class Teacher(SchoolMember):
    '''这里我们将school_obj传进来'''
    def __init__(self,name,age,sex,salary,course,school_obj):
        #SchoolMember.__init__(name,age,sex)
        '''比如在Teacher类里面,我们既想把SchoolMember继承,又想继承
        School,而SchoolMember和School两者的参数有不一样,那么这时候
        用super就没法完成两个类的继承了,这时候就可以用将实例化的类
        传进来的方式解决'''
        super(Teacher,self).__init__(name,age,sex)
        ''''定义类变量school'''
        self.school=school_obj
        self.salary=salary
        self.course=course
    def tell(self):
        print('''
        ----info of teacher----
        name:%s age:%s sex:%s salary:%s course:%s
        '''%(self.name,self.age,self.sex,self.salary,self.course))
s1=School('hafool','beijing')
'''在实例化Teacher时,将s1传递进去,s1是一个已经实例化的School'''
t1=Teacher('sun',18,'F',2000,'linux',s1)
t1.tell()
s1.hire(t1)
'''这时候,就可以通过t1来调用School类里面的函数了,相当于实现了类的继承'''
t1.school.enroll(t1)
#s1.enroll(t1)