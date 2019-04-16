import time

class node:#结点结构
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
stack = []#存放路径走过的结点
visit = []#该点是否访问过
behave = [[0, 1], [0, -1], [-1, 0], [1, 0]]  # 上下左右操作
data = []#数据集
k = 0#允许探寻的最大层数
tmpk = 0#探索时的层数
flag = 0#是否到达终点


def dfs(x, y):
    global flag, tmpk, k
    if x < 1 or x > 16 or y < 1 or y > 34 or tmpk > k:  # 越界
        return
    if x == 16 and y == 2 and tmpk <= k:#到达终点且在当前可以探测的层数之内，则输出当前解，当前解就是最优解
        print('step:', len(stack))
        outdata = []
        for datas in data:
            tmp = []
            for datass in datas:
                tmp.append(datass)
            outdata.append(tmp)
        for j in range(len(stack)):
            outdata[stack[j].x][stack[j].y] = '*'
        for out1 in outdata:
            string = ''
            for out2 in out1:
                if out2 == 1:
                    string += '| '
                elif out2 == 0:
                    string += '  '
                elif out2 == '*':
                    string += '. '
                else:
                    string += 'E '
            print(string)
        flag = 1
        return
    for i in range(4):#上下左右操作
        newx = x + behave[i][0]
        newy = y + behave[i][1]
        if newx >= 1 and newx <= 16 and newy >= 1 and newy <= 34 and data[newx][newy] == 0 and visit[newx][
            newy] == 0 and data[newx][newy] != 8:
            visit[newx][newy] = 1
            current = node(newx, newy)
            stack.append(current)#满足条件，结点入栈，标记为访问过
            tmpk += 1#层数加1
            dfs(newx, newy)#递归访问下一节点
            visit[newx][newy] = 0#回溯时将回溯路径上结点标记为未访问
            del (stack[-1])#删除栈中回溯路径上的结点
            tmpk -= 1#层数减1


if __name__ == "__main__":
    starttime = time.clock()
    alldata = []
    with open('MazeData.txt') as file:
        for line in file:
            line = line.strip('\n')
            alldata.append(line)
    for datas in alldata:
        tmp = []
        tmpvisit = []
        for i in range(len(datas)):
            if datas[i] == '0':
                tmp.append(0)
            elif datas[i] == '1':
                tmp.append(1)
            else:
                tmp.append(8)
            tmpvisit.append(0)
        data.append(tmp)
        visit.append(tmpvisit)
    start = node(1, 34)
    stack.append(start)
    while flag == 0:
        tmpk = 0
        k += 1
        dfs(start.x, start.y)
    endtime = time.clock()
    print('time:', endtime - starttime)
