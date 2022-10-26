'''
程序流程在getAnswer()里执行
'''

from distutils.log import error
from functools import reduce
import os
from typing import Dict, List

class DirectedGraph:
    def __init__(self, edges: List[List[int]]) -> None:
        #顶点从0开始，下标从0开始
        #获得顶点集合
        self.vertices = []
        if len(edges) > 0:#这样筛选出有边的点，对于图中只有一个孤点的图来说，会把孤点漏掉，但在本页没有什么影响
            self.vertices = list(set(reduce(lambda x, y:x+y, edges)))
        #边矩阵
        self.v_nums = max(self.vertices) + 1
        self.vertices = [i for i in range(self.v_nums)]
        self.edges = [[0 for i in range(self.v_nums)] for j in range(self.v_nums)]
        for x, y in edges:
            self.edges[x][y] = 1
        #顶点的F值
        self.F = [-1 for i in range(self.v_nums)]
        pass
    def getAllEdges(self) -> List[List[int]] :
        #ex: [[2,4],[1,2]]
        return [[i, j] for i in range(self.v_nums) for j in range(self.v_nums)  if self.edges[i][j]==1 ]
    def getAllAdjEdges(self, v) -> List[List[int]]:
        '''
        返回以v为起点的所有边的集合
        ''' 
        return [[v, index] for index, value in enumerate(self.edges[v]) if value==1]
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

    def getAllInDegree(self) -> List[int]:
        '''
        下标默认是顶点号
        '''
        in_degree = [0 for _ in range(self.v_nums)]
        for index, row in enumerate(self.edges):
            for col, x in enumerate(self.edges[index]):
                if x==1:
                    in_degree[col] += 1
        return in_degree
        pass
    def toPoSort(self):
        cur_lable = [self.v_nums]
        visited = [False for _ in range(cur_lable[0])]
        def explore(v):  #cur_lable是数值不是引用类型所以不能像self用
            visited[v] = True
            for n, m in self.getAllAdjEdges(v):
                if not visited[m]:
                    explore(m)
            self.F[v] = cur_lable[0]
            cur_lable[0] -= 1

        for x in self.vertices:
            if not visited[x]:
                explore(x)
        return self.F
        pass
    def reserved(self):
        '''
        将所有边反转，[2,3] => [3,2]
        :return:
        '''
        edges = self.getAllEdges()
        for item in edges:
            item.reverse()
        return DirectedGraph(edges)
        pass


class AdjDirectedGraph:
    """有向图的邻接表实现
    """
    def __init__(self, edges: List[List[int]]) -> None:
        #顶点从0开始，下标从0开始
        #获得顶点集合
        self.vertices = []
        if len(edges) > 0:#这样筛选出有边的点，对于图中只有一个孤点的图来说，会把孤点漏掉，但在本页没有什么影响
            self.vertices = list(set(reduce(lambda x, y:x+y, edges)))
        #边矩阵
        self.v_nums = max(self.vertices) + 1
        # self.vertices = [i for i in range(self.v_nums)]
        self.edges = [[] for _ in range(self.v_nums)]
        i = 0
        for x, y in edges:
            self.edges[x].append(y)
        #顶点的F值
        # self.F = [-1 for i in range(self.v_nums)]
        pass
    def getAllEdges(self) -> List[List[int]] :
        #ex: [[2,4],[1,2]]
        return [[i, j] for i in range(self.v_nums) for j in self.edges[i]]
        pass
    def getAllAdjEdges(self, v) -> List[List[int]]:
        '''
        返回以v为起点的所有边的集合
        ''' 
        return [[v, index] for index in self.edges[v]]
    def toPoSort(self):
        cur_lable = [self.v_nums]
        F = [-1 for _ in range(self.v_nums)]
        visited = [False for _ in range(cur_lable[0])]
        def explore(v):  #cur_lable是数值不是引用类型所以不能像self用
            visited[v] = True
            for n, m in self.getAllAdjEdges(v):
                if not visited[m]:
                    explore(m)
            F[v] = cur_lable[0]
            cur_lable[0] -= 1

        for x in range(self.v_nums):
            if not visited[x]:
                explore(x)
        return F
        pass
    def reserved(self):
        '''
        将所有边反转，[2,3] => [3,2]
        :return:
        '''
        edges = self.getAllEdges()
        for item in edges:
            item.reverse()
        return AdjDirectedGraph(edges)
        pass


def read_graph_file(root:str = './'):
    def strs2int(string:str) -> List[int]:
        #ex: '2 4' => [1, 3]    减1是为了让顶点从0开始
        return list(map(lambda x: int(x)-1, string.split(' ')[:2]))
    dirs = os.listdir(root)
    graph_text = []
    for text in dirs:
        if text[-4:] == '.txt':
            path = os.path.join(root, text)
            data = ''
            with open(path) as f:
                data = f.readlines()
            data = [row for row in data if row!='\n']
            data = list(map(strs2int, data))        #data: List[List[1,2]]
            graph_text.append(data)
    return graph_text

def kasaraju(G: AdjDirectedGraph) -> List[int]:
    #scc[v]记录顶点v的强连通分量序号
    scc = [-1 for _ in range(G.v_nums)]
    G_r = G.reserved()          #将所有边反转
    g_f =G_r.toPoSort()         #compute f-values
    visited = [False for _ in range(G.v_nums)]
    num_scc = [-1]              #联通分量从0开始计数
    def explore(v):             #深度遍历
        visited[v] = True
        scc[v] = num_scc[0]
        for n, m in G.getAllAdjEdges(v):
            if not visited[m]:
                explore(m)

    g_f = [[index, value] for index, value in enumerate(g_f)]
    g_f.sort(key=lambda x:x[1])
    for v, f in g_f:
        if not visited[v]:
            num_scc[0] += 1
            explore(v)
    return scc
    pass

def getResult(scc: List[int]) -> Dict:
    '''
    返回字典{key=强连通分量序号: value=[此连通分量中的顶点序号], 以len(value)降序排列
    '''
    dic = dict()
    for v, idx in enumerate(scc):
        dic.setdefault(idx, []).append(v)
    dic = dict(sorted(dic.items(), key=lambda x:len(x[1]), reverse=True))
    return dic
    pass

def getAnswer() -> List[int]:
    '''
    返回文件要求的形式
    '''
    graph_lst = read_graph_file('./challenge')    #将测试例子文件放在当前文件夹下，可自动读取 挑战的数据集在这'./challenge'
    graph_lst.append([[0,2],[2,1],[1,0],[1,2],[1,3]])
    for idx, g in enumerate(graph_lst):
        print('---------构建图')
        graph = AdjDirectedGraph(g)               #构建图
        print('---------图构建完成')
        print('---------计算强连通分量')
        scc = kasaraju(graph)                     #计算强连通分量
        answer = [0 for _ in range(5)]
        i = 0
        for v in getResult(scc).values():
            if i >= 5:
                break
            answer[i] = len(v)
            i += 1
        print('answer:', answer)
    pass

if __name__ == '__main__':
    getAnswer()
    pass
