#!/usr/bin/python
# -*- coding: UTF-8 -*-

########################################################################
#
# Copyright (c) wangziyang. All Rights Reserved
#
########################################################################
"""
Filename      : tree.py
Author        : wangziyang
Email         : ziyangwang1992@163.com
Create time   : 2018-08-28 21:04
Last modified : 2018-08-28 21:04
Brief         : 决策树ID3
"""

import sys

from tools import create_tree


class DecisionTree(object):
    """
    决策树ID3

    Attributes:
        
    """ 

    def __init__(self):
        self.tree = None

    def fit(self, X, y):
        if len(X) != len(y):
            sys.stderr.write("[FATAL] Your sample and label have different nums.\n")
            return False
        if len(X) == 0 or len(y) == 0:
            sys.stderr.write("[FATAL] your sample or label is null.\n")
            return False
        self.tree = create_tree(X, y)
        return True

    def predict(self, X):
        pass
