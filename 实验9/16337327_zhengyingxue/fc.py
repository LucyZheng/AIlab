import time
num=0
def nqueen(k, n, location, domain):
    global num
    if k > n:#上一行已经是最后一行
        for i in range(1, n + 1):
            print(location[i], end=" ")
        print("\t")#输出解
        num += 1#解的个数+1
        return#继续寻找下一个解
    if len(domain[k]) == 0:#如果当前行可选值域为空集，则回溯
        return
    for i in domain[k]:#对当前行的值域的每一个可选项
        location[k] = i#因为可选，所以可以直接赋值
        newdomain = {0:[]}
        for i1 in range(1, n + 1):#深复制domain字典
            tmp = [datas for datas in domain[i1]]
            newdomain[i1]=tmp
        for j in range(k + 1, n + 1):#对接下来的行，在domain里删除不满足约束条件的值
            if i in newdomain[j]:
                newdomain[j].remove(i)
            if i+(j-k) in newdomain[j]:
                newdomain[j].remove(i + (j - k))
            if i - (j - k) >= 1 and i-(j-k) in newdomain[j]:
                newdomain[j].remove(i - (j - k))
        nqueen(k + 1, n, location, newdomain)#对新的domain字典递归搜索当前的子节点


if __name__ == "__main__":

    location = []
    n = input("请输入n：")
    n = int(n)
    start = time.clock()
    for i in range(0, n + 1):
        location.append(0)
    domain = {0:{}}
    for i in range(1, n + 1):
        tmp={}
        for j in range(1, n + 1):
            tmp[j]=j
        domain[i]=tmp


    nqueen(1, n, location, domain)
    end = time.clock()
    print("解的个数为：", num)
    print("花费时间为：", end - start)
