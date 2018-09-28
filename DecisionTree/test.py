#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tools import *
from tree import *

dataset, label = createDataset()
dt = DecisionTree()
dt.fit(dataset, label)
sample1 = [[u"青绿", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑"]]
sample2 = [[u"青绿", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑"],
    [u"乌黑", u"蜷缩", u"沉闷", u"清晰", u"凹陷", u"硬滑"],
    [u"乌黑", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑"],
    [u"青绿", u"蜷缩", u"沉闷", u"清晰", u"凹陷", u"硬滑"],
    [u"浅白", u"蜷缩", u"浊响", u"清晰", u"凹陷", u"硬滑"],
    [u"青绿", u"稍蜷", u"浊响", u"清晰", u"稍凹", u"软粘"],
    [u"乌黑", u"稍蜷", u"浊响", u"稍糊", u"稍凹", u"软粘"],
    [u"乌黑", u"稍蜷", u"浊响", u"清晰", u"稍凹", u"硬滑"],
    [u"乌黑", u"稍蜷", u"沉闷", u"稍糊", u"稍凹", u"硬滑"],
    [u"青绿", u"硬挺", u"清脆", u"清晰", u"平坦", u"软粘"],
    [u"浅白", u"硬挺", u"清脆", u"模糊", u"平坦", u"硬滑"],
    [u"浅白", u"蜷缩", u"浊响", u"模糊", u"平坦", u"软粘"],
    [u"青绿", u"稍蜷", u"浊响", u"稍糊", u"凹陷", u"硬滑"],
    [u"浅白", u"稍蜷", u"沉闷", u"稍糊", u"凹陷", u"硬滑"],
    [u"乌黑", u"稍蜷", u"浊响", u"清晰", u"稍凹", u"软粘"],
    [u"浅白", u"蜷缩", u"浊响", u"模糊", u"平坦", u"硬滑"],
    [u"青绿", u"蜷缩", u"沉闷", u"稍糊", u"稍凹", u"硬滑"]]
dt.predict(sample2, label)
dt.save_model('test.model')
test = dt.load_model('test.model')
print("result: " +  str(test))
print(dt.tree)
