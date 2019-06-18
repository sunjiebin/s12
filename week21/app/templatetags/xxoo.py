from django import template

#注意register名称是固定的，不能随便写
register = template.Library()

@register.simple_tag
def func(a1,a2,a3):
    print(a1+a2)
    return a1+a2+a3

@register.filter
def fil(n1,n2):
    return n2+n1