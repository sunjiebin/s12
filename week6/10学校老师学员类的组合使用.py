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
        print('为老师%s办理入职手续'%staff_obj.name)
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

school=School('老男孩','北京')

t1=Teacher('oldboy',56,'M',200000,'linux')
t2=Teacher('alex',22,'M',300000,'python')

s1=Student('sun',28,'M',1001,'python')
s2=Student('mi',25,'F',1002,'linux')

t1.tell()
s1.tell()

school.hire(t1)
school.enroll(s1)
school.enroll(s2)

#print(school.students[0].grade)
print(school.students)
print(school.staffs)
school.staffs[0].teach()

for stu in school.students:
    stu.pay_tutition(8000)
