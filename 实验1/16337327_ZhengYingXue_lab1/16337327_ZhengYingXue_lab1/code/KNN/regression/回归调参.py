import time
from numpy import *
import operator
import pandas as pd
import numpy as np
# 去除前面的内容只保留句子
def delete(data, depro,filename):
    with open(filename) as file:  # 读取训练集的句子
        count = 0
        for line in file:
            tmp=[]
            if count != 0:
                line = line.strip('\n')
                tmp2=line.split(',')
                data.append(tmp2[0])
                for i in range(1,7):
                    tmp.append(float(tmp2[i]))
                depro.append(tmp)
            count += 1

def delete2(vadata,filename):
    with open(filename) as file:  # 读取验证集的句子
        count = 0
        for line in file:
            if count != 0:
                line = line.strip('\n')
                tmp2 = line.split(',')
                vadata.append(tmp2[0])
            count+=1


# 生成不重复的词汇列
def tran(data):
    voca = []
    for sentence in data:
        tmp = sentence.split(' ')
        for tmp1 in tmp:
            voca.append(tmp1)
    voca2 = sorted(set(voca), key=voca.index)  # 利用set函数去除列表中重复元素
    return voca2


def regression(da, va,depro,kk,distancing):
    vapro=[]
    depro=depro.tolist()
    for i in range(va.shape[0]):
        tmp = tile(va[i], (da.shape[0], 1)) - da
        tmp = tmp.getA() ** distancing
        tmp = mat(tmp)
        sumi = tmp.sum(axis=1)
        sumi = sumi.getA() ** (1/distancing)
        distance = {}
        for j in range(len(sumi)):
            distance[j] = sumi[j][0]
        sorted_x = sorted(distance.items(), key=operator.itemgetter(1))  # 这里按照value排序
        distance = sorted_x
        tmpline=[]
        for k2 in range(6):#对每个测试集的各个情感概率进行计算
            tmp2=0
            for k1 in range(kk):#取K=4
                if distance[k1][1]==0:#考虑到距离为0的情况，此处加上一个极小的数。
                    tmp2+=depro[distance[k1][0]][k2]/(distance[k1][1]+0.00000000000000000001)
                else:
                    tmp2+=depro[distance[k1][0]][k2]/distance[k1][1]
            tmpline.append(tmp2)
        tmpsum=sum(tmpline)
        tmpline /= tmpsum #在各行概率计算完毕后，进行归一化处理，以让各个情感概率为1
        vapro.append(tmpline.tolist())
    return vapro#返回情感概率矩阵，以便进行相关度测试


def onehot(data, vari):
    res = []
    for datas in data:
        tmp = datas.split(' ')
        tmp2 = []
        for varis in vari:
            if varis in tmp:
                tmp2.append(1)
            else:
                tmp2.append(0)
        res.append(tmp2)
    res2 = mat(res)
    return res2


if __name__ == "__main__":
    starttime = time.clock()
    data = []
    depro=[]
    delete(data, depro, 'train_set.csv')
    depro=mat(depro)#depro为训练集的概率矩阵
    vari = tran(data)
    num = len(vari)
    vadata = []
    vapro=[]
    vapro1=[]
    delete(vadata,vapro1,'validation_set.csv')  # 把训练集、测试集的语句和对应情感分别存储
    vapro1 = mat(vapro1)
    vapro1 = vapro1.T
    vapro1 = vapro1.getA()
    onehotmatrix = onehot(data, vari)
    vaonehotmatix = onehot(vadata, vari)
    kmax=0
    summax=0
    proper=0
    range1= int(len(data) ** 0.5)
    for k in range(1,200):
            vapro=regression(onehotmatrix, vaonehotmatix,depro,k,2)
            vapro=mat(vapro)
            vapro=vapro.T
            vapro=vapro.getA()

            sum1=0
            for i in range(6):
                sum1 += np.corrcoef(vapro[i],vapro1[i])[0][1]
            sum1 /=6
            print("K=",k,"  Correlation:",sum1)
            if sum1>summax:
                summax=sum1
                kmax=k


    print("The proper distance:Euclidean Distance\nThe proper K:", kmax, "\nThe max correlation:", summax)

