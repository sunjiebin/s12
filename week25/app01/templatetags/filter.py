from django import template
from django.utils.safestring import mark_safe
register=template.Library()

@register.simple_tag
def filter_all(article_type,k):
    '''
            {% if kwargs.category_id == 0 %}
            <a class="choice" href="article-0-{{ kwargs.article_type_id }}.html">全部</a>
        {% else %}
            <a href="article-0-{{ kwargs.article_type_id }}.html">全部</a>
        {% endif %}
    :return:
    '''
    print(article_type,k)
    if k == 'category_id':
        n0=0
        n1=article_type['category_id']
        n2=article_type['article_type_id']
        print('n1 and n2',str(n1),n2)
    elif  k == 'article_type_id':
        n1 = article_type['article_type_id']
        n0=article_type['category_id']
        n2=0

    if n1 == 0:
        print('n1 and n2',str(n1),n2)
        ret = '<a class="choice" href="article-%s-%s.html">全部</a>' %(n0,n2)
    else:
        ret = '<a  href="article-%s-%s.html">全部</a>' %(n0,n2)



    print('all',ret)
    return mark_safe(ret)

@register.simple_tag
def filter_article_type(type,select_id,item_type):
    '''
            {% for i in category %}
            {# 注意：category数据库里面拿的id是数字，而kwargs的id是字符串，两者不相等。所以在kwargs里面我们将v转换成为了int类型 #}
            {% if i.id == kwargs.category_id %}
                <a class="choice" href="article-{{ i.id }}-{{ kwargs.article_type_id }}.html">{{ i.caption }}</a>
            {% else %}
                <a href="article-{{ i.id }}-{{ kwargs.article_type_id }}.html">{{ i.caption }}</a>
            {% endif %}
            {% endfor %}
    :param args: 
    :return:
    '''

    art_list=[]
    if item_type == 'category':
        for i in type:
            n1=i.id
            n2=select_id.get('category_id')
            n3=select_id.get('article_type_id')
            n4=i.caption
            if n1 == n2:
                ret = '<a class="choice" href="article-%s-%s.html">%s</a>' % (n1, n3, n4)
            else:
                ret = '<a href="article-%s-%s.html">%s</a>' % (n1, n3, n4)
            art_list.append(ret)
            # print(1,art_list)
    elif item_type == 'articletype':
        print('type',type)
        for i in type:
            n1 = i.id
            n2 = select_id.get('article_type_id')
            n3 = select_id.get('category_id')
            n4 = i.caption
            if n1 == n2:
                ret = '<a class="choice" href="article-%s-%s.html">%s</a>' % (n3, n1, n4)
            else:
                ret = '<a href="article-%s-%s.html">%s</a>' % (n3, n1, n4)
            art_list.append(ret)
        # print(2,art_list)



    art=mark_safe(" ".join(art_list))
    return art
