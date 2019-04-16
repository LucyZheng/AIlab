from numpy import *


class node:
    def __init__(self, character=-1, result=-1, child=None, mostresult=-1):
        self.character = character  # 该节点分裂选择的特征
        self.result = result  # 该节点的值，若为叶节点则不为-1，默认为-1，即该节点没有值（还需继续分裂）
        self.child = child  # 字典结构，为{类别：子节点}
        self.mostresult = mostresult  # 此节点中的数据集偏多的结果


def createdatabase(data, filename):
    with open(filename) as file:
        for line in file:
            line = line.strip('\n')
            data.append(line.split(','))


def gini(data):
    datalen = len(data)
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
        tmpsum=0 #数据总个数
        for values in chadic.values():
            tmpsum+=values
        gini=0
        for key in chadic.keys():
            gini+=(1-(valuedic[key]/chadic[key])**2-(1-valuedic[key]/chadic[key])**2)*(chadic[key]/tmpsum)
        if gini<mingini:
            mingini=gini
            prefercol=i
    return prefercol


def createtree(root, data, hd, preresult, i):
    characterdic = {}
    for j in range(len(data[0]) - 1):
        characterdic[j] = []
        for datas in data:
            if datas[j] not in characterdic[j]:
                characterdic[j].append(datas[j])

    if len(data) == 0:
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
    root.mostresult = tmpresult
    for datas in data:
        tmp.append(datas[-1])
    if len(set(tmp)) == 1:
        flag = 1
    if len(data[0]) > 1 and flag == 0:
        root.child = {}
    elif flag == 1:
        root.result = int(tmp[0])
        return
    else:
        root.result = tmpresult
        return

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
        createtree(root.child[key], datadic[key], hd, tmpresult, 0)
    return


def findtheresult(testroot, testdatas):
    preresult = 0
    while testroot.result == -1:
        if testdatas[testroot.character] not in testroot.child.keys():
            return testroot.mostresult
        index = testroot.character
        testroot = testroot.child[testdatas[testroot.character]]
        del (testdatas[index])

    return testroot.result


if __name__ == "__main__":
    alldata = []
    tree = {}
    createdatabase(alldata, 'Car_train.csv')
    for datas in alldata:
        if datas[0]=='vhigh' or datas[0]=='high':
            datas[0]='vhigh-high'
        else:
            datas[0]='med-low'
        if datas[1]=='vhigh' or datas[1]=='high':
            datas[1]='vhigh-high'
        else:
            datas[1]='med-low'
        if datas[2]=='2' or datas[2]=='3':
            datas[2]='2-3'
        else:
            datas[2]='4-5more'
        if datas[3]=='more' or datas[3]=='4':
            datas[3]='4-more'
        if datas[4]=='big' or datas[4]=='med':
            datas[4]='med-big'
        if datas[5]=='low' or datas[5]=='med':
            datas[0]='low-med'
    print(alldata)
    data = alldata[:999]
    root = node()
    sum = 0
    length = 0
    for datas in data:
        sum += int(datas[len(datas) - 1])
        length += 1
    a = sum / length
    hd = -log2(a) * a - log2(1 - a) * (1 - a)
    createtree(root, data, hd, -1, 0)
    testdata = alldata[999:]
    testresult = []
    sum = 0
    for testdatas in testdata:
        testroot = root
        testresult.append(findtheresult(testroot, testdatas))
        if testresult[-1] == int(testdatas[-1]):
            sum += 1
    print(sum / len(testdata))
    # print(json.dumps(tree1, indent=5))
