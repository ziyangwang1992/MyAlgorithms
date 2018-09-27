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
from tools import predict
from tools import save_model
from tools import load_model


class DecisionTree(object):
    """
    决策树ID3

    Attributes:
        
    """ 

    def __init__(self):
        self.tree = None
        self.labels = None

    def fit(self, dataset, labels):
        if len(dataset) == 0 or len(labels) == 0:
            sys.stderr.write("[FATAL] your sample or label is null.\n")
            return False 
        if len(dataset[0]) != len(labels) - 1:
            sys.stderr.write("[FATAL] your sample and label have different columns.\n")
            return False
        if len(dataset[0]) < 3:
            sys.stderr.write("[FATAL] please make sure your feature nums are more than 1.\n")
        self.labels = labels
        self.tree = create_tree(dataset, labels[:])
        return True

    def predict(self, X, labels):
        if self.tree is None:
            sys.stderr.write("[FATAL] your tree has not been created or loaded.\n")
            return False
        if X is None:
            sys.stderr.write("[FATAL] your input dataset is none, please recheck.\n")
            return False
        if len(X[0] != len(labels)):
            sys.stderr.write("[FATAL] your sample and label have different columns.")
            return False
        result = predict(X, labels, self.tree)

    def save_model(self, path):
        pass

    def load_mode(self, path):
        pass
