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
from math import log

import pickle


def createDataset():
    dataset = [[u"青绿", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑", "yes"], 
    [u"乌黑", u"蜷缩", u"沉闷", u"清晰", u"凹陷", u"硬滑", "yes"],
    [u"乌黑", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑", "yes"],
    [u"青绿", u"蜷缩", u"沉闷", u"清晰", u"凹陷", u"硬滑", "yes"],
    [u"浅白", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑", "yes"],
    [u"青绿", u"稍蜷", u"浊响", u"清晰", u"稍凹", u"软粘", "yes"],
    [u"乌黑", u"稍蜷", u"浊响", u"稍糊", u"稍凹", u"软粘", "yes"],
    [u"乌黑", u"稍蜷", u"浊响", u"清晰", u"稍凹", u"硬滑", "yes"],
    [u"乌黑", u"稍蜷", u"沉闷", u"稍糊", u"稍凹", u"硬滑", "no"],
    [u"青绿", u"硬挺", u"清脆", u"清晰", u"平坦", u"软粘", "no"],
    [u"浅白", u"硬挺", u"清脆", u"模糊", u"平坦", u"硬滑", "no"],
    [u"浅白", u"蜷缩", u"浊响", u"模糊", u"平坦", u"软粘", "no"],
    [u"青绿", u"稍蜷", u"浊响", u"稍糊", u"凹陷", u"硬滑", "no"],
    [u"浅白", u"稍蜷", u"沉闷", u"稍糊", u"凹陷", u"硬滑", "no"],
    [u"乌黑", u"稍蜷", u"浊响", u"清晰", u"稍凹", u"软粘", "no"],
    [u"浅白", u"蜷缩", u"浊响", u"模糊", u"平坦", u"硬滑", "no"],
    [u"青绿", u"蜷缩", u"沉闷", u"稍糊", u"稍凹", u"硬滑", "no"]]
    
    #y = ["yes", "yes", "yes", "yes", "yes", "yes", "yes", "yes", "no", "no", "no", "no", "no", "no", "no", "no", "no"]
    
    labels = [u'色泽', u'根蒂', u'敲声', u'纹理', u'脐部', u'触感']

    return dataset, labels

    
def get_max_label(y):
    y_dict = {}
    max_num = -1
    max_val = y[0]
    for i in range(len(y)):
        y_dict[y[i]] = y_dict.get(y[i], 0) + 1
        if y_dict[y[i]] > max_num:
            max_num = y_dict[y[i]]
            max_val = y[i]
    return max_val


def get_entropy(y):
    y_dict = {}
    for val in y:
        y_dict[val] = y_dict.get(val, 0) + 1
    
    total = len(y)
    entropy = 0.0
 
    for label in y_dict:
        prob = float(y_dict[label]) / total
        entropy -= prob * log(prob, 2)
    return entropy 


def split_dataset(dataset, y, index, value):
    sub_dataset = []
    sub_y = []

    for i in range(len(dataset)):
        sample = dataset[i]
        if sample[index] == value:
            new_sample = sample[:index]
            new_sample.extend(sample[index+1:])
            sub_dataset.append(new_sample)
            sub_y.append(y[i])
    return sub_dataset, sub_y


def get_best_feat_index(dataset, y):
    base_entropy = get_entropy(y)
    max_info_gain = 0.0
    max_info_gain_index = -1
    for index in range(len(dataset[0]) - 1):
        info_gain = base_entropy
        feat_values = set([sample[index] for sample in dataset])
        for value in feat_values:
            sub_dataset, sub_y = split_dataset(dataset, y, index, value) 
            weight = float(len(sub_dataset)) / len(dataset)           
            info_gain -= weight * get_entropy(sub_y)

        print("index: %d, info_gain: %f" % (index, info_gain))

        if info_gain > max_info_gain:
            max_info_gain = info_gain
            max_info_gain_index = index
    return max_info_gain_index 


def create_tree(dataset, labels):
    sample_num = len(dataset)
    y = [sample[-1] for sample in dataset]
    feat_num = len(dataset[0]) - 1
    if feat_num == 0:
        return get_max_label(y)
    if y.count(y[0]) == len(y):
        return y[0]
    best_feat_index = get_best_feat_index(dataset, y)
    best_feat_label = labels[best_feat_index]
    tree = {best_feat_label:{}}
    del(labels[best_feat_index])
    best_feat_values = set([sample[best_feat_index] for sample in dataset])
    for value in best_feat_values:
        sub_labels = labels[:]
        sub_dataset, sub_y = split_dataset(dataset, y, best_feat_index, value)
        tree[best_feat_label][value] = create_tree(sub_dataset, sub_labels) 
    return tree


def predict_one(sample, labels, tree):
    if not isinstance(tree, dict):
        return tree
    label_dict = dict(zip(labels, sample))
    keys = tree.keys()
    if keys is None or len(keys) == 0:
        sys.stderr.write("[ERROR] predict failed: %s\n" % sample)
        return None
    label = list(keys)[0]

    if label not in label_dict:
        sys.stderr.write("[ERROR] predict failed: %s\n, label: %s not in labels.\n" % (sample, label))
        return None
    value = label_dict[label]
    sub_tree = {}
    try:
        sub_tree = tree[label][value]
    except:
        sys.stderr.write("[ERROR] predict: %s failed: %s is not a value of label: %s.\n" % (sample, value, label))
        return None
    return predict_one(sample, labels, sub_tree)


def predict(X, label, tree):
    for sample in X:
        if len(sample) != len(label):
            sys.stderr.write("[ERROR] sample: %s and label: %s have different columns.\n" % (sample, label))
            return False 
        pred = predict_one(sample, label, tree)
        if pred:
            print(pred)
        else:
            print("failed.")


def save_model(path, tree):
    with open(path, 'wb') as file:
        pickle.dump(tree, file)


def load_model(path):
    tree = None
    with open(path, 'rb') as file:
        tree = pickle.load(file)
    return tree
