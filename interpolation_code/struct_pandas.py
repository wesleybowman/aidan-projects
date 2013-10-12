from __future__ import division
import numpy as np
import pandas as pd
from probeMerge import *
import scipy as sp
from scipy.interpolate import Rbf
from scipy import interpolate
from multiprocessing import Pool
import os as os
from datetime import datetime, timedelta
import csv
import matplotlib.pyplot as plt
from interp import linear

# From Robie, load in the appropriate probe data and organise it.
def loadProbe(data):
    print 'Loading Probe data'
    datadir = data
    specifer = 'L*'
    files = glob.glob(datadir + specifer)
    loc = []
    for File in files:
        item = os.path.basename(File)
        num = re.search("\d", item).start()
        end = item.index('_')
        loc.append(int(item[num:end]))
    num_locs = max(loc)
    data_entries = len(files)/num_locs
    loc = np.array(loc)
    data_entries = np.unique(loc)
    indiv_locs = []
    for i in data_entries:
        curr_loc = np.where(loc == i)[0]
        indiv_locs.append([files[j] for j in curr_loc])
    probes = dict_probe(indiv_locs)
    print 'Probe Data loaded'
    return probes

# find the mean height of an element in the grid based of the average height of
# the surrounding nodes.
def sigmas(dicto,local,siglay):
    pos1 = str(local)+'el1-01'
    pos2 = str(local)+'el2-01'
    pos3 = str(local)+'el3-01'
    me = np.array([dicto[pos1],dicto[pos2],dicto[pos3]])
    maxx = np.mean(me,axis=0)
    mean = np.outer(maxx,siglay)
    return mean,maxx

#Load and extract out the necessary data from a .mat file and separate out the
#data
def matdata(matDir):
    adcp = {}
    adcp.update(sp.io.loadmat(matDir))
    d = adcp['data']
    t = adcp['time']
    p = adcp['pres']
    p =p[0,0]
    t = t[0,0]
    time = t['mtime']
    pres = p['surf']
    data = d[0,0]
    u = data['east_vel']
    w = data['vert_vel']
    v = data['north_vel']
    binss = data['bins']
    return u,v,w,binss,time,pres

#Based on the elevation from either fvcom or adcp files we find the bin that is
#just below the water level.
def find_closest(A, target):
    #A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    return idx

# This doesn't work, don't worry about it.
def probe_interp(i):
    print i
    rbu = Rbf(el[i,:],uu[i,:])
    rbv = Rbf(el[i,:],vv[i,:])
    rbw = Rbf(el[i,:],ww[i,:])
    f = np.transpose(rbu(binss))
    g = np.transpose(rbv(binss))
    h = np.transpose(rbw(binss))
    interp_u.append([i, f])
    interp_v.append([i, g])
    interp_w.append([i, h])
    return interp_u,interp_v,interp_w

# This converts the int date value from fvcom or the adcp to a datetime object
# that is used to index the dataframes.
def conv_time(data):
    l = []
    d = data.flatten()
    dl = len(d)
    print 'begin time conversion'
    for i in xrange(dl):
        date=datetime.fromordinal(int(d[i]))+timedelta(days=d[i]%1)-timedelta(days=366)
        date.isoformat(' ')
        date = date.strftime("%Y-%m-%d %H:%M:%S") # This takes out the millisecond component ie rounds
        l.append(date)
    array = np.array([l])
    print 'time converted'
    return array

if __name__ == "__main__":

    #load adcp ndata and make the time conversion
    matDir = '/home/wesley/github/aidan-projects/interpolation_code/Flow_Stn4.mat'
    u,v,w,binss,time,pres = matdata(matDir)
    time = conv_time(time)
    print 'done conversion for adcps'

    #load probe data works only for 3d files apparently
    #3d
    probeDir = '/home/wesley/github/aidan-projects/interpolation_code/'
    probes = loadProbe(probeDir)

    #2d load and prepare to merge datasets for a year long dataframe
    """
    datadir1 = '/home/aidan/thesis/ncdata/gp/gp_f0.015/2d_probe_data/jan1/'
    datadir2 = '/home/aidan/thesis/ncdata/gp/gp_f0.015/2d_probe_data/jan2/'
    jan1 = loadProbe(datadir1)
    jan2 = loadProbe(datadir2)
    """

    #calculate the elevations of each sigma layer
    siglay = np.array([0.98999,0.94999,0.86999,0.74999,0.58999,0.41000,0.25000,0.13000,0.05000,0.01000])
    el,el_tot = sigmas(probes,4,siglay)

    #For 2d load in all data and set variables.
    """
    times1 = jan1['time']+678942
    times1 = conv_time(times1)
    times2 = jan2['time']+678942
    times2 = conv_time(times2)

    uu1 =jan1['7ua-01'][:,0]
    vv1 =jan1['7va-01'][:,0]
    el1 =jan1['7el2-01'][:,0]
    print uu1.shape
    print el1.shape

    uu = jan2['7ua-01'][:,0]
    vv = jan2['7va-01'][:,0]
    el2 = jan2['7el2-01'][:,0]
    print uu.shape
    print el2.shape
    #raw_input('d')
    """

    #For 3d set variables and prep for interpolations
    uu = probes['4u-01']
    vv = probes['4v-01']
    ww = probes['4w-01']
    times = probes['time']+678941.986112 #original value from mitchell 678942
    #subtract 20 minutes
    print times.shape
    times = conv_time(times)

    #interpolate sigma layer speeds to adcp depths with parallization. Does not
    #work
    """
    interp_u = []
    interp_v = []
    interp_w = []
    _, a = times.shape
    p = Pool()
    c =  p.map(probe_interp, xrange(a))
    #c,v,b =  p.map(probe_interp, xrange(a))
    a = np.array(c)
    print a.shape
    """
    #interpolate the sigma layer simulated speeds to the adcp heights
    #change in Rbf to 'linear', which was not the default.
    onetime = times.flatten()
    t = len(onetime)

#for i in xrange(t):
#    print i
#    rbf = Rbf(el[i,:],uu[i,:],function='linear')
#    rbv = Rbf(el[i,:],vv[i,:],function='linear')
#    rbw = Rbf(el[i,:],ww[i,:],function='linear')
#    f = np.transpose(rbf(binss))
#    g = np.transpose(rbv(binss))
#    h = np.transpose(rbw(binss))
#    if i == 0:
#        interp_u = f
#        interp_v = g
#        interp_w = h
#    else:
#        interp_u = np.vstack((interp_u,f))
#        interp_v = np.vstack((interp_v,g))
#        interp_w = np.vstack((interp_w,h))
#print 'done'

#Use fortran for the interpolation
    binss = binss.flatten()
    interp_u = np.empty((t,binss.shape[0]))
    interp_v = np.empty((t,binss.shape[0]))
    interp_w = np.empty((t,binss.shape[0]))

    for i in xrange(t):
        print i
        a = linear(el[i,:],uu[i,:],binss)
        b = linear(el[i,:],vv[i,:],binss)
        c = linear(el[i,:],ww[i,:],binss)
        interp_u[i, :] = a
        interp_v[i, :] = b
        interp_w[i, :] = c


    #find the index on the bin level where the water level is.
    b = binss.ravel()
    p = pres.ravel()
    close = find_closest(b,p)-1
    e = el_tot.ravel()
    closefv = find_closest(b,e)-1

    #replace nans above the water line.
    l = len(close)
    for i in xrange(l):
        u[i,close[i]:] = np.nan
        v[i,close[i]:] = np.nan
        w[i,close[i]:] = np.nan

    for i in xrange(t):
        interp_u[i,closefv[i]:] = np.nan
        interp_v[i,closefv[i]:] = np.nan
        interp_w[i,closefv[i]:] = np.nan

    """
    #Merge together the 2d year long probe files.
    index1 = np.array(times1[0,:])
    index2 = np.array(times2[0,:])

    df1 = pd.DataFrame({'ua':uu1,'va':vv1,'el':el1},index=index1)
    df2 = pd.DataFrame({'ua':uu,'va':vv,'el':el2},index=index2)
    print df1
    print df2
    #df1.plot(subplots=True)
    #df2.plot(subplots=True)
    #plt.show()
    comp = df1.combine_first(df2)
    almost_complete = pd.concat([df1,df2],axis=0,join='outer')
    #complete = almost_complete.drop_duplicates(cols=['ua','va','el'],take_last=True)
    #almost_complete = almost_complete.sort()
    comp.plot(subplots=True,rot=20)
    plt.show()
    """

    """
    #organize and build data panel for adcp data
    al_speeds = np.array([u,v,w])
    bins = np.transpose(binss)
    index = np.array(time[0,:])
    columns = ['u','v','w']
    dp = pd.Panel(al_speeds,items=columns,major_axis=index,minor_axis=bins[0,:])
    pd.Panel.save(dp,'/home/aidan/thesis/data_files/flw_stn5_adcp_corrected')
    """
    #organize and data panel for fvcom probe data
    #all_speeds = np.array([interp_u,interp_v,interp_w])
    #items = ['u','v','w']
    #bins = np.transpose(binss)
    #dfp = pd.Panel(all_speeds,items=items, major_axis=onetime,minor_axis=bins[0,:])
    #pd.Panel.save(dfp,'/home/aidan/thesis/data_files/flw_stn4_fvcom_corrected_test')
