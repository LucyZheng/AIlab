import time
class node:#结点结构
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
stack = []#存放路径走过的结点
stacks = []#存放所有可达到目标的路径
minstep = 10000#判断最小路径的变量
length=[]
index = 0
bestindex = 0#判断最小路径的下标
visit = []#该点是否访问过
behave = [[0, 1], [0, -1], [-1, 0], [1, 0]]  # 上下左右操作
data = []#数据集
starttime=0

def dfs(x, y):
    global starttime
    global minstep
    global index
    global bestindex
    if x < 1 or x > 16 or y < 1 or y > 34:  # 越界
        return
    if x == 16 and y == 2:#到达终点
        print('step:', len(stack))
        outdata = []#输出迷宫及路线
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
        endtime = time.clock()
        print('time:', endtime - starttime)
        print('\n---\n')
        stacks.append(outdata)#当前可到达目标的路径存储起来
        length.append(len(stack))
        index += 1
        if minstep > len(stack):#判断是否是最短路径的结果
            minstep = len(stack)
            bestindex = index
        return
    for i in range(4):#上下左右操作
        newx = x + behave[i][0]
        newy = y + behave[i][1]
        if newx >= 1 and newx <= 16 and newy >= 1 and newy <= 34 and data[newx][newy] == 0 and visit[newx][
            newy] == 0 and data[newx][newy] != 8:
            visit[newx][newy] = 1
            current = node(newx, newy)
            stack.append(current)#满足条件，结点入栈，标记为访问过
            dfs(newx, newy)#递归访问下一节点
            visit[newx][newy] = 0#回溯时将回溯路径上结点标记为未访问
            del (stack[-1])#删除栈中回溯路径上的结点


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
    dfs(start.x, start.y)
    print('bestpath:')
    for j in range(len(length)):
        if length[j]==minstep:
            for out1 in stacks[j]:
                string = ""
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
    print('the minstep is:', minstep)
    endtime = time.clock()
    print('time:', endtime - starttime)