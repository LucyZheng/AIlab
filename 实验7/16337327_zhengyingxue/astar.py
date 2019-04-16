import copy
import time


class node:
    def __init__(self, value=-1, x=-1, y=-1, currentdata=[], father=None, gx=0, hx=0, fx=0):
        self.value = value#与0交换位置的数（可以作为路径输出）
        self.x = x#0的坐标
        self.y = y
        self.currentdata = currentdata#当前状态矩阵
        self.father = father#父节点
        self.gx = gx
        self.hx = hx
        self.fx = fx


behave = [[0, 1], [0, -1], [-1, 0], [1, 0]]  # 上下左右操作
open = []
close = []
flag = 0#是否找到解


def astar(node1, data, goaldis):
    for i in range(4):
        newx = node1.x + behave[i][0]
        newy = node1.y + behave[i][1]
        newgx = node1.gx + 1
        if newx > 3 or newx < 0 or newy > 3 or newy < 0:#越界跳过
            continue
        newdata = copy.deepcopy(data)
        tmp = data[newx][newy]
        newdata[node1.x][node1.y] = tmp
        newdata[newx][newy] = 0
        newnode = node(tmp, newx, newy, newdata, node1, newgx)#建立新节点
        newhx = 0
        for i in range(4):
            for j in range(4):
                if newdata[i][j] != 0:
                    a, b = goaldis[newdata[i][j]]
                    newhx += abs(i - a) + abs(j - b)#计算曼哈顿距离
        newnode.hx = newhx
        newnode.fx = newnode.hx + newnode.gx#计算f（n）
        for opens in open:
            if newnode.currentdata == opens.currentdata and opens.fx > newnode.fx:
                opens.fx = newnode.fx#有重复值则更新值
        open.append(newnode)#加入open表
    open.remove(node1)#open表里删除父节点
    close.append(node1)#父节点加入close表


if __name__ == '__main__':
    starttime = time.clock()
    data = [
        [10, 5, 8, 3],
        [1, 9, 2, 4],
        [13, 14,0, 6],
        [15, 7, 12, 11]
    ]
    goal = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    goaldis = [(-1, -1)]
    for i in range(4):
        for j in range(4):
            goaldis.append((i, j))#目标距离列表，包含所有目标结点的坐标，以便计算曼哈顿距离
    for i in range(4):#找到0值所在的坐标
        for j in range(4):
            if data[i][j]==0:
                firstx=i
                firsty=j
    x=node(-1,firstx,firsty,data)#起点建立
    open.append(x)
    tmpfather = None
    k = 0
    path = []
    while flag == 0 and len(open) != 0:#还没找到解时
        minfx = 10000
        minindex = 0
        for i in range(len(open)):
            if open[i].fx < minfx:
                minfx = open[i].fx
                minindex = i#找到f（n）最小的结点
        astar(open[minindex], open[minindex].currentdata, goaldis)#对它进行扩展
        for opens in open:
            if goal == opens.currentdata:#找到终点
                flag = 1
                path.append(opens.value)
                tmpfather = opens.father
    while tmpfather != None and tmpfather.value != -1:#通过终点的父节点在close表里搜索，直至追溯到起点
        path.append(tmpfather.value)
        tmpfather = tmpfather.father
    for i in range(len(path)):#倒序输出即为路径
        print(path[-1 - i],end=' ')
    print('\n')
    endtime = time.clock()
    print("step:",len(path))
    print("time:",endtime - starttime)
