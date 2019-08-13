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