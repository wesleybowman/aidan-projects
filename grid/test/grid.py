from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from itertools import combinations
from scipy.spatial import KDTree
from scipy.spatial.distance import pdist

def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def func(a):
    return list(combinations(a,2))

p = np.array([[1,1,2,3,3,15,16,6,16],[2,13,3,14,15,16,17,7,18],[14,14,14,15,4,4,18,19,19]])
#point = np.random.randint(0,10,size=(3,20))

print p.T
data2 = map(tuple,p.T)
print data2
#data2 = map(tuple,point.T)

edges = map(func,data2)
print edges


G = nx.Graph()

for i in edges:
    G.add_edges_from(i)

shortest = nx.shortest_path(G,source=1,target=7)
print shortest
#print nx.triangles(G)

nx.draw(G)
plt.show()



#data = pd.DataFrame(p)

#d={}
#for i in data:
    #d[i]= data[i].values

#print d[0]
#print d.has_key(0)
#for i in d[0]:
#    print i
#
#new = {'A':['B','C'],
#       'B':['D','C','A','E','H'],
#       'C':['B','A','E','F'],
#       'D':['B','H','E','F','G'],
#       'E':['B','C','D','F'],
#       'F':['E','C','D','G'],
#       'G':['D','F']
#       }
#
#
#
#paths = find_shortest_path(new,'A','G')
#print paths
