#!/usr/bin/python
# -*- coding: UTF-8 -*-

########################################################################
#
# Copyright (c) wangziyang. All Rights Reserved
#
########################################################################
"""
Filename      : tools.py
Author        : wangziyang
Email         : ziyangwang1992@163.com
Create time   : 2018-08-28 23:28
Last modified : 2018-08-28 23:28
Brief         : 
"""

import sys 


def get_max_label(X, y):
    pass


def get_best_feat_index(X, y):
    pass


def split_dataset(X, y, index, value)
    newX, newy
    return newX, newy


def create_tree(X, y):
    sample_num = len(X)
    feat_num = len(X[0])
    if feat_num == 0:
        return get_max_label(X, y)
    if y.count(y[0]) == len(y):
        return y[0]
    best_feat_index = get_best_feat_index(X, y)
    tree = {best_feat_index:{}}
    best_feat_values = set([sample[best_feat_index] for sample in X])
    for value in best_feat_values:
        tree[best_feat_index][value] = create_tree(split_dataset(X, y, best_feat_index, value)) 
    return tree
