from pomegranate import *
#图：C&M->S,A&S->M2,S&P->D
#pcma概率
patientage = DiscreteDistribution({'0-30': 0.1, '31-65': 0.3, '65+': 0.6})
ctscanresult = DiscreteDistribution({'I': 0.7, 'H': 0.3})
mriscanresult = DiscreteDistribution({'I': 0.7, 'H': 0.3})
anticoagulants = DiscreteDistribution({'U': 0.5, 'N': 0.5})
#s条件概率
stroketype=ConditionalProbabilityTable(
    [['I','I','I',0.8],
     ['I','H','I',0.5],
     ['H','I','I',0.5],
     ['H','H','I',0],
     ['I','I','H',0],
     ['I','H','H',0.4],
     ['H','I','H',0.4],
     ['H', 'H','H',0.9],
     ['I','I','S',0.2],
     ['I','H','S',0.1],
     ['H','I','S',0.1],
     ['H','H','S',0.1]
     ],
    [ctscanresult,mriscanresult]
)
#m2条件概率
mortality=ConditionalProbabilityTable(
    [['I','U','F',0.28],
     ['H','U','F',0.99],
     ['S','U','F',0.1],
     ['I','N','F',0.56],
     ['H','N','F',0.58],
     ['S','N','F',0.05],
     ['I','U','T',0.72],
     ['H','U','T',0.01],
     ['S','U','T',0.9],
     ['I','N','T',0.44],
     ['H','N','T',0.42],
     ['S','N','T',0.95]
     ],
    [stroketype,anticoagulants]
)
#d条件概率
disability=ConditionalProbabilityTable(
    [
        ['I','0-30','N',0.8],
        ['H','0-30','N',0.7],
        ['S','0-30','N',0.9],
        ['I','31-65','N',0.6],
        ['H','31-65','N',0.5],
        ['S', '31-65', 'N', 0.4],
        ['I', '65+', 'N', 0.3],
        ['H', '65+', 'N', 0.2],
        ['S', '65+', 'N', 0.1],
        ['I', '0-30', 'M', 0.1],
        ['H', '0-30', 'M', 0.2],
        ['S', '0-30', 'M', 0.05],
        ['I', '31-65', 'M', 0.3],
        ['H', '31-65', 'M', 0.4],
        ['S', '31-65', 'M', 0.3],
        ['I', '65+', 'M', 0.4],
        ['H', '65+', 'M', 0.2],
        ['S', '65+', 'M', 0.1],
        ['I', '0-30', 'S', 0.1],
        ['H', '0-30', 'S', 0.1],
        ['S', '0-30', 'S', 0.05],
        ['I', '31-65', 'S', 0.1],
        ['H', '31-65', 'S', 0.1],
        ['S', '31-65', 'S', 0.3],
        ['I', '65+', 'S', 0.3],
        ['H', '65+', 'S', 0.6],
        ['S', '65+', 'S', 0.8],
    ],
    [stroketype,patientage]
)
#添加结点
sp=Node(patientage,name='patientage')
sc=Node(ctscanresult,name='ctscanresult')
sm=Node(mriscanresult,name='mriscanresult')
ss=Node(stroketype,name='stroketype')
sa=Node(anticoagulants,name='anticoagulants')
sd=Node(disability,name='disability')
sm2=Node(mortality,name='mortality')
#构建贝叶斯网络
model=BayesianNetwork('task3')
model.add_states(sp,sc,sm,ss,sa,sd,sm2)
#添加边
model.add_edge(sc,ss)
model.add_edge(sm,ss)
model.add_edge(sa,sm2)
model.add_edge(ss,sm2)
model.add_edge(ss,sd)
model.add_edge(sp,sd)
#生成网络
model.bake()
#预测概率
print(model.predict_proba({'patientage':'0-30','ctscanresult':'I'}))
print('--------')
print(model.predict_proba({'patientage':'65+','mriscanresult':'I'}))
print('--------')
print(model.predict_proba({'patientage':'65+','ctscanresult':'H','mriscanresult':'I'}))
print('--------')
print(model.predict_proba({'patientage':'0-30','anticoagulants':'U','stroketype':'S'}))
print('--------')
#联合概率
print(model.probability([['0-30','I','H','S','U','S','F']]))