from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from struct_pandas import *
from probeMerge import *
from pandas.tools.plotting import *
from mpl_toolkits.mplot3d import Axes3D
import datetime as dt
import matplotlib.dates as dt


def timeslice(panel,start,stop):
    a = panel.major_axis[:]
    minn = a[np.where(a < start)][-1]
    maxx = a[np.where(a < stop)][-1]
    new = panel.loc[['u','v','w'],minn:maxx]
    return new

def findtime(panel1,panel2,time):
    if len(panel1.shape) & len(panel2.shape) == 3:
        a = panel1.major_axis[:]
        b = panel2.major_axis[:]
        minn = a[np.where(a < time)][-1]
        maxx = b[np.where(b < time)][-1]
    else:
        a = panel1.index[:]
        b = panel2.index[:]
        minn = a[np.where(a < time)][-1]
        maxx = b[np.where(b < time)][-1]
    return minn,maxx

def rolling_int(panel1,time1,time2):
    if len(panel1.shape) == 3:
        a = panel1.major_axis[:]
        minn = a[np.where(a < time1)]
        maxx = a[np.where(a < time2)]
        diff = len(maxx)-len(minn)
    else:
        a = panel1.index[:]
        minn = a[np.where(a < time1)]
        maxx = a[np.where(a < time2)]
        diff = len(maxx)-len(minn)
    return diff

def xtime(panel):
    time = panel.major_axis[:].values.tolist()
    l = len(time)
    days = []
    hours = []
    year = []
    month = []
    day = []
    hour = []
    minute = []
    second = []
    for i in xrange(l):
        t = time[i].split(" ")
        days.append(t[0])
        hours.append(t[1])
    for i in xrange(l):
        d = days[i].split("-")
        h = hours[i].split(":")
        year.append(d[0])
        month.append(d[1])
        day.append(d[2])
        hour.append(h[0])
        minute.append(h[1])
        second.append(h[2])
    return year,month,day,hour,minute,second

def depth_avg(panel,plot=False,u=True,v=True,w=False):
    mean = panel.mean(axis=2)
    if plot == True:
        fig,ax = plt.subplots()
        if u==True:
            ax.plot_date(mean.index.to_datetime(),mean['u'],'-',label ='U')
        if v ==True:
            ax.plot_date(mean.index.to_datetime(),mean['v'],'-',label ='V')
        if w ==True:
            ax.plot_date(mean.index.to_datetime(),mean['w'],'-',label ='W')
        ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid()
        ax.xaxis.set_major_locator(dt.MonthLocator())
        ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        plt.legend()
        plt.tight_layout()
        plt.ylabel('Velocity (m/s)')
        plt.title('Depth Averaged Speeds')
        plt.show()
    return mean

def avgDepth_speed(panel1,panel2,sep1,sep2,probet,adcpt):
    a = panel1.minor_axis[:]
    probem = []
    adcpm = []
    for i,j in enumerate(a):
        print j
        height1 = panel1.minor_xs(j)
        height2 = panel2.minor_xs(j)
        mean1 = pd.rolling_mean(height1,sep1)
        mean2 = pd.rolling_mean(height2,sep2)
        mean1t = mean1.apply(mean_vel,axis=1)
        mean2t = mean2.apply(mean_vel,axis=1)
        pmean = mean1t[probet]
        amean = mean2t[adcpt]
        probem.append(pmean)
        adcpm.append(amean)
    fig,ax = plt.subplots()
    ax.plot(probem,a,label='FVCOM')
    ax.plot(adcpm,a,label='ADCP')
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.set_xlabel('Mean Speed (m/s)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Velocity by Depth')
    plt.legend()
    plt.show()

def depth_speed(panel1,panel2,tim,time,plot=False):
    a = panel1.major_xs(tim)
    c = panel2.major_xs(time)
    b = np.sqrt(a['u']**2+a['v']**2+a['w']**2)
    d = np.sqrt(c['u']**2+c['v']**2+c['w']**2)
    mi = panel1.minor_axis[:]
    mino = panel2.minor_axis[:]
    if plot == True:
        fig,axes = plt.subplots()
        plt.plot(b,mi,label='probe')
        plt.plot(d,mino,label='adcp')
        plt.xlabel('Total Velocity (m/s)')
        plt.ylabel('Depth (m)')
        plt.title('Depth vs Speed')
        plt.legend()
        plt.grid()
        plt.show()
    return b,d


def rolling_m(panel1,panel2,sep1,sep2,binn,var,separate=False,hr=False):
    height1 = panel1.minor_xs(binn)
    height2 = panel2.minor_xs(binn)
    mean1 = pd.rolling_mean(height1[var],sep1)
    mean2 = pd.rolling_mean(height2[var],sep2)
    if separate == True:
        fig,ax = plt.subplots(nrows=len(var),ncols=2)
        ax[0].plot_date(mean1.index.to_datetime(),mean1,'-')
        ax[1].plot_date(mean2.index.to_datetime(),mean2,'-')
        ax[0].set_title(str(var)+' Velocity from Probes')
        ax[1].set_title(str(var)+' Velocity from ADCPs')
        ax[0].xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        ax[0].xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax[0].xaxis.grid(True, which="minor")
        ax[0].yaxis.grid()
        ax[0].xaxis.set_major_locator(dt.MonthLocator())
        ax[0].xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        ax[1].xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        ax[1].xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax[1].xaxis.grid(True, which="minor")
        ax[1].yaxis.grid()
        ax[1].xaxis.set_major_locator(dt.MonthLocator())
        ax[1].xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        plt.tight_layout()
        plt.show()
    else:
        fig,ax = plt.subplots()
        ax.plot_date(mean1.index.to_datetime(),mean1,'-',label = 'Probes')
        ax.plot_date(mean2.index.to_datetime(),mean2,'-',label = 'ADCPs',color='red')
        ax.set_title(str(var)+' Velocity Comparison from Probes and ADCPs \n at '+str(binn)+'m from the Ocean Floor')
        if hr == True:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=1))
        else:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid()
        ax.xaxis.set_major_locator(dt.MonthLocator())
        ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        ax.set_ylabel('Velocity (m/s)')
        plt.tight_layout()
        plt.legend()
        plt.show()

def variance(x):
    return np.sqrt((1/3)*(x[0]**2+x[1]**2+x[2]**2))

def mean_vel(x):
    return np.sqrt((x[0]**2+x[1]**2+x[2]**2))

def total_vel(panel1,panel2,sep1,sep2,binn,hr=False):
    height1 = panel1.minor_xs(binn)
    height2 = panel2.minor_xs(binn)
    mean1 = pd.rolling_mean(height1,sep1)
    mean2 = pd.rolling_mean(height2,sep2)
    mean1t = mean1.apply(mean_vel,axis=1)
    mean2t = mean2.apply(mean_vel,axis=1)
    fig,ax = plt.subplots()
    ax.plot_date(mean1t.index.to_datetime(),mean1t,'-',label = 'Probes')
    ax.plot_date(mean2t.index.to_datetime(),mean2t,'-',label = 'ADCPs',color='red')
    ax.set_title(' Velocity Comparison from Probes and ADCPs \n at '+str(binn)+'m from the Ocean Floor')
    if hr == True:
        ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=1))
    else:
        ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
    ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
    ax.xaxis.grid(True, which="minor")
    ax.yaxis.grid()
    ax.xaxis.set_major_locator(dt.MonthLocator())
    ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
    ax.set_ylabel('Velocity (m/s)')
    plt.tight_layout()
    plt.legend()
    plt.show()

def turb_depth(panel1,panel2,sep1,sep2,probet,adcpt):
    a = panel1.minor_axis[:]
    probeturbint = []
    adcpturbint = []
    for i,j in enumerate(a):
        print j
        height1 = panel1.minor_xs(j)
        height2 = panel2.minor_xs(j)
        mean1 = pd.rolling_mean(height1,sep1)
        mean2 = pd.rolling_mean(height2,sep2)
        var1 = pd.rolling_var(height1,sep1)
        var2 = pd.rolling_var(height2,sep2)
        var1t = var1.apply(variance,axis=1)
        var2t = var2.apply(variance,axis=1)
        mean1t = mean1.apply(mean_vel,axis=1)
        mean2t = mean2.apply(mean_vel,axis=1)
        t_int1 = var1t/mean1t
        t_int2 = var2t/mean2t
        ptime = t_int1[probet]
        atime = t_int2[adcpt]
        print ptime
        print atime
        probeturbint.append(ptime)
        adcpturbint.append(atime)
    fig,ax = plt.subplots()
    ax.plot(probeturbint,a,label='FVCOM')
    ax.plot(adcpturbint,a,label='ADCP')
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.set_xlabel('Turbulence Intensity')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Turbulence Intensity by Depth')
    plt.legend()
    plt.show()

def rey_stress(x):
    return 1026*(x[0]*x[1]+x[0]*x[2]+x[1]*x[2])

def reynold_stress(panel1,panel2,sep1,sep2,binn,hr=False):
    height1 = panel1.minor_xs(binn)
    height2 = panel2.minor_xs(binn)
    mean1 = pd.rolling_mean(height1,sep1)
    mean2 = pd.rolling_mean(height2,sep2)
    rstress1 = mean1.apply(rey_stress,axis=1)
    rstress2 = mean2.apply(rey_stress,axis=1)
    fig,ax = plt.subplots()
    ax.plot_date(rstress1.index.to_datetime(),rstress1,'-',label = 'Probes')
    ax.plot_date(rstress2.index.to_datetime(),rstress2,'-',label = 'ADCPs',color='red')
    ax.set_title('Reynolds Stress Comparison between Probes and ADCPs \n at '+str(binn)+'m from the Ocean Floor')
    if hr == True:
        ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=1))
    else:
        ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
    ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
    ax.xaxis.grid(True, which="minor")
    ax.yaxis.grid()
    ax.xaxis.set_major_locator(dt.MonthLocator())
    ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
    ax.set_ylabel('Reynolds Stress')
    plt.tight_layout()
    plt.legend()
    plt.show()

def reynolds_depth(panel1,panel2,sep1,sep2,probet,adcpt):
    a = panel1.minor_axis[:]
    probereystr = []
    adcpreystr = []
    for i,j in enumerate(a):
        print j
        height1 = panel1.minor_xs(j)
        height2 = panel2.minor_xs(j)
        mean1 = pd.rolling_mean(height1,sep1)
        mean2 = pd.rolling_mean(height2,sep2)
        rstress1 = mean1.apply(rey_stress,axis=1)
        rstress2 = mean2.apply(rey_stress,axis=1)
        pR = rstress1[probet]
        aR = rstress2[adcpt]
        print pR
        print aR
        probereystr.append(pR)
        adcpreystr.append(aR)
    fig,ax = plt.subplots()
    ax.plot(probereystr,a,label='FVCOM')
    ax.plot(adcpreystr,a,label='ADCP')
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.set_xlabel('Reynolds Stress')
    ax.set_ylabel('Depth (m)')
    ax.set_title('Reynolds Stress by Depth')
    plt.legend()
    plt.show()


def turbulence_int(panel1,panel2,sep1,sep2,binn,both=False,hr=False):
    height1 = panel1.minor_xs(binn)
    height2 = panel2.minor_xs(binn)
    mean1 = pd.rolling_mean(height1,sep1)
    mean2 = pd.rolling_mean(height2,sep2)
    var1 = pd.rolling_var(height1,sep1)
    var2 = pd.rolling_var(height2,sep2)
    var1t = var1.apply(variance,axis=1)
    var2t = var2.apply(variance,axis=1)
    mean1t = mean1.apply(mean_vel,axis=1)
    mean2t = mean2.apply(mean_vel,axis=1)
    t_int1 = var1t/mean1t
    t_int2 = var2t/mean2t

    if both == True:
        fig,ax = plt.subplots()
        ax1 = ax.twinx()
        ax.plot_date(t_int2.index.to_datetime(),t_int2,'-',label = 'ADCPs I',color='red')
        ax.plot_date(t_int1.index.to_datetime(),t_int1,'-',label = 'Probes I')
        ax1.plot_date(mean1t.index.to_datetime(),mean1t,'--',label = 'Probes Speed')
        ax1.plot_date(t_int2.index.to_datetime(),mean2t,'--',label = 'ADCPs Speed')
        ax.set_title('Turbulence Intensity')
        if hr == True:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        else:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=1))
        ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid()
        ax.xaxis.set_major_locator(dt.MonthLocator())
        ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        plt.tight_layout()
        ax.set_ylabel('Turbulence Intensity')
        ax1.set_ylabel('Velocity (m/s)')
        plt.legend()
        plt.show()

    else:
        fig,ax = plt.subplots()
        ax1 = ax.twinx()
        ax.plot_date(t_int1.index.to_datetime(),t_int1,'-',color='red',label = 'Probes I')
        ax1.plot_date(mean1t.index.to_datetime(),mean1t,'--',label = 'Probes Speed')
        ax.set_title('Turbulence Intensity \n Calculated from FVCOM Data')
        if hr == True:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        else:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=1))
        ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid()
        ax.xaxis.set_major_locator(dt.MonthLocator())
        ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        plt.tight_layout()
        ax.set_ylabel('Turbulence Intensity')
        ax1.set_ylabel('Velocity (m/s)')
        plt.legend()
        plt.show()

        fig,ax = plt.subplots()
        ax1 = ax.twinx()
        ax.plot_date(t_int2.index.to_datetime(),t_int2,'-',color='red',label = 'ADCP I')
        ax1.plot_date(mean2t.index.to_datetime(),mean2t,'--',label = 'ADCP Speed')
        ax.set_title('Turbulence Intensity \n Calculated for Measured Data')
        if hr == True:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=6))
        else:
            ax.xaxis.set_minor_locator(dt.HourLocator(byhour=range(24), interval=1))
        ax.xaxis.set_minor_formatter(dt.DateFormatter('%H:%M\n%a'))
        ax.xaxis.grid(True, which="minor")
        ax.yaxis.grid()
        ax.xaxis.set_major_locator(dt.MonthLocator())
        ax.xaxis.set_major_formatter(dt.DateFormatter('\n\n\n%b\n%Y'))
        plt.tight_layout()
        ax.set_ylabel('Turbulence Intensity')
        ax1.set_ylabel('Velocity (m/s)')
        plt.legend()
        plt.show()


def distro(panel,binn,var,timestart,timestop,dep_avg=False):
    if dep_avg == True:
        l = len(var)
        time = timeslice(panel,timestart,timestop)
        mean = time.mean(axis=2)
        sub = mean.mean(axis=0)
        cor = mean.sub(sub)
        for i in xrange(l):
            cor[var[i]].plot(kind='kde',label=var[i])
        plt.title('Depth Averaged Velocity Distributions')
        plt.legend()
        plt.show()
    else:
        l = len(var)
        time = timeslice(panel,timestart,timestop)
        mean = time.minor_xs(binn)
        sub = mean.mean(axis=0)
        cor = mean.sub(sub)
        for i in xrange(l):
            cor[var[i]].plot(kind='kde',label=var[i])
        plt.title('Velocity Distributions '+str(binn)+'m for Ocean Floor')
        plt.legend()
        plt.show()

def time_match(panel1,panel2,binn):
    pan1 = panel1.minor_xs(binn)
    pan2 = panel2.minor_xs(binn)
    test = pan2.rename(columns={'u' : 'uu', 'v' : 'vv', 'w' : 'ww'})
    a=pd.concat([pan1,test],axis=1,join='inner')
    return a

def roll_corr(con_pan, var1, var2,window,plot=False):
    if plot == True:
        a = lag_plot(con_pan[var1])
        plt.show()
        autocorrelation_plot(con_pan[var1])
        plt.show()
    else:
        a =  pd.rolling_corr(con_pan[var1],con_pan[var2],window=window)
    return a

def scat(panel1,panel2,binn,var1,var2,var3,dim=False):
    if dim == True:
        pan1 = panel1.minor_xs(binn)
        pan2 = panel2.minor_xs(binn)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(pan1[var1],pan1[var2],pan1[var3],cmap='jet',label='ADCP')
        ax.scatter(pan2[var1],pan2[var2],pan2[var3],cmap='jet',label='Probe')
        ax.set_xlabel('U Velocity')
        ax.set_ylabel('V Velocity')
        ax.set_zlabel('W Velocity')
        plt.title('Velocity Scatter Plot')
        plt.grid()
        plt.show()
    else:
        pan1 = panel1.minor_xs(binn)
        pan2 = panel2.minor_xs(binn)
        plt.figure()
        pan1.plot(x=var1,y=var2,style='o',label='ADCP',grid=True)
        pan2.plot(x=var1,y=var2,style='o',label='Probe',grid=True)
        plt.legend()
        plt.xlabel(str(var1)+' (m/s)')
        plt.ylabel(str(var2)+' (m/s)')
        plt.title('Northern and Eastern Velocity Scatter Plot')
        plt.show()


if __name__ == "__main__":

    savedir_adcp = '/home/aidan/thesis/data_files/flw_stn4_adcp_corrected'
    savedir_probe = '/home/aidan/thesis/data_files/flw_stn4_fvcom_corrected_test'

    #Load the pandas panels
    adcp = pd.Panel.load(savedir_adcp)
    probe = pd.Panel.load(savedir_probe)

    #choose start time and end time to slice both panels
    timestart = '2012-07-27 08:00:00'
    timestop = '2012-07-27 23:00:00'

    #This selects the amount of time to average over. The times must be between
    #timestart and timestop
    average = ['2012-07-27 08:10:00','2012-07-27 08:20:00']

    #slice the adcp and probe data
    probe = timeslice(probe,timestart,timestop)
    adcp = timeslice(adcp,timestart,timestop)

    #findtime takes time inputs and finds the closest match in the panels that
    #is less than each average value
    ad,fv = findtime(adcp,probe,average[0])
    adc,fvc = findtime(adcp,probe,average[1])

    #rolling_int returns the number of timesteps in a given average range
    agap = rolling_int(adcp,ad,adc)
    pgap = rolling_int(probe,fv,fvc)

    #choose a bin to analyze, necessary for any timestep plots.
    #use this to find bin values,
    #print probe.minor_axis[:]
    desiredBin = 10.11

    #choose a time needed for depth profiles
    desiredTime = '2012-07-27 18:00:00'

    #Here we find a time is desired bin dataset
    a =  probe.minor_xs(desiredBin)
    b =  adcp.minor_xs(desiredBin)
    probeTime,adcpTime = findtime(a,b,desiredTime)

    #These are the plot calls

    #depth_speed(adcp,probe,adcpTime,probeTime,plot=True)
    #depth_avg(probe,plot=True,u=True,v=True,w=True)
    #rolling_m(probe,adcp,pgap,agap,10.11,'u')
    #rolling_m(probe,adcp,pgap,agap,10.11,'v')
    #rolling_m(probe,adcp,pgap,agap,10.11,'w')
    #rolling_m(probe,adcp,pgap,agap,4.11,'v',hr=True)

    #distro(adcp,probe1,['u','v'],timestart,timestop,dep_avg=True)
    #scat(adcp,probe,10.11,'u','v','w')#,dim=True)
    #scat(adcp,probe,10.11,'u','v','w',dim=True)
    #total_vel(probe,adcp,pgap,agap,10.11,hr=False)
    turbulence_int(probe,adcp,pgap,agap,10.11,both=True)
    #turb_depth(probe,adcp,pgap,agap,probeTime,adcpTime)
    #reynold_stress(probe,adcp,pgap,agap,10.11,hr=True)
    #reynolds_depth(probe,adcp,pgap,agap,probeTime,adcpTime)
    avgDepth_speed(probe,adcp,pgap,agap,probeTime,adcpTime)

    #Time match links adcp and probe data together and keeps only equal time
    #steps

    connect = time_match(probe,adcp,desiredBin)
    c1,_ = findtime(connect,connect,average[0])
    c2,_ = findtime(connect,connect,average[1])
    cgap = rolling_int(connect,c1,c2)
    #roll_corr(connect,'w','uu',cgap,plot=True)
    #roll_corr(connect,'ww','uu',cgap,plot=True)
