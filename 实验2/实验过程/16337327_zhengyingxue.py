from numpy import *
from graphviz import Digraph
import csv


class node:
    def __init__(self, character=-1, result=-1, child={}, mostresult=-1):
        self.character = character  # 该节点分裂选择的特征
        self.result = result  # 该节点的值，若为叶节点则不为-1，默认为-1，即该节点没有值（还需继续分裂）
        self.child = child  # 字典结构，为{类别：子节点}
        self.mostresult = mostresult  # 该节点的数据集中多数值


def createdatabase(data, filename):  # 读取数据
    with open(filename) as file:
        for line in file:
            line = line.strip('\n')
            data.append(line.split(','))


def informationgainprobablity(data, hd):  # 计算信息增益率
    datalen = len(data)
    maxgd = -10000
    prefercol = 0
    for i in range(len(data[0]) - 1):
        hda = 0
        chadic = {}  # 分支中各个情况的样本个数
        valuedic = {}  # 分支中各个情况的结果（1或0的和）
        for datas in data:
            if datas[i] not in chadic.keys():
                chadic[datas[i]] = 1
                valuedic[datas[i]] = int(datas[-1])
            else:
                chadic[datas[i]] += 1
                valuedic[datas[i]] += int(datas[-1])
        splitinfo = 0
        tmpsum = 0
        for values in chadic.values():
            tmpsum += values
        for values in chadic.values():  # 计算属性的熵
            splitinfo += -(values / tmpsum) * log2(values / tmpsum) - (1 - values / tmpsum) * log2(1 - values / tmpsum)
        for key in chadic.keys():  # 计算信息增益
            if valuedic[key] == 0 or chadic[key] == valuedic[key]:
                hda += 0
            else:
                hda += (chadic[key] / datalen) * (-valuedic[key] / chadic[key] * log2(valuedic[key] / chadic[key]) - (
                        1 - valuedic[key] / chadic[key]) * log2(1 - valuedic[key] / chadic[key]))
        if (hd - hda) / splitinfo > maxgd:  # 寻找最大的信息增益率
            maxgd = (hd - hda) / splitinfo
            prefercol = i
    return prefercol


def informationgain(data, hd):  # 计算信息增益
    datalen = len(data)
    maxgd = -10000
    prefercol = 0
    for i in range(len(data[0]) - 1):
        hda = 0
        chadic = {}  # 分支中各个情况的样本个数
        valuedic = {}  # 分支中各个情况的结果（1或0的和）
        for datas in data:
            if datas[i] not in chadic.keys():
                chadic[datas[i]] = 1
                valuedic[datas[i]] = int(datas[-1])
            else:
                chadic[datas[i]] += 1
                valuedic[datas[i]] += int(datas[-1])
        for key in chadic.keys():  # 计算信息增益
            if valuedic[key] == 0 or chadic[key] == valuedic[key]:
                hda += 0
            else:
                hda += (chadic[key] / datalen) * (-valuedic[key] / chadic[key] * log2(valuedic[key] / chadic[key]) - (
                        1 - valuedic[key] / chadic[key]) * log2(1 - valuedic[key] / chadic[key]))
        if hd - hda > maxgd:  # 寻找最大的信息增益
            maxgd = hd - hda
            prefercol = i
    return prefercol


def gini(data):  # 计算GINI系数
    mingini = 10000
    prefercol = 0
    for i in range(len(data[0]) - 1):
        chadic = {}  # 分支中各个情况的样本个数
        valuedic = {}  # 分支中各个情况的结果（1或0的和）
        for datas in data:
            if datas[i] not in chadic.keys():
                chadic[datas[i]] = 1
                valuedic[datas[i]] = int(datas[-1])
            else:
                chadic[datas[i]] += 1
                valuedic[datas[i]] += int(datas[-1])
        tmpsum = 0  # 数据总个数
        for values in chadic.values():
            tmpsum += values
        gini = 0
        for key in chadic.keys():
            gini += (1 - (valuedic[key] / chadic[key]) ** 2 - (1 - valuedic[key] / chadic[key]) ** 2) * (
                    chadic[key] / tmpsum)
        if gini < mingini:  # 寻找最小的gini系数
            mingini = gini
            prefercol = i
    return prefercol


def createtree(root, data, hd, preresult, i, k):  # 递归建树
    characterdic = {}  # 当前的特征字典，根据当前数据集生成
    for j in range(len(data[0]) - 1):
        characterdic[j] = []
        for datas in data:
            if datas[j] not in characterdic[j]:
                characterdic[j].append(datas[j])

    if len(data) == 0:  # 若当前分类的数据集为0，则等于父节点中存在最多的值
        root.result = preresult
        return
    datadic = {}
    tmp = []
    flag = 0
    sum = 0
    for datas in data:
        sum += int(datas[-1])
    if sum < len(data) / 2:
        tmpresult = 0
    else:
        tmpresult = 1
    root.mostresult = tmpresult  # 找到当前数据集中最多出现的值
    for datas in data:
        tmp.append(datas[-1])
    if len(set(tmp)) == 1:  # 是否数据集的值相同
        flag = 1
    if len(data[0]) > 1 and flag == 0:  # 若数据集的值不相同，则建立子节点
        root.child = {}
    elif flag == 1:  # 否则，该节点的值为这个数据集的值
        root.result = int(tmp[0])
        return
    else:
        root.result = tmpresult  # 为叶节点：叶节点的值为最多出现的值
        return

    if k == '0':  # 根据K的不同选择不同的判别规则
        character = informationgain(data, hd)
    elif k == '1':
        character = informationgainprobablity(data, hd)
    else:
        character = gini(data)

    root.character = character
    for datass in characterdic[character]:
        root.child[datass] = node()
        datadic[datass] = []
    for datas in data:
        datadic[datas[character]].append(datas)  # 数据集字典为当前数据集的一个划分
    for values in datadic.values():
        for disdata in values:
            del (disdata[character])  # 在数据集中删去特征
    for key in root.child.keys():
        createtree(root.child[key], datadic[key], hd, tmpresult, 0, k)
    return


def findtheresult(testroot, testdatas):  # 遍历决策树，找到最终的值
    preresult = 0
    while testroot.result == -1:
        if testdatas[testroot.character] not in testroot.child.keys():
            return testroot.mostresult
        index = testroot.character
        testroot = testroot.child[testdatas[testroot.character]]
        del (testdatas[index])

    return testroot.result


def printtree(root, lastname):  # 利用graphviz画图
    testdic = root.child
    for keys in testdic:
        if root.result != -1:
            lastname1 = root.result
            dot.node(str(lastname1))#节点名称
            dot.edge(str(lastname), str(lastname1), str(root.result))#在前两个点之间建立一条边并标记为第三个参数
            return
        else:
            lastname1 = lastname + '->' + keys#通过路径名称是独一无二的这一特性标记节点
            dot.node(str(lastname1))
            dot.edge(str(lastname), str(lastname1), keys)
            printtree(root.child[keys], lastname1)


if __name__ == "__main__":
    alldata = []
    k = input("choose the model: 0-ID3  1-C4.5  2-CART:")
    tree = {}
    createdatabase(alldata, 'Car_train.csv')
    for datas in alldata:  # 在每一列特征后添加属性下标，以便查看
        datas[0] += '(cha0)'
        datas[1] += '(cha1)'
        datas[2] += '(cha2)'
        datas[3] += '(cha3)'
        datas[4] += '(cha4)'
        datas[5] += '(cha5)'
    data = alldata
    root = node()
    sum = 0
    length = 0
    for datas in data:
        sum += int(datas[len(datas) - 1])
        length += 1
    a = sum / length
    hd = -log2(a) * a - log2(1 - a) * (1 - a)
    dot = Digraph(comment='The Decision Tree')
    dot.node('root')
    createtree(root, data, hd, -1, 0, k)
    printtree(root, 'root')
    dot.render('test-output/test-table.gv', view=True)
    testdata = []
    createdatabase(testdata,'car_test_with_label.csv')
    for datas in testdata:  # 在每一列特征后添加属性下标，以便查看
        datas[0] += '(cha0)'
        datas[1] += '(cha1)'
        datas[2] += '(cha2)'
        datas[3] += '(cha3)'
        datas[4] += '(cha4)'
        datas[5] += '(cha5)'
    testresult = []
    sum = 0
    with open("16337327_zhengyingxue.csv", "w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for testdatas in testdata:
            testroot = root
            tmp=[]
            tmp.append(findtheresult(testroot, testdatas))
            if(str(tmp[-1])==str(testdatas[-1])):
                sum+=1
            testresult.append(tmp)
        writer.writerows(testresult)
    print('Accuracy:',sum/len(testdata)*100,'%')