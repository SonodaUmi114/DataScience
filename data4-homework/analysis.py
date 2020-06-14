'''
Group1 members information:
Name, ID, E-mail
Cao Yanfei    320180939561  caoyf18@lzu.edu.cn
Cao Yuxuan    320180939571  caoyx2018@lzu.edu.cn
Ding Junwei   320180939671  dingjw18@lzu.edu.cn
Gao Shan      320180939740  shgao18@lzu.edu.cn
Liu Zheng     320180940101  liuzheng2018@lzu.edu.cn
Qiu Hanqiang  320180940181  479845114@qq.com
Song Xiujie   320180940211  songxj2018@lzu.edu.cn
Zhang Zexin   320180940590  zhangzexin18@lzu.edu.cn
'''

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 1.0
__author__ = ['Hanqiang Qiu','Yanfei Cao','Zheng Liu','Xiujie Song','Yuxuan Cao','Shan Gao','Zexin Zhang','Junwei Ding']
__email__ = ['479845114@qq.com','caoyf18@lzu.edu.cn','liuzheng2018@lzu.edu.cn','songxj@lzu.edu.cn','caoyx2018@lzu.edu.cn','shgao18@lzu.edu.cn','zhangzexin18@lzu.edu.cn','dingjw18@lzu.edu.cn']
__status__ = 'done'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import random

def clean(filename):
    dataframe = pd.read_csv(str(filename), skip_blank_lines = True)
    #print(dataframe.time)
    array1 = []
    for i in dataframe.time :
        array1.append(i)
    array2 = random.sample(array1, 2000)
    array2.sort()
    array3 = np.asarray(array2)
    #print(array2)
    #print(len(array2))
    return array3


def makeimg(filename):
    dataframe = pd.read_csv(str(filename), skip_blank_lines = True)
    #print(dataframe.time)
    array1 = []
    for i in dataframe.time :
        array1.append(i)
    plt.hist(array1, bins=50, density=1, facecolor='blue', alpha=0.75)
    plt.title(filename)
    plt.xlabel('time to fix')
    plt.ylabel('share')
    plt.show()



def KL(arr1, arr2):
    return scipy.stats.entropy(arr1, arr2)

def JS(p,q):
    M=(p+q)/2
    return 0.5*scipy.stats.entropy(p, M)+0.5*scipy.stats.entropy(q, M)


#计算曼哈顿距离：
def manhattan(p,q):
#只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same += 1
    n = same
    vals = range(n)
    distance = sum(abs(p[i] - q[i]) for i in vals)
    return distance

#计算皮尔逊相关度：
def pearson(p,q):
#只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same +=1

    n = same
    sumx = sum([p[i] for i in range(n)])
    sumy = sum([q[i] for i in range(n)])
    sumxsq = sum([p[i]**2 for i in range(n)])
    sumysq = sum([q[i]**2 for i in range(n)])
    sumxy = sum([p[i]*q[i] for i in range(n)])
    # print sumxy
    #求出pearson相关系数
    up = sumxy - sumx*sumy/n
    down = ((sumxsq - pow(sumxsq,2)/n)*(sumysq - pow(sumysq,2)/n))**.5
    #若down为零则不能计算，return 0
    if down == 0 :return 0
    r = up/down
    return r




def caclu(funcname):
    arr1 = clean('v4_4.csv')
    arr2 = clean('v4_9.csv')
    arr3 = clean('v4_14.csv')
    arr4 = clean('v4_19.csv')
    print(str(funcname))
    print(funcname(arr1, arr2))
    print(funcname(arr1, arr3))
    print(funcname(arr1, arr4))
    print(funcname(arr2, arr3))
    print(funcname(arr2, arr4))
    print(funcname(arr3, arr4))




makeimg('v4_4.csv')
makeimg('v4_9.csv')
makeimg('v4_14.csv')
makeimg('v4_19.csv')

caclu(pearson)
caclu(KL)
caclu(JS)
caclu(manhattan)






