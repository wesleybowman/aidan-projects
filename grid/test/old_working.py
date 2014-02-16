import netCDF4 as nc
import numpy as np
import scipy.spatial
import networkx as nx
import matplotlib.pyplot as plt

class shortest_element_path:
    def __init__(self, filename):

        data = nc.Dataset(filename,'r')

        latc = data.variables['latc'][:]
        lonc = data.variables['lonc'][:]

        z = np.vstack((latc,lonc)).T

        self.points = map(tuple,z)

        print 'Loaded'

        # make a Delaunay triangulation of the point data
        self.delTri = scipy.spatial.Delaunay(self.points)
        print 'Delaunay Done'

        # create a set for edges that are indexes of the points
        self.edges = set()
        self.weight = []
        # for each Delaunay triangle
        for n in xrange(self.delTri.nsimplex):
            # for each edge of the triangle
            # sort the vertices
            # (sorting avoids duplicated edges being added to the set)
            # and add to the edges set

            self.edge = sorted([self.delTri.vertices[n,0], self.delTri.vertices[n,1]])
            a = self.points[self.edge[0]]
            b = self.points[self.edge[1]]
            self.weight.append(np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2))
            self.edges.add((self.edge[0], self.edge[1]))

            self.edge = sorted([self.delTri.vertices[n,0], self.delTri.vertices[n,2]])
            a = self.points[self.edge[0]]
            b = self.points[self.edge[1]]
            self.weight.append(np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2))
            self.edges.add((self.edge[0], self.edge[1]))


            self.edge = sorted([self.delTri.vertices[n,1], self.delTri.vertices[n,2]])
            a = self.points[self.edge[0]]
            b = self.points[self.edge[1]]
            self.weight.append(np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2))
            self.edges.add((self.edge[0], self.edge[1]))

        print 'Edges Done'

        print self.weight
        # make a graph based on the Delaunay triangulation edges
        self.graph = nx.Graph(list(self.edges),weight=self.weight)
        #print(graph.edges())

        print 'Graph Made'

        self.pointIDXY = dict(zip(range(len(self.points)), self.points))

    def getTargets(self, source, target, coords=False):
        print '\n'
        print 'Source'
        print source
        #print pointIDXY[source]
        print 'Target'
        print target
        #print pointIDXY[target]

        if coords:
            for key, value in self.pointIDXY.items():
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

        shortest = nx.shortest_path(self.graph,source=s,target=t)
        dist = nx.shortest_path_length(self.graph,source=s,target=t)


        print 'Shortest Path (by elements)'
        print shortest

        if coords:
            coords = [self.pointIDXY[i] for i in shortest]
            print 'Shortest Path (by elements)'
            print coords

        print 'Shortest Distance (by coordinates)'
        print dist

        return shortest

    def graph(self):
        nx.draw(self.graph, self.pointIDXY)
        plt.show()



if __name__ == '__main__':

    filename = 'dngrid_0001.nc'

    test = shortest_element_path(filename)

    shortest = test.getTargets(41420,39763)
    shortest = test.getTargets(48484,53441)
    shortest = test.getTargets(27241,24226)
    shortest = test.getTargets(21706,17458)
    shortest = test.getTargets(14587,5416)


