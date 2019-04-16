import time
from numpy import *
import operator
from collections import Counter

# 去除前面的内容只保留句子
def delete(data, emotion, filename):
    with open(filename) as file:  # 读取训练集的句子
        count = 0
        for line in file:
            if count != 0:
                line = line.strip('\n')
                data.append(line.split(',')[0])
                emotion.append(line.split(',')[1])
            count += 1


# 生成不重复的词汇列
def tran(data):
    voca = []
    for sentence in data:
        tmp = sentence.split(' ')
        for tmp1 in tmp:
            voca.append(tmp1)
    voca2 = sorted(set(voca), key=voca.index)  # 利用set函数去除列表中重复元素
    return voca2

#da：训练集的one-hot矩阵，va：验证集one-hot矩阵
def classification(da,va,emotion,distancing,kk):
    newemotion=[]
    for i in range(va.shape[0]):
        tmp=tile(va[i],(da.shape[0],1))-da #将一行测试样本行复制扩展为矩阵，并将此矩阵与训练基矩阵做减运算
        tmp=tmp.getA() ** distancing #将矩阵转化为数组逐个乘方
        tmp=mat(tmp)
        sumi=tmp.sum(axis=1)#对做了减运算的矩阵进行每行都进行相加，得到一个每行和的矩阵
        sumi=sumi.getA() ** (1/distancing) #开方，即得到这条验证集语句与所有训练集语句的欧式距离
        distance={}
        for j in range(len(sumi)):
            distance[j]=sumi[j][0]
        sorted_x = sorted(distance.items(), key=operator.itemgetter(1))  # 这里按照value排序
        distance=sorted_x
        newemotio=[]
        for k in range(kk):
            newemotio.append(emotion[distance[k][0]])
        newemotion.append(Counter(newemotio).most_common(1)[0][0])#找众数
    return newemotion

#生成one-hot矩阵
def onehot(data, vari):
    res = []
    for datas in data:
        tmp = datas.split(' ')#将每个词语分割成词组
        tmp2=[]
        for varis in vari:
            if varis in tmp:#判断不重复词汇表里的词是否在样本中
                tmp2.append(1)
            else:
                tmp2.append(0)
        res.append(tmp2)
    res2=mat(res)
    return res2


if __name__ == "__main__":
    starttime = time.clock()
    data = []
    emotion = []
    delete(data, emotion, 'train_set.csv')
    vari = tran(data)
    num = len(vari)
    vadata = []
    vaemotion = []
    delete(vadata, vaemotion, 'validation_set.csv')  # 把训练集、测试集的语句和对应情感分别存储
    kmax=0
    acumax=0
    proper=0
    range1=len(data)//2
    for distancing in range(1,3):
        if distancing==1:
            print("The Manhattan Distance:\n")
        else:
            print("The Eulidean Distance:\n")
        for k in range(1,range1):
            onehotmatrix = onehot(data, vari)
            vaonehotmatix=onehot(vadata,vari)
            testemotion=classification(onehotmatrix,vaonehotmatix,emotion,distancing,k)
            flag=0
            for i in range(len(testemotion)):
                #print(testemotion[i])
                if testemotion[i]==vaemotion[i]:
                    flag+=1
            accuracy=flag/len(testemotion)
            print('k=',k,'  accuracy:',float(accuracy))
            if acumax<accuracy:
                acumax=accuracy
                kmax=k
                proper=distancing
    if proper==1:
        print("The proper distance:Manhattan Distance\nThe proper K:",kmax,"\nThe max accuracy:",acumax)
    else:
        print("The proper distance:Euclidean Distance\nThe proper K:", kmax, "\nThe max accuracy:", acumax)
    endtime = time.clock()
    print('time:', endtime - starttime)
