import numpy as np
from collections import defaultdict
from itertools import combinations
triangles = [(1,2,3), (2,3,4), (1,3,5), (3,4,5), (5,6,7), (4,5,6)]


p = np.array([[1,1,2,3,3,15,16,6,16],[2,13,3,14,15,16,17,7,18],[14,14,14,15,4,4,18,19,19]])

data = map(tuple,p.T)

# For each edge set triangles containing that edge
edge2trias = defaultdict(list)  # edge (v1,v2) -> list of triangles
#for t_ind, ps in enumerate(triangles):
for t_ind, ps in enumerate(data):
    for edge in zip(ps, ps[1:]+ps[:1]):
        edge2trias[tuple(sorted(edge))].append(t_ind)
# For each edge, set pair(s) of neighbouring triangles
tria2neigh = defaultdict(list)  # triangle index -> list of neighbouring triangles
for edge, trias in edge2trias.iteritems():
    for t1, t2 in combinations(trias, 2):
        tria2neigh[t1].append(t2)
        tria2neigh[t2].append(t1)

print tria2neigh
