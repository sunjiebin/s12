#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

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
    def __init__(self,name,age,sex,salary,course):
        #SchoolMember.__init__(name,age,sex)
        super(Teacher,self).__init__(name,age,sex)
        self.salary=salary
        self.course=course
    def tell(self):
        print('''
        ----info of teacher----
        name:%s age:%s sex:%s salary:%s course:%s
        '''%(self.name,self.age,self.sex,self.salary,self.course))
    def teach(self):
        print('%s is teaching course [%s]'%(self.name,self.course))

class Student(SchoolMember):
    def __init__(self,name,age,sex,stu_id,grade):
        super(Student,self).__init__(name,age,sex)
        self.stu_id=stu_id
        self.grade=grade
    def tell(self):
        print('''
         ----info of student----
         name:%s age:%s sex:%s stuid:%s grade:%s
         ''' % (self.name, self.age, self.sex, self.stu_id, self.grade))
    def pay_tutition(self,amount):
        print('%s has paid tutition for $[%s]'%(self.name,amount))

'''实例化School,将self.name,self.addr赋值'''
school=School('老男孩','北京')

'''实例化Teacher，添加两个老师'''
t1=Teacher('oldboy',56,'M',200000,'linux')
t2=Teacher('alex',22,'M',300000,'python')
'''实例化Student，添加两个学生'''
s1=Student('sun',28,'M',1001,'python')
s2=Student('mi',25,'F',1002,'linux')
'''调用实例化后的方法'''
t1.tell()
t1.teach()
s1.tell()
print('打印school.name',school.name)

'''在实例化后School中，引入t1
过程解析：
school.hire(t1)   通过school，将t1的内存地址放在hire函数的参数里面。
执行了以下方法，
这个方法里面的self便是school，所以self.name也就是school.name
staff_obj就是传进来的t1，所以staff_obj.name其实就是t1.name
   def hire(self,staff_obj):   
        print('%s机构为老师%s办理入职手续'%(self.name,staff_obj.name))
下面这行的self.staffs是School类里面定义的构造函数，相当于school.staffs.append
        self.staffs.append(staff_obj)
'''
school.hire(t1)
school.enroll(s1)
school.enroll(s2)

#print(school.students[0].grade)
'''打印school.students,这是一个列表，列表里面的元素是s1,s2的内存地址。
school.students[0]是s1的内存地址，school.students[2]是s2的内存地址。
'''
print(school.students)
print(school.staffs)

'''school.staffs[0]即我们前面添加的t1的内存地址，所以
school.staffs[0].teach() == t1.teach()
'''
school.staffs[0].teach()
#和上面的效果等效
t1.teach()

for stu in school.students:
    stu.pay_tutition(8000)
'''等效于'''
for stu in [s1,s2]:
    stu.pay_tutition(8000)
