import string

dictionary = []
with open('vocabulary.txt', 'r', encoding='UTF-8') as file:  # 读取训练集的句子
    for line in file:
        line = line.strip('\n')
        dictionary.append(line)
dictionary.append('rrb')
dictionary.append('lrb')
data = []
table = str.maketrans(string.punctuation + string.digits, ' ' * (len(string.punctuation) + len(string.digits)))
with open('testData.txt', 'r', encoding='UTF-8') as file:  # 读取训练集的句子
    for line in file:
        line = line.strip('\n').replace('n\'t', 'nt').replace('\'s', 's')
        data.append(line.translate(table))
voca = []
delete={}
with open('testout.txt', 'w', encoding='UTF-8') as file2:
    for sentences in data:
        j = 0
        tmp = sentences.split(' ')
        for tmp1 in tmp:
            if tmp1 != ''  and tmp1 not in dictionary:
                file2.write(tmp1 + ' ')
                voca.append(tmp1)
            j += 1
            if j > 153:
                break
        file2.write('\n')
file2.close()
voca2 = set(voca)
i = 0
with open('out2.txt', 'w', encoding='UTF-8') as file3:
    for vocas in voca2:
        i += 1
        file3.write(vocas + ' ')
print(i)
