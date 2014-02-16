from mayavi import mlab
import numpy as np
import networkx as nx
import netCDF4 as nc

def compute_delaunay_edges(x, y, visualize=False):
    """ Given 3-D points, returns the edges of their
        Delaunay triangulation.

        Parameters
        -----------
        x: ndarray
            x coordinates of the points
        y: ndarray
            y coordinates of the points
        z: ndarray
            z coordinates of the points

        Returns
        ---------
        new_x: ndarray
            new x coordinates of the points (same coords but different
            assignment of points)
        new_y: ndarray
            new y coordinates of the points (same coords but different
            assignment of points)
        new_z: ndarray
            new z coordinates of the points (same coords but different
            assignment of points)
        edges: 2D ndarray.
            The indices of the edges of the Delaunay triangulation as a
            (N, 2) array [[pair1_index1, pair1_index2],
                          [pair2_index1, pair2_index2],
                          ...                         ]
    """
    vtk_source =  mlab.pipeline.scalar_scatter(x, y, figure=False)
    delaunay =  mlab.pipeline.delaunay(vtk_source)
    delaunay.filter.offset = 999    # seems more reliable than the default
    edges = mlab.pipeline.extract_edges(delaunay)

    # We extract the output array. the 'points' attribute itself
    # is a TVTK array, that we convert to a numpy array using
    # its 'to_array' method.
    new_x, new_y = edges.outputs[0].points.to_array().T
    lines = edges.outputs[0].lines.to_array()
    return new_x, new_y, np.array([lines[1::3], lines[2::3]]).T


def graph_plot(x, y, z, start_idx, end_idx, edge_scalars=None, **kwargs):
    """ Show the graph edges using Mayavi

        Parameters
        -----------
        x: ndarray
            x coordinates of the points
        y: ndarray
            y coordinates of the points
        z: ndarray
            z coordinates of the points
        edge_scalars: ndarray, optional
            optional data to give the color of the edges.
        kwargs:
            extra keyword arguments are passed to quiver3d.
    """
    vec = mlab.quiver3d(x[start_idx],
                        y[start_idx],
                        z[start_idx],
                        x[end_idx] - x[start_idx],
                        y[end_idx] - y[start_idx],
                        z[end_idx] - z[start_idx],
                        scalars=edge_scalars,
                        mode='2ddash',
                        scale_factor=1,
                        **kwargs)
    if edge_scalars is not None:
        vec.glyph.color_mode = 'color_by_scalar'
    return vec


def build_geometric_graph(x, y, z, edges):
    """ Build a NetworkX graph with xyz node coordinates and the node indices
        of the end nodes.

        Parameters
        -----------
        x: ndarray
            x coordinates of the points
        y: ndarray
            y coordinates of the points
        z: ndarray
            z coordinates of the points
        edges: the (2, N) array returned by compute_delaunay_edges()
            containing node indices of the end nodes. Weights are applied to
            the edges based on their euclidean length for use by the MST
            algorithm.

        Returns
        ---------
        g: A NetworkX undirected graph

        Notes
        ------
        We don't bother putting the coordinates into the NX graph.
        Instead the graph node is an index to the column.
    """
    xyz = np.array((x, y, z))
    def euclidean_dist(i, j):
        d = xyz[:,i] - xyz[:,j]
        return np.sqrt(np.dot(d, d))

    g = nx.Graph()
    for i, j in edges:
        if nx.__version__.split('.')[0] > '0':
            g.add_edge(i, j, weight=euclidean_dist(i, j))
        else:
            g.add_edge(i, j, euclidean_dist(i, j))
    return g


def points_on_sphere(N):
    """ Generate N evenly distributed points on the unit sphere centered at
        the origin. Uses the 'Golden Spiral'.
        Code by Chris Colbert from the numpy-discussion list.
    """
    phi = (1 + np.sqrt(5)) / 2  # the golden ratio
    long_incr = 2*np.pi / phi   # how much to increment the longitude

    dz = 2.0 / float(N)         # a unit sphere has diameter 2
    bands = np.arange(N)        # each band will have one point placed on it
    z = bands * dz - 1 + (dz/2) # the height z of each band/point
    r = np.sqrt(1 - z*z)        # project onto xy-plane
    az = bands * long_incr      # azimuthal angle of point modulo 2 pi
    x = r * np.cos(az)
    y = r * np.sin(az)
    return x, y, z


################################################################################
if __name__ == '__main__':
    # generate some points
    #x, y, z = points_on_sphere(50)
    # Avoid triangulation problems on the sphere
    #z *= 1.01

    data = nc.Dataset('dngrid_0001.nc','r')

    latc = data.variables['latc'][:]
    lonc = data.variables['lonc'][:]

    x = latc
    y = lonc

    points = np.vstack((latc,lonc)).T
    print 'Loaded'

    mlab.figure(1, bgcolor=(0,0,0))
    mlab.clf()

    # Now get the Delaunay Triangulation from vtk via mayavi mlab. Vtk stores
    # its points in a different order so overwrite ours to match the edges
    new_x, new_y, edges = compute_delaunay_edges(x, y, visualize=True)
    assert(x.shape == new_x.shape)   # check triangulation got everything
    x, y = new_x, new_y

    if nx.__version__ < '0.99':
        raise ImportError('The version of NetworkX must be at least '
                    '0.99 to run this example')

    # Make a NetworkX graph out of our point and edge data
    g = build_geometric_graph(x, y, edges)

    # Compute minimum spanning tree using networkx
    # nx.mst returns an edge generator
    edges = nx.minimum_spanning_tree(g).edges(data=True)
    start_idx, end_idx, _ = np.array(list(edges)).T
    start_idx = start_idx.astype(np.int)
    end_idx   = end_idx.astype(np.int)

    # Plot this with Mayavi
    graph_plot(x, y, start_idx, end_idx,
                opacity=0.8,
                colormap='summer',
                line_width=4,
                )

    mlab.view(60, 46, 4)
    mlab.show()
