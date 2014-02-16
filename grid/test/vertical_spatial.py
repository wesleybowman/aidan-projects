from __future__ import division
import numpy as np
import pandas as pd
import sys
sys.path.insert(0,'/home/aidan/thesis/probe_code/fvcomprobe/const_panels/')
from structFunc import conv_time
import netCDF4 as net
from multiprocessing import Pool
import matplotlib.pyplot as plt
import matplotlib.tri as tri

def time_index(a):
    a = a.reindex(index=a.index.to_datetime())
    return a

def magnitude(a):
    mag = np.sqrt(a['u']**2+a['v']**2+a['w']**2)
    return mag

def theta(a):
    a = np.arctan2(a['v'],a['u'])
    return a


if __name__ == "__main__":


    fileDir = '/home/aidan/thesis/ncdata/gp/2014/'
    filename = 'dngrid_0001.nc'
    siglay = np.array([0.98999,0.94999,0.86999,0.74999,0.58999,0.41000,0.25000,0.13000,0.05000,0.01000])
    ### BPb -TA
    #elements = [17521, 18093, 18092, 18643, 19188, 19702, 20191, 20685, 21180, 21675, 22185, 22705, 23228, 23758, 24283, 24782, 25275, 25774, 26276, 26759, 27219, 27653, 28084, 28527]

    ### south passage
    # top
    #elements = [41420, 41421, 41422, 41787, 41425, 41426, 41427, 41428, 41429, 41430, 41431, 41063, 41064, 40698, 40699, 40700, 40701, 40702, 40703, 40348, 40349, 40350, 40351, 40352, 40007, 40008, 39664, 39665, 39666, 39311, 39312, 39670, 39671, 39672, 39673, 39675, 39676, 39677, 39678, 39679, 39326, 39327, 39328, 39329, 39330, 39332, 39333, 39334, 38959, 38960, 38961, 38962, 38567, 38568, 38569, 38570, 38571, 38166, 38167, 38168, 38169, 38170, 38171, 38172, 38173, 38581, 38176, 38177, 38178, 38179, 38180, 38181, 38182, 37775, 37776, 37777, 37778, 37779, 38189, 38192, 38193, 38194, 38603, 38604, 38999, 39001, 39004, 39005, 38611, 38612, 38613, 38614, 38615, 38616, 39013, 39014, 39016, 39017, 39386, 39390, 39391, 39392, 39748, 39749, 39750, 39751, 39752, 39753, 39754, 39402, 39403, 39404, 39759, 39760, 39762, 39763]
    # bottom
    elements = [48484, 48485, 48885, 48886, 49295, 49296, 49717, 49718, 49299, 49300, 49301, 49302, 49303, 49725, 49726, 49727, 49728, 50156, 49732, 49733, 49734, 49735, 49736, 49737, 49317, 49318, 49319, 49742, 49743, 50169, 49746, 49747, 49748, 49749, 49750, 49751, 49752, 50177, 50178, 50613, 50181, 50182, 50183, 50616, 50620, 50621, 50188, 50189, 50190, 50191, 50192, 50193, 50194, 50195, 50196, 50197, 49773, 49774, 50201, 50202, 50203, 50204, 50205, 50206, 50641, 50642, 50643, 50644, 50645, 50214, 50215, 50216, 50217, 50218, 50653, 50654, 50655, 50656, 51097, 51098, 51099, 51100, 51101, 51102, 51103, 51104, 51105, 51106, 51107, 51108, 51555, 51556, 51557, 51558, 51559, 51560, 52009, 52010, 52011, 52012, 52469, 52016, 52017, 52018, 52019, 52020, 52022, 52023, 52024, 52479, 52482, 52483, 52484, 52485, 52486, 52951, 52952, 52953, 52492, 52493, 52494, 52958, 52961, 52962, 52963, 52964, 53435, 53436, 53438, 53439, 53441]
    ### north pass
    ### top pass
    #elements = [27241, 27240, 27239, 27238, 27237, 26777, 26294, 26293, 25789, 25290, 25289, 25288, 25287, 25285, 25282, 24789, 24788, 24288, 23760, 23229, 23228, 23227, 22701, 22700, 22698, 23222, 23221, 23220, 23749, 23748, 23747, 23746, 23745, 23744, 23212, 23211, 23210, 23209, 23208, 23207, 23206, 23205, 23204, 23203, 23201, 23200, 22673, 22671, 22670, 22669, 22668, 22666, 22665, 22664, 22667, 23188, 23187, 23186, 23185, 23184, 22656, 22655, 22654, 22653, 23177, 23704, 24227, 24226]^
    ### middle pass
    #elements = [21706, 21716, 22226, 22740, 60487, 61054, 18741, 63079, 18194, 64442, 65364, 65873, 66407, 31437, 32950, 33411, 57243, 58318, 58321, 58868, 59417, 59972, 60543, 61109, 61657, 61283, 61276, 61278, 61794, 61795, 61286, 60734, 60160, 59600, 59054, 59055, 58516, 58517, 58518, 59065, 59619, 60184, 60764, 61329, 64657, 57484, 56953, 54934, 54437, 37537, 37133, 36719, 36275, 35812, 38340, 37942, 30817, 34128, 32826, 29845, 22637, 18580, 18025, 18581, 18582, 18031, 18030, 17458]
    ### bottom pass
    #elements = [14587, 13974, 13975, 14598, 14599, 15225, 15226, 15853, 15854, 16458, 16459, 17038, 17617, 17621, 64442, 65364, 65873, 66407, 31437, 32950, 33411, 57243, 58318, 58321, 58868, 59417, 59972, 60543, 61109, 61657, 61283, 61276, 61278, 61794, 61795, 61286, 60734, 60160, 59600, 59054, 59055, 58516, 58517, 58518, 59065, 59619, 60184, 60764, 61329, 64657, 57484, 56953, 54934, 54437, 37537, 37133, 36719, 36275, 35812, 38340, 37942, 30817, 34128, 32826, 29845, 22637, 18580, 18025, 12060, 11492, 6540, 6940, 6544, 6153, 6154, 5775, 5416]

    nc = net.Dataset(fileDir+filename).variables
    time = nc['time'][:]+678942
    time = np.array([time]).transpose()
    time = conv_time(time)
    time = time.flatten()
    items = ['u','v','w']

    '''
    nodes = []
    for i,j in enumerate(elements):
        node = nc['nv'][:,j]
        h1 = nc['zeta'][:,node[0]]
        h2 = nc['zeta'][:,node[1]]
        h3 = nc['zeta'][:,node[2]]
        base1 = nc['h'][node[0]]+h1
        base2 = nc['h'][node[1]]+h2
        base3 = nc['h'][node[2]]+h3
        layers1 = np.outer(base1,siglay)
        layers2 = np.outer(base2,siglay)
        layers3 = np.outer(base3,siglay)
        layers = np.array([layers1,layers2,layers3])
        h = layers.mean(axis=0)
        nodes.append(h)

    nodes = np.array(nodes)
    '''

    #sys.exit()
    lat = []
    lon = []
    frames = []
    for i,j in enumerate(elements):
        print i
        u = nc['u'][:,:,j]
        v = nc['v'][:,:,j]
        w = nc['ww'][:,:,j]
        latitude = nc['latc'][j]
        longitude = nc['lonc'][j]
        dfp = pd.Panel(np.array([u,v,w]),items=items, major_axis=time,minor_axis=siglay)
        frames.append(dfp)
        lat.append(latitude)
        lon.append(longitude)
        #pd.Panel.to_pickle(dfp,'/home/aidan/thesis/probe_data/panels/2014/BPb-TA/el'+str(j))

    print 'done loop'

    #angle = Pool().map(theta,frames)
    #frames = Pool().map(magnitude,frames)
    #frames = Pool().map(time_index,frames)
    #angle = Pool().map(time_index,angle)

    newframe = []
    for i,j in enumerate(frames):
        print i
        a = magnitude(j)
        a = time_index(a)
        newframe.append(a)

    print 'done second loop'

    slices = np.linspace(50,150,100).astype(int)

    for a,b in enumerate(slices):
        f = []
        for i,j in enumerate(newframe):
            x = np.asarray(j.iloc[b]).flatten()
            f.append(x)

        f = np.array(f).transpose()
    print f
    print lat
    print lon

    '''
    fig,ax = plt.subplots()
    levels = np.linspace(0,3,50)
    cs = ax.contourf(lat,siglay,f,levels=levels)
    #ax.contour(lat,siglay,f,cs.levels,colors='k',hold='on')
    fig.colorbar(cs,ax=ax)
    plt.show()
    '''
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(lat,lon,siglay,f)
    plt.show()
