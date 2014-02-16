import graph_tool.all as gt
import numpy as np
from scipy.spatial.distance import pdist
import netCDF4 as nc
#import matplotlib.pyplot as plt

#ppoints = np. array([[66,67],[67,64],[66,64],[67,66],[68,50],[40,50]])

data = nc.Dataset('dngrid_0001.nc','r')

latc = data.variables['latc'][:]
lonc = data.variables['lonc'][:]

ppoints = np.vstack((latc,lonc)).T
print 'Loaded'

tri, pos = gt.triangulation(ppoints, type="delaunay")
print 'Done Triangulation'

weight = tri.new_edge_property("double")

for e in tri.edges():
    weight[e] = np.sqrt(sum((np.array(pos[e.source()]) - np.array(pos[e.target()]))**2))

print 'Done weighting'

b = gt.betweenness(tri, weight=weight)
b[1].a *= 120

dist = gt.shortest_distance(tri,tri.vertex(0),tri.vertex(5),weights=weight)
path, elist = gt.shortest_path(tri,tri.vertex(0),tri.vertex(5))

print 'Done shortest distance and path'
print 'dist'
print dist
print 'path'
for i in path:
    print i


gt.graph_draw(tri, vertex_text=tri.vertex_index, edge_text=tri.edge_index,
              edge_pen_width=b[1], output_size=(1000,1000), output="triang.pdf")


#weights = pdist(ppoints)
#print weights

#pos = gt.sfdp_layout(tri)
#gt.graph_draw(tri, eweight=weights, pos=pos, output="sfdp.pdf")
