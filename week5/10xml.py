#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''导入xml处理模块'''
import xml.etree.ElementTree as ET
'''读取config.xml文件，遍历整个文件'''
tree = ET.parse('config.xml')
root = tree.getroot()
'''获取根下的标签'''
print(root.tag)

for child in root:
    #获取一级标签里面的参数
    print(child.attrib)
    for i in child:
        #tag获取标签名，text获取标签里面的值
        print(i.tag,i.text)

#只遍历year节点
for node in root.iter('year'):
    print(node.text)

#修改
'''修改,将year标签里面的年份值+100，
并写入到新的文件中'''
for node in root.iter('year'):
    year=int(node.text)+100
    #将node.text重新赋值，即改变了原来的值
    node.text=str(year)
    #给node节点增加了属性，会在year标签属性里面多了updated=yes
    node.set('upated','yes')
#定入到指定的文件
tree.write('config-new.xml')

#删除
'''查找country标签，并标签下rank标签值大于50的country删除'''
#循环所有的country
for node in root.findall('country'):
    #找到country下面的rank标签里面的值
    print(node.find('rank').text)
    rank=int(node.find('rank').text)
    if rank>50:
        root.remove(node)
tree.write('config-del.xml')

#自建一个xml
import xml.etree.ElementTree as ET

#创建根节点namelist
new_xml = ET.Element("namelist")
#创建子节点，名称为name,属性为attrib定义
name = ET.SubElement(new_xml, "name", attrib={"enrolled": "yes"})
age = ET.SubElement(name, "age", attrib={"checked": "no"})
sex = ET.SubElement(name, "sex")
#name标签里面的值为33
sex.text = '33'
name2 = ET.SubElement(new_xml, "name", attrib={"enrolled": "no"})
age = ET.SubElement(name2, "age")
age.text = '19'

et = ET.ElementTree(new_xml)  # 生成文档对象
et.write("test.xml", encoding="utf-8", xml_declaration=True)

ET.dump(new_xml)  # 打印生成的格式