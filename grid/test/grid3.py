import netCDF4 as nc
import numpy as np
import scipy.spatial
import networkx as nx
#from scipy.spatial.distance import pdist

data = nc.Dataset('dngrid_0001.nc','r')

latc = data.variables['latc'][:]
lonc = data.variables['lonc'][:]

z = np.vstack((latc,lonc)).T

#z = np.array([[1,1,2,3,3,15,16,6,16],[2,13,3,14,15,16,17,7,18],[14,14,14,15,4,4,18,19,19]]).T
#z = np. array([[66,67],[67,64],[66,64],[67,66],[68,50]])

points = map(tuple,z)

print 'Loaded'

# make a Delaunay triangulation of the point data
delTri = scipy.spatial.Delaunay(points)
print 'Delaunay Done'

# create a set for edges that are indexes of the points
edges = set()
# for each Delaunay triangle
for n in xrange(delTri.nsimplex):
    # for each edge of the triangle
    # sort the vertices
    # (sorting avoids duplicated edges being added to the set)
    # and add to the edges set
    edge = sorted([delTri.vertices[n,0], delTri.vertices[n,1]])
    edges.add((edge[0], edge[1]))
    edge = sorted([delTri.vertices[n,0], delTri.vertices[n,2]])
    edges.add((edge[0], edge[1]))
    edge = sorted([delTri.vertices[n,1], delTri.vertices[n,2]])
    edges.add((edge[0], edge[1]))

print 'Edges Done'

# make a graph based on the Delaunay triangulation edges
graph = nx.Graph(list(edges))
#print(graph.edges())

print 'Graph Made'

# plot graph
pointIDXY = dict(zip(range(len(points)), points))

#[-66.3391,44.2761] to [-66.3391,44.2799]
#17521 - 28527
#source = points[17521]
#target = points[28527]
#source = points[1]
#target = points[4]

def getTargets(source, target, coords=False):
    print '\n'
    print 'Source'
    print source
    print pointIDXY[source]
    print '\n'
    print 'Target'
    print target
    print pointIDXY[target]

    if coords:
        for key, value in pointIDXY.items():
            if value==source:
                print 'Source'
                print key
                s = key

            if value==target:
                print 'Target'
                print key
                t = key

    else:
        s = source
        t = target

    return s,t

#17521 - 28527
s,t = getTargets(17521,28527)

#shortest = nx.shortest_path(graph,source=s,target=t)
shortest = nx.shortest_path(graph,source=s,target=t)
dist = nx.shortest_path_length(graph,source=s,target=t)

coords = [pointIDXY[i] for i in shortest]

print '\n'
print 'Shortest Path (by elements)'
print shortest
print '\n'
print 'Shortest Path (by coordinates)'
print coords
print '\n'
print 'Shortest Distance (by coordinates)'
print dist
print '\n'


#print 'Done pointIDXY'
#print pointIDXY

#print 'Graphing'
#import matplotlib.pyplot as plt
#nx.draw(graph, pointIDXY)
#plt.show()



