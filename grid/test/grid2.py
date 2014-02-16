from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from itertools import combinations,izip
from scipy.spatial import KDTree
from scipy.spatial.distance import pdist
[(66, 67), (68, 50)]
from scipy.spatial import Delaunay

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


points = np. array([[66,67],[67,64],[66,64],[67,66]])

    #p.append(v+({'weight':weights[i]},))
lat = np.array([66,67,66,67,68,68])
lon = np.array([67,64,64,66,65,50])

coord = izip(list(lat),list(lon))

weights =  pdist(points)

print 'coord with weights'
p = []
points = []
for i,v in enumerate(coord):
    points.append(v)
    p.append(v)

print p

weights = izip(p,pdist(p))
pointsWithWeights = []
for i in weights:
    pointsWithWeights.append(i)

print 'pointsWithWeights'
print pointsWithWeights

tri = Delaunay(points)

print 'points'
print points
print 'tripoints'
print tri.points
print 'list'
print list(points)
pairs = combinations(list(p),2)

#pairs = combinations(p,2)


pw = []

print 'pairs'
for i in pairs:
    print i
    pw.append(list(i))

final = []

for i,v in enumerate(pdist(tri.points)):
    j = {'weight':v}
    #pw[i].append(j)
    z = tuple(pw[i])+(j,)
    print z
    final.append(z)

print pw
print final


G = nx.Graph()
#G.add_edges_from([(66,67),(67,64),])
for i in final:
    G.add_edges_from([i])
#
shortest = nx.shortest_path(G,source=(66,67),target=(68,50))
print shortest
nx.draw(G)
plt.show()


points = np. array([[66,67],[67,64],[66,64],[67,66],[68,50]])
tri = Delaunay(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.show()

#t = izip(pw,pdist(tri.points))


#print 't \n'
#for i in t:
#    print i


#G.add_edges_from()


