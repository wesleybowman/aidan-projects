import graph_tool.all as gt
import numpy as np
from scipy.spatial.distance import pdist, squareform
import netCDF4 as nc
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path
#import matplotlib.pyplot as plt


data = nc.Dataset('dngrid_0001.nc','r')

latc = data.variables['latc'][:]
lonc = data.variables['lonc'][:]

points = np.vstack((latc,lonc)).T
print 'Loaded'

points = np.array([[66,67],[67,64],[66,64],[67,66],[68,50],[40,50],[70,80],[65,65]])
dist = pdist(points)
print dist.shape
p = squareform(points)
graph = csr_matrix(p)
print graph.shape

#s = shortest_path(graph)

#print s



