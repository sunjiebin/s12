#!/usr/bin/env python3
# Auther: sunjb

def add_node(tree_dic,comment):
    if comment.parent_comment is None:
        tree_dic[comment]={}
    else:
        for k,v in tree_dic.items():
            if k == comment.parent_comment:
                tree_dic[comment.parent_comment][comment]={}
            else:
                add_node(v,comment)

def build_tree(comment_set):
    # print(comment_set)
    tree_dic={}
    for comment in comment_set:
        add_node(tree_dic,comment)
    return tree_dic

# def render_comment_node(tree_dic,margin_val):
#     html=""
#     for k,v in tree_dic.items():
#         ele="<div class='comment-node' style='margin-left:%spx'>"%margin_val + k.comment + '</div>'
#         html+=ele
#         html+=render_comment_node(v,margin_val+10)
#     return html
def render_comment_tree(tree_dic,margin_val=0):
    html=""
    for k,v in tree_dic.items():
        ele="<div class='root-comment'style='margin-left:%spx'>"%margin_val+"<span style='margin-left:10px'>%s</span>"%k.date + \
            "<span style='margin-left:10px'>%s</span>"%k.comment + \
            '<span comment-id=%s style="margin-left:10px;color:#033" class="glyphicon glyphicon-comment click-comment" aria-hidden="true"></span>' %k.id+ \
        "</div>"
        html+=ele
        html+=render_comment_tree(v,margin_val+10)
    return html


# def add_node2(tree_dic,comment):
#     if comment[1] is None:
#         tree_dic[comment[0]]={}
#     else:
#         for k,v in tree_dic.items():
#             if k == comment[1]:
#                 tree_dic[k][comment[0]]={}
#             else:
#                 add_node2(v,comment)
#
# def build_tree2(comment_set):
#     # print(comment_set)
#     tree_dic={}
#     for comment in comment_set:
#         add_node2(tree_dic,comment)
#     return tree_dic