class VariableElimination:
    @staticmethod
    #factor_list:所有变量的列表 query_variables:所求的变量的概率,
    #ordered_list_of_hidden_variables#消除变量的顺序, evidence_list#条件变量
    def inference(factor_list, query_variables, ordered_list_of_hidden_variables, evidence_list):
        for key, value in evidence_list.items():#如果有条件限制则进行投影操作，把包含条件概率变量的因子全部投影化
            for vars in factor_list:
                if key in vars.var_list:
                    factor_list[factor_list.index(vars)] = vars.restrict(key, str(value))
        for var in ordered_list_of_hidden_variables:
            eliminate = []#对每个消除变量进行操作
            for var2 in factor_list:
                if var in var2.var_list:
                    eliminate.append(var2)#添加包含这个变量的因子
            for var3 in eliminate:
                factor_list.remove(var3)#在原来的表里删除这些因子
            tmp = eliminate[0]
            del(eliminate[0])
            while len(eliminate) != 0:
                tmp = tmp.multiply(eliminate[0])
                del(eliminate[0])#对这些因子的各个情况求积
            tmp=tmp.sum_out(var)#求和操作
            factor_list.append(tmp)#因子列表里添加新的因子
        print("RESULT: ")
        res = factor_list[0]
        for factor in factor_list[1:]:
            res = res.multiply(factor)
        total = sum(res.cpt.values())
        res.cpt = {k: v / total for k, v in res.cpt.items()}
        res.print_inf()

    @staticmethod
    def print_factors(factor_list):
        for factor in factor_list:
            factor.print_inf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.var_list = var_list
        self.cpt = {}

    def set_cpt(self, cpt):
        self.cpt = cpt

    def print_inf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.var_list))
        for key in self.cpt:
            print("   key: " + key + " val : " + str(self.cpt[key]))
        print()

    def multiply(self, factor):
        '''function that multiplies with another factor'''
        # Your code here
        new_list = []
        for i in range(len(self.var_list)):
            if self.var_list[i] in factor.var_list:
                theindex = factor.var_list.index(self.var_list[i])
                new_list = self.var_list + factor.var_list[:theindex] + factor.var_list[theindex + 1:]#对新的变量进行结合两个因子的命名
                break
        new_cpt = {}
        for key1, value1 in self.cpt.items():
            for key2, value2 in factor.cpt.items():
                if key1[i] == key2[theindex]:#如果当前变量在两个因子里值相等
                    new_cpt[key1 + key2[:theindex] + key2[theindex + 1:]] = value1 * value2#则计算乘积
        new_node = Node('f' + str(new_list), new_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def sum_out(self, variable):
        '''function that sums out a variable given a factor'''
        # Your code here
        new_var_list=[]
        new_cpt={}
        for vars in self.var_list:
            new_var_list.append(vars)
        theindex=self.var_list.index(variable)
        new_var_list.remove(variable)#删除需要求和的变量
        for key,value in self.cpt.items():
            if key[:theindex]+key[theindex+1:] in new_cpt.keys():#如果求和变量已经在列表里面了
                new_cpt[key[:theindex]+key[theindex+1:]]+=value#则相加
            else:
                new_cpt[key[:theindex]+key[theindex+1:]]=value#否则创建新的键值
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        '''function that restricts a variable to some value
        in a given factor'''
        # Your code here
        new_var_list=[]
        new_cpt = {}
        index = self.var_list.index(variable)
        for var in self.var_list:
            new_var_list.append(var)
        new_var_list.remove(variable)#删除需要投影的变量名
        for key, values in self.cpt.items():
            if key[index] == value:
                new_cpt[key[:index] + key[index + 1:]] = values#如果当前变量值是投影值，则赋值
        new_node = Node('f' + str(new_var_list), new_var_list)
        new_node.set_cpt(new_cpt)
        return new_node


# Create nodes for Bayes Net
B = Node('B', ['B'])
E = Node('E', ['E'])
A = Node('A', ['A', 'B', 'E'])
J = Node('J', ['J', 'A'])
M = Node('M', ['M', 'A'])

# Generate cpt for each node
B.set_cpt({'0': 0.999, '1': 0.001})
E.set_cpt({'0': 0.998, '1': 0.002})
A.set_cpt({'111': 0.95, '011': 0.05, '110': 0.94, '010': 0.06,
           '101':0.29, '001': 0.71, '100': 0.001, '000': 0.999})
J.set_cpt({'11': 0.9, '01': 0.1, '10': 0.05, '00': 0.95})#(A,J)
M.set_cpt({'11': 0.7, '01': 0.3, '10': 0.01, '00': 0.99})






print("P(A) **********************")
VariableElimination.inference([B, E, A, J, M], ['A'], ['B', 'E', 'J', 'M'], {})

print("P(B | J, ~M) **********************")
VariableElimination.inference([B, E, A, J, M], ['B'], ['E', 'A'], {'J':1, 'M':0})
