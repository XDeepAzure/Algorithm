
import copy
import time

from regex import P

def getChain(target):
    answers, seq = [[]], [1,]         #seq记录回溯中产生的答案，answers记录全部答案
    min_k = [target]
    def chain(k, seq, X_set):              #求解序列中seq[k]的值
        if k >= min_k[0]:
            return    
        #在树分叉的过程中防止分出相同的叉，ex[1,2,3] seq[i]+seq[j]=4,(i,j)=(0,2),(1,1)
        #待选值从前面算出来，所有待选值为X + （新增的seq[-1]与seq内所有值相加），且排除重复
        # for idx, v in enumerate(X_set):
        #     if v > seq[-1]: break
        # if X_set[idx] <= seq[-1]:
        #     idx +=1
        # X = X_set[idx:]                         #摘除小于seq[-1]的
        X = [v for v in X_set if v>seq[-1]]
        X += [v+seq[-1] for v in seq if (v+seq[-1] not in X) and (v+seq[-1]<=target)]
        # X += [v+seq[-1] for v in seq if v+seq[-1]<=target]
        # X = sorted(list(set(X)))
        for x in reversed(X):              #反过来遍历，能在小规模上提高速度
            if x < target:
                seq.append(x)
                chain(k+1, seq, X)
                seq.pop()
            elif x == target:
                min_k[0] = min(k, min_k[0])
                answers[0] = copy.deepcopy(seq)+[x]
        pass
    chain(1, seq, [2])
    return min_k[0], answers

def getPermute(n, T):
    C = set(range(1,n+1))               #待排元素集合
    answers, p = [], []                 #所有合法序列，当下序列
    def permute(C, max_three):
        if len(C) == 0:               #已经没有待排元素了
            answers.append(copy.deepcopy(p))
        else:
            lst = list(C)
            lst.sort()
            for x in lst:               #此时的lst是有序的
                if len(p) >= 2:
                    max_three = max(max_three, p[-2]+p[-1]+x)
                if max_three > T:       #基于此时lst有序来剪枝的
                    break
                p.append(x)
                C.discard(x)
                permute(C, max_three)
                C.add(x)
                p.pop()
    permute(C, -1)
    return answers

def problem1():
    """
    打印问题一中示例答案
    最短长度、[x1,...xl]、解决此target所用时间
    """
    targets = [8, 47, 71, 127, 191, 379, 607]
    for x in targets:
        start = time.process_time()
        print('-'*20)
        print(getChain(x), 'time=', time.process_time()-start)

def problem2():
    pairs = [(5, 9), (12, 21), (13, 23), (14, 24), (15, 25)]        #(n, T)
    for n, T in pairs:
        print('-'*30)
        start = time.process_time()
        print(getPermute(n, T), 'time=', time.process_time()-start)
    pass 
if __name__=='__main__':
    # problem1()
    problem2()
    pass