import time
import copy


class node:
    def __init__(self, value=-1, x=0, y=0, currentdata=[], gx=0, hx=0, fx=0):
        self.value = value #与0交换位置的数（可以作为路径输出）
        self.x = x #0的坐标
        self.y = y
        self.currentdata = currentdata#当前状态矩阵
        self.gx = gx
        self.hx = hx,
        self.fx = fx


stack = []  # 存放路径走过的结点
behave = [[0, 1], [0, -1], [-1, 0], [1, 0]]  # 上下左右操作
data = []  # 数据集
maxfx = 0
flag = 0  # 是否到达终点
morefx = []


def idastar(node1, nodedata, goaldis):
    global flag, maxfx
    if node1.fx > maxfx:
        morefx.append(node1.fx)#当前矩阵f（x）大于maxf（x）则回溯
        return
    if node1.currentdata == goal and flag == 0:#找到目标
        for item in stack:#输出深度搜索栈中的结点——形成路径
            if item.value != -1:
                print(item.value, end=' ')
        print('\n')
        print("step:", len(stack) - 1)
        flag = 1
        endtime = time.clock()
        print('time:', endtime - starttime)
        exit()#由深度优先搜索的性质，找到解即为最优解，退出
    for i in range(4):#空格进行上下左右移动
        newx = node1.x + behave[i][0]
        newy = node1.y + behave[i][1]
        newgx = node1.gx + 1#进行一次移动，gx+1
        if newx > 3 or newx < 0 or newy > 3 or newy < 0:
            continue
        newdata = copy.deepcopy(nodedata)
        tmp = nodedata[newx][newy]
        newdata[node1.x][node1.y] = tmp
        newdata[newx][newy] = 0
        newnode = node(tmp, newx, newy, newdata, newgx)
        newhx = 0
        for i in range(4):
            for j in range(4):
                if newdata[i][j] != 0:
                    a, b = goaldis[newdata[i][j]]
                    newhx += abs(i - a) + abs(j - b)#计算曼哈顿距离
        newnode.hx = newhx
        newnode.fx = newnode.hx + newnode.gx
        stack.append(newnode)#当前搜索的结点入栈
        idastar(newnode, newdata, goaldis)#继续深度搜索
        del (stack[-1])#回溯时删去该节点


if __name__ == '__main__':
    starttime = time.clock()
    data = [
        [0,5,1,7],
        [2,11,4,3],
        [9,13,6,15],
        [10,14,12,8]
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
            if data[i][j] == 0:
                firstx = i
                firsty = j
    x = node(-1, firstx, firsty, data, 0)#起点建立
    hx = 0
    for i in range(4):
        for j in range(4):
            if data[i][j] != 0:
                a, b = goaldis[data[i][j]]
                hx += abs(i - a) + abs(j - b)
    x.hx = hx
    x.fx = hx
    morefx.append(x.fx)#maxfx首先取起点的f（n）
    k = 0
    while flag == 0:
        stack = []
        stack.append(x)
        k += 1
        maxfx = max(morefx)
        print(k, 'round', time.clock(), 's', 'maxfx=' + str(maxfx))
        morefx = []
        idastar(x, data, goaldis)
