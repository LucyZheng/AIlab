import time
from numpy import *
import operator
from collections import Counter
import string


# 去除前面的内容只保留句子
def delete(data, filename):
    with open(filename, 'r', encoding='UTF-8') as file:  # 读取训练集的句子
        for line in file:
            line = line.strip('\n')
            data.append(line)


# 生成不重复的词汇列
def tran():
    with open('out2.txt', 'r', encoding='UTF-8') as file2:
        for line in file2:
            return line.strip(' ').split(' ')


# da：训练集的one-hot矩阵，va：验证集one-hot矩阵
def classification(da, va, emotion, distancing, kk,vaemotion):
    newemotion = []
    num=0
    for i in range(va.shape[0]):
        tmp = tile(va[i], (da.shape[0], 1)) - da  # 将一行测试样本行复制扩展为矩阵，并将此矩阵与训练基矩阵做减运算
        tmp = tmp.getA() ** distancing  # 将矩阵转化为数组逐个乘方
        tmp = mat(tmp)
        sumi = tmp.sum(axis=1)  # 对做了减运算的矩阵进行每行都进行相加，得到一个每行和的矩阵
        sumi = sumi.getA() ** (1 / distancing)  # 开方，即得到这条验证集语句与所有训练集语句的欧式距离
        distance = {}
        for j in range(len(sumi)):
            distance[j] = sumi[j][0]
        sorted_x = sorted(distance.items(), key=operator.itemgetter(1))  # 这里按照value排序
        distance = sorted_x
        newemotio = []
        for k in range(kk):
            newemotio.append(emotion[distance[k][0]])
        newemotion.append(Counter(newemotio).most_common(1)[0][0])  # 找众数
        num+=1
        print(newemotion[-1])
    return newemotion


# 生成one-hot矩阵
def onehot(data, vari):
    res = []
    num=0
    for datas in data:
        tmp = datas.strip(' ').split(' ')  # 将每个词语分割成词组
        tmp2 = []
        for varis in vari:
            if varis in tmp:  # 判断不重复词汇表里的词是否在样本中
                tmp2.append(1)
            else:
                tmp2.append(0)
        res.append(tmp2)
        print('训练',num,'onehot成功')
        num+=1

    res2 = mat(res)
    return res2


if __name__ == "__main__":
    starttime = time.clock()
    alldata = []
    allemotion = []
    delete(alldata, 'out.txt')
    delete(allemotion, 'trainLabel.txt')
    print('读取数据成功！')
    data = alldata[:6000]
    emotion = allemotion[:6000]
    vari = tran()
    print('读取不重复词汇成功！')
    num = len(vari)
    vadata = []
    vaemotion = []
    kmax = 0
    acumax = 0
    proper = 0
    range1 = 10
    onehotmatrix = onehot(data, vari)
    print("训练集onehot成功")
    vaonehotmatix = onehot(vadata, vari)
    print("验证集onehot成功")
    testemotion = classification(onehotmatrix, vaonehotmatix, emotion, 2, 10,vaemotion)
    endtime = time.clock()
    print('time:', endtime - starttime)
