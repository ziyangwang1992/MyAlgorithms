from __future__ import division
import sys
import os
from math import sqrt
import math
import time
import tkMessageBox


def loadMovieLens(fileName):
    if fileName=='u1.test' or fileName=='u1.base':
        path = './movielens/'+fileName
    else:   
        path = './movielens/u1.base'
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
def sim_correntropy(prefer, user1, user2):
    sim = {}
    deta = 5
    # deta = (get_deta(prefer,user1) + get_deta(prefer,user2)) / 2
    for item in prefer[user1]:
        if item in prefer[user2]:
            sim[item] = 1
	n = len(sim)
    if n== 0:
        return -1
    sum1 = sum([prefer[user1][item]*prefer[user1][item] for item in sim])
    sum2 = sum([prefer[user2][item]*prefer[user2][item] for item in sim])
    sum3 = sum([prefer[user1][item]*prefer[user2][item] for item in sim])
    l2_distance = sqrt(sum1 + sum2 - 2*sum3)
    result = -(1/(2*deta*deta))*l2_distance
    result = pow(math.e, result)
    result = result / deta / n / sqrt(2*math.pi)
    return result


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
    sum1 = sum([prefer[user1][item] for item in sim])
    sum2 = sum([prefer[user2][item] for item in sim])

    # sum of squares
    sum1Sq = sum([pow(prefer[user1][item], 2) for item in sim])
    sum2Sq = sum([pow(prefer[user2][item], 2) for item in sim])

    sumMulti = sum([prefer[user1][item]*prefer[user2][item] for item in sim])
    num1 = sumMulti - (sum1*sum2/n)
    num2 = sqrt( (sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))  
    if num2==0:                                               
        return 0  

    result = num1/num2
    return result
    

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


def get_deta(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count + 1
    average = sum/count
    sum = 0
    for item in prefer[userId]:
        sum = sum + pow(prefer[userId][item] - average, 2)
    return sqrt(sum / count)	


def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count


def getRating(prefer1, userId, itemId, knumber,similarity):
    sim = 0.0
    averageOther =0.0
    jiaquanAverage = 0.0
    simSums = 0.0

    users = topKMatches(prefer1, userId, itemId, knumber, similarity)

    averageOfUser = getAverage(prefer1, userId)     

    for other in users:
        sim = similarity(prefer1, userId, other)   
        averageOther = getAverage(prefer1, other) 

        simSums += abs(sim)   
        jiaquanAverage +=  (prefer1[other][itemId]-averageOther)*sim   

    if simSums==0:
        return averageOfUser
    else:
        return (averageOfUser + jiaquanAverage/simSums)  


def getAllUserRating(fileTrain='u1.base', fileTest='u1.test', fileResult='result.txt', k=65, similarity=sim_correntropy):
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
    print("MAE:", abError/inAllnum)


if __name__ == "__main__":
    print("\n--------------cf_user_corr using MovieLens -----------\n")
    start = time.clock()
    getAllUserRating('u1.base', 'u1.test', 'result.txt')
    end = time.clock()
    print "running time: %f s" % (end - start)
    tkMessageBox.showinfo(title='Hello', message='Your cf_user_corr has been run successfully')
    
    
