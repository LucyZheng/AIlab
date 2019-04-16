import time
from numpy import *
import math
def delete(data, filename):
    with open(filename, 'r', encoding='UTF-8') as file:  # 读取训练集的句子
        for line in file:
            line = line.strip('\n')
            data.append(line)

def tran(data):
    voca = []
    for sentence in data:
        tmp = sentence.split(' ')
        for tmp1 in tmp:
            voca.append(tmp1)
    voca2 = set(voca) # 利用set函数去除列表中重复元素
    voca3=[]
    i=0
    for vocas in voca2:
        print("判断 ",i)
        i+=1
        if voca.count(vocas) > 1:#去除出现频率过小的词
            voca3.append(vocas)
    return voca3



def calprobablity(data, vari, class1, emotion):#计算先验概率和条件概率
    index = 0
    for i in range(5):
        for varis in vari:
            class1[str(i)][varis] = 0
    for datas in data:
        tmp = datas.strip(' ').split(' ')  # 将每个词语分割成词组
        for varis in vari:
            if varis in tmp:
                class1[emotion[index]][varis] += 1#计算各属性取值0或1（在或不在该条数据中）
        print(index, " 成功")
        index += 1


def classification(vadata, testemotion, class1, class2, sumdic, length, vari):#根据朴素贝叶斯公式计算并预测分类
    pclass2 = {}
    for i in range(5):
        pclass2[str(i)] = math.log((class2[str(i)] + 18) / (length + 5)) # 拉普拉斯平滑求P(Y=i)
    sum1 = 0
    for vadatas in vadata:
        tmppro = []
        tmp2 = vadatas.strip(' ').split(' ')
        for i in range(5):
            probab = pclass2[str(i)]
            for voca in tmp2:
                if voca in vari:
                    probab += math.log((class1[str(i)][voca] + 18) / (sumdic[str(i)] + 2))#乘法转化为取对数后的加法
            tmppro.append(probab)
        testemotion.append(tmppro.index(max(tmppro)))
        print(sum1, '预测成功')
        sum1 += 1



if __name__ == "__main__":
    starttime = time.clock()
    alldata = []
    allemotion = []
    delete(alldata, 'out.txt')
    delete(allemotion, 'trainLabel.txt')
    print('读取数据成功！')
    data = alldata[:18000]#取前18000条为训练集，后6000条为验证集
    length=len(data)
    emotion = allemotion[:18000]
    vari = tran(data)
    print('生成不重复词汇成功！')
    vadata = alldata[18000:]
    vaemotion = allemotion[18000:]
    class1={}#第一个字典：在每个分类下每个属性的数量
    class2={}#第二个字典：每个分类出现的次数
    for i in range(5):
        class1[str(i)]={}
        class2[str(i)]=0
    for emotions in emotion:
        class2[emotions]+=1
    sumdic={}
    calprobablity(data, vari,class1,emotion)#计算先验概率和条件概率
    testemotion=[]#判断出来的情感
    for k in range(5):
        sum=0
        for value in class1[str(k)].values():
           sum+=value
        sumdic[str(k)]=sum#每一类的词语总个数
    classification(vadata,testemotion,class1,class2,sumdic,length,vari)
    flag=0
    for i in range(len(testemotion)):
        if str(testemotion[i])==str(vaemotion[i]):
            flag+=1
    print(flag/len(vaemotion))
