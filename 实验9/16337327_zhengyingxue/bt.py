import time
num=0
def nqueen(k, n, location):
    global num
    if k > n:#上一行已经是最后一行
        for i in range(1, n + 1):
            print(location[i], end=" ")
        print("\t")#输出解
        num += 1#解的个数+1
        return#继续寻找下一个解
    for i in range(1,n+1):#对每一列来说
        flag=1
        for j in range(1,k):
            if i==location[j] or k-j==abs(i-location[j]):#跟前面判断过的行有冲突，则该位置不可行，继续外循环
                flag=0
                break
        if (flag):#如果该位置可行，则该行位置为当前判断的列标志
            location[k]=i
            nqueen(k+1,n,location)#递归搜索当前情况的子树


if __name__ == "__main__":

    location = []
    n = input("请输入n：")
    n = int(n)
    start = time.clock()
    for i in range(0, n + 1):
        location.append(0)
    nqueen(1, n, location)
    end = time.clock()
    print("解的个数为：", num)
    print("花费时间为：", end - start)
