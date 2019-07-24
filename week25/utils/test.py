from bs4 import BeautifulSoup

'''需要beautifulsoup4的支持'''
# pip3 install beautifulsoup4

content='''
<div class="condition" id='i2'>
    <h1>过滤条件</h1>
    <div>
        <p>aa</p>
        <a href='/index'>测试</a>
        {% filter_all kwargs 'category_id' %}
        {% filter_article_type category kwargs 'category' %}
    </div>
</div>
<span style="font-size: 8px">testspan</span>
<script>alter('123')</script>
'''

# 黑名单方式删除匹配的标签及属性
#从html格式解析content里面的内容
soup=BeautifulSoup(content,'html.parser')
# 查找content里面的script标签
tag=soup.find('script')
# 打印查找到的标签
print('打印匹配到的script标签',tag)
# 清空tag对象，也就是清空查找到的script标签里面的内容，但是script标签本身还是留下
tag.clear()
print('decode前',content)
# 将转码成字符串,执行后<script><script>里面的alter('123')被清除了。
content=soup.decode(content)
print('decode后，清空了script里面的内容',content)
#隐藏匹配到的<script>标签
tag.hidden=True
content=soup.decode(content)
print('隐藏了script标签',content)

span=soup.find('span')
# 找到span标签属性并以字典显示
print('找到span标签的属性',span.attrs)
del span.attrs['style']
print('删除掉span的sytle属性',span)

print(content)

# 标签白名单
white_tags=['p','strong','div']
ss=BeautifulSoup(content,'html.parser')
# find_all()找到所有的标签
for tag in ss.find_all():
    # 打印匹配的标签名称
    # print(tag.name)
    if tag.name in white_tags:
        pass
    else:
        # hidden隐藏了匹配到的标签，但并不会将标签里面的内容隐藏，如 <h>hello</h> ---> hello
        tag.hidden=True
        # 所以一般配合clear一起用，隐藏标签的同时，把里面的内容也一并清空
        '''注意：在清除时要注意标签的包含关系，会把标签下的子标签一并清除。如<h1><p>aa</p></h1> --> 全部清空，<p>aa</p>虽然在白名单，但不会留下 '''
        tag.clear()


content=ss.decode()
print('白名单之外的全清除')
print(content)

# 属性白名单
tags={
    'div':['class'],
    'strong':['id'],
}
aa=BeautifulSoup(content,'html.parser')
for tag in aa.find_all():
    if tag.name in tags:
        pass
    else:
        tag.hidden=True
        tag.clear()
        continue
    # 获取tag里面的标签属性
    input_attrs=tag.attrs  # {'class': ['condition'], 'id': 'i2'}
    print(input_attrs)
    #获取到tags里面的value,也就是标签的属性
    valid_attrs=tags[tag.name]  #   ['class']

    for k in list(input_attrs.keys()):
        if k in valid_attrs:
            pass
        else:
            del tag.attrs[k]
print('删除属性前')
print(content)
content = aa.decode()
print('白名单之外的属性全清除后')
print(content)



