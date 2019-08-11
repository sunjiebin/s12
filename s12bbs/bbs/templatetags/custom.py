#!/usr/bin/env python3
# Auther: sunjb

from django import template
register=template.Library()

@register.simple_tag
def truncate_url(img_obj):
    # print(dir(img_url))     #查看这个对象拥有的方法
    # return '/'.join(img_obj.split('/')[1:])
    return img_obj.split('/', maxsplit=1)[-1]    #和上面的join取得的结果是一样的

@register.filter
def truncate_url2(url):
    return '/'.join(url.split('/')[1:])

@register.simple_tag
def filter_comment(article_obj):
    query_set=article_obj.comment_set.select_related()
    comments={
        'comment_count':query_set.filter(comment_type=1).count(),
        'thumb_count':query_set.filter(comment_type=2).count(),
    }
    return comments