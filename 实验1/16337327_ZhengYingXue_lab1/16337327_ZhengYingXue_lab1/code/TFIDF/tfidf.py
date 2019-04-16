import math
import time
from numpy import *

# 去除前面的内容只保留句子
def delete(data):
    with open('semeval.txt') as file:
        for line in file:
            line = line.strip('\n')
            data.append(line.split('\t')[2])


# 生成不重复的词汇表。data:测试集样本的列表
def tran(data):
    voca = []
    for sentence in data:
        tmp = sentence.split(' ') #逐行分离各个词语
        for tmp1 in tmp:
            voca.append(tmp1)
    voca2 = sorted(set(voca), key=voca.index)  # 利用set函数去除列表中重复元素
    return voca2 #返回不重复的词汇表



# num:不重复词汇表的长度
def tfidf(data, vari, num):
    #生成TF矩阵
    tf = []
    idf = []
    for datas in data:
        tmp=datas.split(' ')#对每行语句的词分开
        tmp2=[]
        for varis in vari:
            tmp2.append(tmp.count(varis))#计算分开的所有词里该词的个数，加入该行的列表中
        tf.append(tmp2)#列表添加行元素成为嵌套列表
    tf=mat(tf)#嵌套列表转化为矩阵
    sum=tf.sum(axis=1)#对矩阵进行各行求和
    tf=tf/sum#归一化处理
    #生成idf矩阵
    for varis in vari:
        i=0
        for datas in data:
            tmp=datas.split(' ')
            if varis in tmp:
                i+=1#判断词是否在语句的词组列表中，如果在则该词存在的文章数+1
        idf.append(math.log(len(data)/(1+i),math.e))#进行idf计算
    for i in range(len(vari)):
        tf[:,i] *= idf[i]#tf*idf
    tfidf=tf
    return tfidf #返回计算好的TF-IDF矩阵


if __name__ == "__main__":
    starttime=time.clock()
    data = []
    delete(data)
    vari = tran(data)
    num = len(vari)
    tfidfmatrix=tfidf(data, vari, num)
    tfidfmatrix=tfidfmatrix.tolist()
    with open('16337327_ZhengYingXue_TFIDF.txt', 'w') as file:
        for i in range(len(tfidfmatrix)):
            for j in range(num):
                if tfidfmatrix[i][j] != 0:
                    file.write(str(float(tfidfmatrix[i][j])))
                    file.write(' ')
            file.write('\n')
    endtime = time.clock()
    print('Time:', endtime - starttime)
