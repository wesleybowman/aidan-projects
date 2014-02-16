from pylab import *
import matplotlib.tri as Tri
import netCDF4
import datetime as dt
from datatools import *
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap


if __name__ == "__main__":
    fs2 = [-66.3392,44.2762]
    fs3 = [-66.3421,44.2606]
    fs4 = [-66.3354,44.2605]
    fs5 = [-66.3381,44.2505]
    GPBPa = [-66.3395,44.2778]
    GPBPb = [-66.3391,44.2761]
    GPTA = [-66.3391,44.2799]
    GPTAJ = [-66.3380,44.2743]
    podlon = np.array([fs2[0],fs3[0],fs4[0],fs5[0],GPBPa[0],GPBPb[0],GPTA[0],GPTAJ[0]])
    podlat = np.array([fs2[1],fs3[1],fs4[1],fs5[1],GPBPa[1],GPBPb[1],GPTA[1],GPTAJ[1]])

    fileDir = '/home/aidan/thesis/ncdata/gp/2014/'
    filename = 'dngrid_0001.nc'
    timeInt = [00,1000]

    #data = load_timeslice(fileDir,timeInt[0],timeInt[1],singlename=filename,dim='2D')
    #data = ncdatasort(data)

    nc = netCDF4.Dataset(fileDir+filename).variables

    # Get Connectivity array
    nv = nc['nv'][:].T - 1
    # Get trigrid
    #trigrid = nc['trigrid']
    # Get depth
    h = nc['h'][:]
    # Get x,y coordinates
    x = nc['x'][:]
    y = nc['y'][:]
    # Get lon,lat coordinates for nodes (depth)
    lat = nc['lat'][:]
    lon = nc['lon'][:]
    # Get lon,lat coordinates for cell centers (depth)
    latc = nc['latc'][:]
    lonc = nc['lonc'][:]

    tri = Tri.Triangulation(lon,lat, triangles=nv) #xy or latlon based on how you are #Grand Passage

    levels=arange(-38,-4,1)   # depth contours to plot

    fig = plt.figure(figsize=(18,10))
    plt.rc('font',size='22')
    ax = fig.add_subplot(111,aspect=(1.0/cos(mean(lat)*pi/180.0)))
    plt.tricontourf(tri, -h,levels=levels,shading='faceted',cmap=plt.cm.gist_earth)
    plt.triplot(tri)
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.gca().patch.set_facecolor('0.5')
    cbar=colorbar()
    cbar.set_label('Water Depth (m)', rotation=-90,labelpad=30)

    scale = 1
    ticks = ticker.FuncFormatter(lambda lon, pos: '{0:g}'.format(lon/scale))
    ax.xaxis.set_major_formatter(ticks)
    ax.yaxis.set_major_formatter(ticks)
    plt.grid()

    elements = [41420, 41421, 41422, 41787, 41425, 41426, 41427, 41428, 41429, 41430, 41431, 41063, 41064, 40698, 40699, 40700, 40701, 40702, 40703, 40348, 40349, 40350, 40351, 40352, 40007, 40008, 39664, 39665, 39666, 39311, 39312, 39670, 39671, 39672, 39673, 39675, 39676, 39677, 39678, 39679, 39326, 39327, 39328, 39329, 39330, 39332, 39333, 39334, 38959, 38960, 38961, 38962, 38567, 38568, 38569, 38570, 38571, 38166, 38167, 38168, 38169, 38170, 38171, 38172, 38173, 38581, 38176, 38177, 38178, 38179, 38180, 38181, 38182, 37775, 37776, 37777, 37778, 37779, 38189, 38192, 38193, 38194, 38603, 38604, 38999, 39001, 39004, 39005, 38611, 38612, 38613, 38614, 38615, 38616, 39013, 39014, 39016, 39017, 39386, 39390, 39391, 39392, 39748, 39749, 39750, 39751, 39752, 39753, 39754, 39402, 39403, 39404, 39759, 39760, 39762, 39763]

    el2 = [48484, 48485, 48885, 48886, 49295, 49296, 49717, 49718, 49299, 49300, 49301, 49302, 49303, 49725, 49726, 49727, 49728, 50156, 49732, 49733, 49734, 49735, 49736, 49737, 49317, 49318, 49319, 49742, 49743, 50169, 49746, 49747, 49748, 49749, 49750, 49751, 49752, 50177, 50178, 50613, 50181, 50182, 50183, 50616, 50620, 50621, 50188, 50189, 50190, 50191, 50192, 50193, 50194, 50195, 50196, 50197, 49773, 49774, 50201, 50202, 50203, 50204, 50205, 50206, 50641, 50642, 50643, 50644, 50645, 50214, 50215, 50216, 50217, 50218, 50653, 50654, 50655, 50656, 51097, 51098, 51099, 51100, 51101, 51102, 51103, 51104, 51105, 51106, 51107, 51108, 51555, 51556, 51557, 51558, 51559, 51560, 52009, 52010, 52011, 52012, 52469, 52016, 52017, 52018, 52019, 52020, 52022, 52023, 52024, 52479, 52482, 52483, 52484, 52485, 52486, 52951, 52952, 52953, 52492, 52493, 52494, 52958, 52961, 52962, 52963, 52964, 53435, 53436, 53438, 53439, 53441]

    #elements = [41420, 41050, 40681, 40324, 40677, 39274, 42531, 42928, 43334, 43738, 44142, 44545, 44929, 46826, 48444, 32007, 50529, 50971, 32977, 32976, 55214, 56724, 57243, 58318, 58321, 58868, 59417, 59972, 60543, 61109, 61657, 61283, 61276, 61278, 61279, 60726, 60154, 59596, 59050, 59049, 58509, 58508, 57974, 57443, 56917, 56416, 55917, 55411, 54916, 54913, 54418, 53939, 53941, 54425, 54427, 54929, 55431, 40847, 41211, 41203, 41199, 40834, 40832, 40474, 40472, 40471, 40470, 40469, 40468, 40466, 40115, 40111, 39763]
    scatter(nc['lonc'][elements],nc['latc'][elements],s=80)#,label='Flow Station 2, 2012',color='red')
    scatter(nc['lonc'][el2],nc['latc'][el2],s=80,label='Flow Station 3, 2012',color='brown')
    #scatter(podlon[2],podlat[2],s=80,label='Flow Station 4, 2012',color='blue')
    #scatter(podlon[3],podlat[3],s=80,label='Flow Station 5, 2012',color='purple')
    #scatter(podlon[4],podlat[4],s=80,label='GP-130620-BPa',color='yellow')
    #scatter(podlon[5],podlat[5],s=80,label='GP-130620-BPb',color='orange')
    #scatter(podlon[6],podlat[6],s=80,label='GP-130730-TA',color='magenta')
    #scatter(podlon[7],podlat[7],s=80,label='GP-120904-TA',color='brown')
    legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2, ncol=3,fontsize='14', borderaxespad=0.)
    plt.show()
