文件说明
KNN：KNN跑训练集，但是由于训练集太大+numpy占内存过大，所以会造成电脑很卡+准确率也不高，写完后就跑过一次，请无视。
NB：朴素贝叶斯算法训练的模型，跑一次约10分钟。
词汇处理：对训练集数据进行的处理，在处理完训练集之后要将文件名改成测试集的名字再处理一次。
vocabulary.txt：停用词表。
请先跑词汇处理.py，再跑NB.py
使用word2vec库词向量处理经过验证发现在这个程序里对正确率没有什么提高，加上朴素贝叶斯本身就很快，所以不提交上来了。