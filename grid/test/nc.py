import netCDF4 as nc
import numpy as np

data = nc.Dataset('dngrid_0001.nc','r')

latc = data.variables['latc']
lonc = data.variables['lonc']

print 'Loaded'
print latc[:]
print lonc[:]


z = np.vstack((latc[:],lonc[:]))

print 'Z'
print z.T


print z
