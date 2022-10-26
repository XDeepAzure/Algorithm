'''
无向图，用邻接表实现
'''

from functools import reduce
import os
from typing import List


class UndirectedGraph():
    def __init__(self, edges: List[List[int]]) -> None:
        self.vertices = []
        if len(edges) > 0:
            self.vertices = list(set(reduce(lambda x, y:x+y, edges)))
        self.v_nums = max(self.vertices) +1
        self.vertices = [i for i in range(self.v_nums)]
        self.edges = [[] for _ in range(self.v_nums)]
        for v, m in edges:      #邻接表
            if m not in self.edges[v]:
                self.edges[v].append(m)
            if v not in self.edges[m]:
                self.edges[m].append(v)

        pass
    def getAllAdjEdge(self, v) -> List[List[int]]:
        #ex: [[2,4],[2,3]]      感觉这里用元组更好些
        return [[v, i] for i in self.edges[v]]
        pass
    def getAllEdge(self) -> List[List[int]]:
        '''
        返回所有的边
        '''
        return [[v, w] for v in range(self.v_nums) for w in self.edges[v]]
        pass
    def DFS(self, v: int, visited: List[bool], visit=lambda self,x: print(x) ):
        visited[v] = True
        visit(self, v)
        adj_vertices = self.getAllAdjEdges(v)
        for item in adj_vertices:
            m = item[1]
            if visited[m] == False:
                self.DFS(m, visited, visit)
        pass
    pass

def stackPop(stack: List, edge: List[int]):
    '''
    从stack进行pop直到pop出的边和edge一样， 返回pop出的所有边
    List[Tuple(int, int)]
    '''
    def isSame(x, edge):
        x= sorted(x)
        for i in range(len(x)):
            if x[i]!=edge[i]:
                return False
        return True
    
    edge, ans, x = sorted(edge), [], stack.pop()
    while not isSame(x, edge):
        ans.append(x)
        x = stack.pop()
    ans.append(x)
    return ans
    pass

def computeBCC(G: UndirectedGraph):
    '''
    输入无向图，返回此图的双连通分量的列表
    返回示例[[[1,2],[2,3],[1,3]],...]
    '''
    t, stack, bcc= [0], [], []                 #t:dfs访问次序
    parent = [-1 for _ in range(G.v_nums)]  #parent[v]记录顶点v在dfs树中的父亲结点
    #用来记录顶点v深度优先搜索序列中的编号
    D = [0 for _ in range(G.v_nums)]
    #Low[v] 以v为根的⼦树通过回边所能到达的最⾼顶点的编号，初始值与D保持一致
    Low = [0 for _ in range(G.v_nums)]
    def dfsbcc(v:int):
        t[0] += 1
        Low[v] = D[v] = t[0]
        child_nums = 0  #v的孩子的个数
        for _, w in G.getAllAdjEdge(v):
            if D[w] == 0:     #也做visited之用
                parent[w] = v
                child_nums += 1
                stack.append([v,w])
                dfsbcc(w)
                Low[v] = min(Low[v], Low[w])
                #判断v是不是割点
                if (D[v] == 0 and child_nums > 1) or (0 < D[v] <= Low[w]):
                    bcc.append(stackPop(stack, [v, w]))
            else:   #当w已经访问过了，那么（v,w）是一条回边
                if parent[v] != w:
                    Low[v] = min(Low[v], D[w])
                    if D[w] < D[v]:
                        stack.append([v, w])
        pass
    dfsbcc(0)
    return bcc
    pass

def read_graph_file(root:str = './'):
    def strs2int(string:str) -> List[int]:
        #ex: '2 4' => [1, 3]    减1是为了让顶点从0开始
        return list(map(lambda x: int(x)-1, string.split(' ')[:2]))
    dirs = os.listdir(root)
    graph_text = []
    for text in dirs:
        if text[-4:] == '.txt' and text[:11] == 'problem8.11':
            path = os.path.join(root, text)
            data = ''
            with open(path) as f:
                data = f.readlines()
            data = [row for row in data if row!='\n']
            data = list(map(strs2int, data))        #data: List[List[1,2]]
            graph_text.append(data)
    return graph_text
def getAnwser():
    """返回图双连通分量的所有边
    """
    graph_lst = read_graph_file()
    graph_lst.append([[0,2],[2,1],[1,0],[0,3],[1,3]])
    for idx, g in enumerate(graph_lst):
        graph = UndirectedGraph(g)
        print(f'----------- 第{idx}个无向图 -----双连通分量为------')
        for x in computeBCC(graph):
            print(x)
    pass

if __name__ == '__main__':
    # stack = [[1,2],[2,3],[3,4],[4,5]]
    # edge = [3,2]
    # print(stackPop(stack, edge))
    getAnwser()
    pass
