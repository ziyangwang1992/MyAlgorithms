from __future__ import division
import sys
import os
import math
import time
from math import sqrt
import tkMessageBox


def loadMovieLens(fileName):
    path = './movielens/' + fileName
    prefer = {}
    for line in open(path, 'r'):
        (userid, movieid, rating, ts) = line.split('\t')
        prefer.setdefault(userid, {})
        prefer[userid][movieid] = float(rating)
    return prefer


def testData():
    trainDict = loadMovieLens('u1.base')
    testDict = loadMovieLens('u1.test')
    print(len(trainDict))
    print(len(testDict))
    print("load success")


### comupute correntropy
def sim_correntropy(prefer, item, other):
    sim = {}
    deta = 5
    # deta = (get_deta(prefer,user1) + get_deta(prefer,user2)) / 2
    for user in prefer:
        if other in prefer[user] and item in prefer[user]:
            sim[user] = 1
    n = len(sim)
    if n== 0:
        return -1
    sum1 = sum([prefer[user][item]*prefer[user][item] for user in sim])
    sum2 = sum([prefer[user][other]*prefer[user][other] for user in sim])
    sum3 = sum([prefer[user][item]*prefer[user][other] for user in sim])
    l2_distance = sqrt(sum1 + sum2 - 2*sum3)
    result = -(1/(2*deta*deta))*l2_distance
    result = pow(math.e, result)
    result = result / deta / n / sqrt(2*math.pi)
    return result


### compute cosin similarity
def sim_pearson_item(prefer, item1, item2):
    sim = {}
    for user in prefer:
        if item1 in prefer[user] and item2 in prefer[user]:
            sim[user] = 1
    n = len(sim)
    if n == 0:
        return -1
    ave1 = getItemAverage(prefer, item1)
    ave2 = getItemAverage(prefer, item2)
    num1 = sum([(prefer[user][item1]-ave1)*(prefer[user][item2]-ave2) for user in sim])
    sum1 = sum([pow(prefer[user][item1]-ave1,2) for user in sim])
    sum2 = sum([pow(prefer[user][item2]-ave2,2) for user in sim])
    num2 = sqrt(sum1) * sqrt(sum2)
    if num2 == 0:
        return 0
    return num1/num2    


### compute pearson similarity for item_based cf
def sim_cosine(prefer, item1, item2):
    sim = {}
    for user in prefer:
        if item1 in prefer[user] and item2 in prefer[user]:
            sim[user] = 1
    # number of element
    n = len(sim)
    if n==0:
        return -1
    num1 = sum([(prefer[user][item1] - getAverage(prefer, user)) for user in sim])
    sum1 = sum([pow((prefer[user][item1] - getAverage(prefer, user)),2) for user in sim])
    sum2 = sum([pow((prefer[user][item2] - getAverage(prefer, user)),2) for user in sim])
    num2 = sqrt(sum1) * sqrt(sum2)
    if num2 == 0:
        return 0
    return num1/num2    
    

### compute pearson similarity
def sim_pearson(prefer, user1, user2):
    sim = {}
    for item in prefer[user1]:
        if item in prefer[user2]:
            sim[item] = 1
    # number of element
    n = len(sim)
    if n==0:
        return -1
    
    # sum
    # sum1 = sum([prefer[user1][item] for item in sim])
    # sum2 = sum([prefer[user2][item] for item in sim])
    # sum of squares
    # sum1Sq = sum([pow(prefer[user1][item], 2) for item in sim])
    # sum2Sq = sum([pow(prefer[user2][item], 2) for item in sim])
    # sumMulti = sum([prefer[user1][item]*prefer[user2][item] for item in sim])
    # num1 = sumMulti - (sum1*sum2/n)
    # num2 = sqrt( (sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))  

    ave1 = getAverage(prefer, user1)
    ave2 = getAverage(prefer, user2)
    num1 = sum([(prefer[user1][item]-ave1)*(prefer[user2][item]-ave2) for item in sim])
    sum1Sq = sum([pow(prefer[user1][item]-ave1, 2) for item in sim])
    sum2Sq = sum([pow(prefer[user2][item]-ave2, 2) for item in sim])
    num2 = sqrt(sum1Sq * sum2Sq)
    
    
    if num2==0:                                               
        return 0  

    result = num1/num2
    return result
    

def topKItems(prefer, user, itemId, k, sim):
    itemSet = []
    scores = []
    items = []
    for item in prefer[user]:
        itemSet.append(item)
    scores = [(sim_correntropy(prefer, itemId, other), other) for other in itemSet if other != itemId]
    scores.sort()
    scores.reverse()
    if len(scores) <= k:
        for item in scores:
            items.append(item[1])
        return items
    else:
        kscore = scores[0:k]
        for item in kscore:
            items.append(item[1])
        return items


def topKMatches(prefer, person, itemId, k, sim):
    userSet = []
    scores = []
    users = []
    
    for user in prefer:
        if itemId in prefer[user]:
            userSet.append(user)

    scores = [(sim(prefer, person, other),other) for other in userSet if other!=person]

    scores.sort()
    scores.reverse()

    if len(scores)<=k:       
        for item in scores:
            users.append(item[1])  
        return users
    else:                   
        kscore = scores[0:k]
        for item in kscore:
            users.append(item[1]) 
        return users               


def getItemAverage(prefer, itemId):
    count = 1;
    sum = 0;
    for user in prefer:
        if itemId in prefer[user]:
            sum = sum + prefer[user][itemId]
            count = count + 1
    return sum/count


def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count


def getRating(prefer1, userId, itemId, knumber,similarity):
    sim = 0.0
    averageOther = 0.0
    jiaquanAverage = 0.0
    simSums = 0.0

    items = topKItems(prefer1, userId, itemId, knumber, similarity)

    averageOfItem = getItemAverage(prefer1, itemId)     

    for other in items:
        sim = similarity(prefer1, itemId, other)   
        averageOther = getItemAverage(prefer1, other) 

        simSums += abs(sim)   
        jiaquanAverage += (prefer1[userId][other]-averageOther)*sim   

    if simSums==0:
        return averageOfItem
    else:
        return (averageOfItem + jiaquanAverage/simSums)  


def getAllUserRating(fileTrain, fileTest, fileResult, k=15, similarity=sim_correntropy):
    prefer1 = loadMovieLens(fileTrain)         
    prefer2 = loadMovieLens(fileTest)            
    inAllnum = 0
    rightNum = 0
    abError = 0

    #file = open(fileResult, 'a')
    #file.write("%s\n"%("------------------------------------------------------"))
    
    for userid in prefer2:            
        for item in prefer2[userid]: 
            rating = getRating(prefer1, userid, item, k, similarity)
            realRating = prefer2[userid][item]
            if int(round(rating))==realRating:
                rightNum += 1
            #file.write('%s\t%s\t%s\n'%(userid, item, rating))
            inAllnum = inAllnum +1
            abError += abs(rating - realRating)
    #file.close()
    print("-------------Completed!!-----------",rightNum/inAllnum)
    print("MAE:",abError/inAllnum)


if __name__ == "__main__":
    print("\n--------------cf_item_corr MovieLens -----------\n")
    num = 0
    while num <= 0:
        if num == 0:
            file = 'u1.base'
        else:
            file = 'u1_chaos'+str(num)+'.base'
        start = time.clock()
        getAllUserRating(file, 'u1.test', 'result.txt')
        end = time.clock()
        print file + " success run, running time: %f s" % (end - start)
        num+=1
    tkMessageBox.showinfo(title='Hello', message='Your cf_item has been run successfully')

###prefer{'John': {'M': 5, 'T': 1, 'W': 2, 'F': 2}, 'Diane': {'F': 3, 'M': 4, 'T': 3, 'D': 5}, 'Lucy': {'F': 5, 'M': 1, 'T': 5, 'W': 5, 'D': 2}, 'Eric': {'M': 2, 'D': 3, 'W': 4, 'F': 5}}
    
    
