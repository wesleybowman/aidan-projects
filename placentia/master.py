''' master file '''

''' imports needed for doing bash commands in python '''
import os
import shutil

''' imports needed for getRestartTime '''
from scipy.io import netcdf
import glob

''' imports needed for email '''
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def copySingleFile(sourcefile,destination):

    shutil.copy(sourcefile,destination)

def copyDirectory(sourcefile,destination):

    shutil.copytree(sourcefile,destination)

def makeDirectory(directoryName):

    os.mkdir(directoryName)

def move(sourcefile,destination):

    shutil.move(sourcefile,destination)

def removeSingleFile(sourcefile):

    os.remove(sourcefile)

def removeDirectory(sourcefile):

    shutil.rmtree(sourcefile)

def mail(gmail_user,gmail_pwd,to, subject='ACE-net job status', text='Run has started'):
    ''' Sends an email from a gmail account to a user with a subject and a
        message '''

    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()

def readInFiles():
    ''' Read in the email and password. A userInfo.txt file is needed in the
        same directory. userInfo.txt has the users email and password in it. '''

    with open("userInfo.txt",'r') as f:
        user=f.readline()
        passwd=f.readline()
        user = user.rstrip('\n')
        passwd = passwd.rstrip('\n')

    return user,passwd


def getRestartTime():

    datadir = '/home/daugue6/capeislerestart/output/'

    #get the correct restart file, the second newest one (if there is more than one)
    files = glob.glob(datadir + "*.nc")

    #find the restart files
    restart_files = []

    for i in files:
        if "restart" in i:
            restart_files.append(i)

    #get the latest restart file

    filenums = []
    for i in restart_files:
        filenums.append(int(i[-7:-3]))

    latest = filenums.index(max(filenums))

    #we need the times data from the restart file
    ncid = netcdf.netcdf_file(files[latest],'r')
    Times = ncid.variables['Times'].data

    ind = Times.shape[0] - 1

    #join the elements of the list into a single string

    time = "\'"
    for i in Times[ind,:]:
        if i == 'T':
            time += ' '
        else:
            time += i
    time += "\'"

    name="\'{}\'".format(files[latest])

    return time, name

def buildRestart():

    oldRunFile = 'capeisle_run.nml'

    start, restartDir = getRestartTime()

    restart = restartDir.split('/')[-1]
    restart = "\'{}" .format(restart)

    outputFile = oldRunFile

    moveOldTo = './runfiles/'
    renameOld='capeisle_run{}.nml'.format(start)
    oldOutputRunFile = 'run_output{}'.format(start)


    try:
        makeDirectory(moveOldTo)

    except OSError:
        pass

    move(oldRunFile, renameOld)
    move(renameOld, moveOldTo)
    move(oldOutputRunFile, moveOldTo)


    top = '''
    !================================================================!
    _______  _     _  _______  _______  _______  ______     _____
    (_______)(_)   (_)(_______)(_______)(_______)(_____ \   (_____)
    _____    _     _  _        _     _  _  _  _  _____) )  _  __ _
    |  ___)  | |   | || |      | |   | || ||_|| |(_____ (  | |/ /| |
    | |       \ \ / / | |_____ | |___| || |   | | _____) )_|   /_| |
    |_|        \___/   \______) \_____/ |_|   |_|(______/(_)\_____/
    -- Beta Release
    !                                                                !
    !========DOMAIN DECOMPOSITION USING: METIS 4.0.1 ================!
    !======Copyright 1998, Regents of University of Minnesota========!
    !                                                                !
    '''

    change = '''

    &NML_CASE
    CASE_TITLE      = 'Cape Isle Site'
    TIMEZONE        = 'UTC',
    DATE_FORMAT     = 'YMD'
    START_DATE      = {0}
    END_DATE        = '2011-10-16 00:00:00'
    /

    &NML_STARTUP
    STARTUP_TYPE      = 'hotstart'
    STARTUP_FILE      = {1}
    STARTUP_UV_TYPE   = 'set values'
    STARTUP_TURB_TYPE = 'set values'
    STARTUP_TS_TYPE   = 'constant'
    STARTUP_T_VALS    = 18
    STARTUP_S_VALS    = 35.0
    STARTUP_DMAX      =  -10.0
    /

    &NML_IO
    INPUT_DIR       =  './input/'
    OUTPUT_DIR      =  './ouput/'
    IREPORT         =  720,
    VISIT_ALL_VARS  = F,
    WAIT_FOR_VISIT  = F,
    USE_MPI_IO_MODE = F
    /

    &NML_INTEGRATION
    EXTSTEP_SECONDS =  0.5,
    ISPLIT          =  1
    IRAMP           =  34560
    MIN_DEPTH       =  0.5
    STATIC_SSH_ADJ  =  0.0
    /

    &NML_RESTART
    RST_ON  = T,
    RST_FIRST_OUT      = {0}
    RST_OUT_INTERVAL   = 'days = 1.0'
    RST_OUTPUT_STACK   =           1
    /

    &NML_NETCDF
    NC_ON   = T,
    NC_FIRST_OUT    = {0}
    NC_OUT_INTERVAL =  'seconds=600.0',
    NC_OUTPUT_STACK =  0,
    NC_GRID_METRICS = T,
    NC_VELOCITY     = F,
    NC_SALT_TEMP    = F,
    NC_TURBULENCE   = F,
    NC_AVERAGE_VEL  = T,
    NC_VERTICAL_VEL = F,
    NC_WIND_VEL     = F,
    NC_WIND_STRESS  = F,
    NC_EVAP_PRECIP  = F,
    NC_SURFACE_HEAT = F,
    NC_GROUNDWATER = F
    /
    '''.format(start, restart)

    rest = '''
    &NML_NETCDF_AV
    NCAV_ON = F,
    NCAV_FIRST_OUT  = 'none'
    NCAV_OUT_INTERVAL       =  0.0,
    NCAV_OUTPUT_STACK       =           0,
    NCAV_GRID_METRICS       = F,
    NCAV_FILE_DATE  = F,
    NCAV_VELOCITY   = F,
    NCAV_SALT_TEMP  = F,
    NCAV_TURBULENCE = F,
    NCAV_AVERAGE_VEL        = F,
    NCAV_VERTICAL_VEL       = F,
    NCAV_WIND_VEL   = F,
    NCAV_WIND_STRESS        = F,
    NCAV_EVAP_PRECIP        = F,
    NCAV_SURFACE_HEAT       = F,
    NCAV_GROUNDWATER        = F,
    NCAV_BIO        = F,
    NCAV_WQM        = F,
    NCAV_VORTICITY  = F
    /

    &NML_SURFACE_FORCING
    WIND_ON = F,
    HEATING_ON      = F,
    PRECIPITATION_ON        = F,
    /

    &NML_PHYSICS
    HORIZONTAL_MIXING_TYPE          = 'closure'
    HORIZONTAL_MIXING_KIND          = 'constant'
    HORIZONTAL_MIXING_COEFFICIENT   = 0.3
    HORIZONTAL_PRANDTL_NUMBER       = 1.0
    VERTICAL_MIXING_TYPE            = 'closure'
    VERTICAL_MIXING_COEFFICIENT     = 1.0E-3,
    VERTICAL_PRANDTL_NUMBER         = 1.0
    BOTTOM_ROUGHNESS_MINIMUM        =  0.0025
    BOTTOM_ROUGHNESS_LENGTHSCALE    =  0.001
    BOTTOM_ROUGHNESS_KIND           = 'constant'
    BOTTOM_ROUGHNESS_TYPE           = 'orig'
    CONVECTIVE_OVERTURNING          = F,
    SCALAR_POSITIVITY_CONTROL       = T,
    BAROTROPIC                      = T,
    BAROCLINIC_PRESSURE_GRADIENT    = 'sigma levels'
    SEA_WATER_DENSITY_FUNCTION      = 'dens2'
    RECALCULATE_RHO_MEAN           = F
    INTERVAL_RHO_MEAN              = 'seconds=1800.'
    TEMPERATURE_ACTIVE              = F,
    SALINITY_ACTIVE                 = F,
    SURFACE_WAVE_MIXING             = F,
    WETTING_DRYING_ON               = T
    /

    &NML_RIVER_TYPE
    RIVER_NUMBER    =           0,
    /

    &NML_OPEN_BOUNDARY_CONTROL
    OBC_ON                      = T,
    OBC_NODE_LIST_FILE          = 'capeisle_obc.dat'
    OBC_ELEVATION_FORCING_ON    = T,
    OBC_ELEVATION_FILE          = 'capeisle_el_obc.nc'
    OBC_TS_TYPE                 = 3
    OBC_TEMP_NUDGING            = F,
    OBC_TEMP_FILE               = 'none'
    OBC_TEMP_NUDGING_TIMESCALE  =  0.0000000E+00,
    OBC_SALT_NUDGING            = F,
    OBC_SALT_FILE               = 'none'
    OBC_SALT_NUDGING_TIMESCALE  =  0.0000000E+00,
    OBC_MEANFLOW                = F,
    /

    &NML_GRID_COORDINATES
    GRID_FILE       = 'capeisle_grd.dat'
    GRID_FILE_UNITS = 'meters'
    PROJECTION_REFERENCE  = 'proj=lcc +lon_0=-6.461692e+01 +lat_0=4.545973e+01 +lat_1=4.514367e+01 +lat_2=4.577579e+01'
    SIGMA_LEVELS_FILE     = 'sigma.dat'
    DEPTH_FILE      = 'capeisle_dep.dat'
    CORIOLIS_FILE   = 'capeisle_cor.dat'
    SPONGE_FILE     = 'capeisle_spg.dat'
    BFRIC_FILE='capeisle_bfric.dat'
    VVCOE_FILE='capeisle_vvcoe.dat'
    /

    &NML_GROUNDWATER
    GROUNDWATER_ON             = F,
    GROUNDWATER_FLOW  = 0.0,
    GROUNDWATER_FILE           = 'none'
    /

    &NML_LAG
    LAG_PARTICLES_ON        = F,
    LAG_START_FILE   = 'none'
    LAG_OUT_FILE     = 'none'
    LAG_RESTART_FILE = 'none'
    LAG_OUT_INTERVAL =  0.000000000000000E+000,
    LAG_SCAL_CHOICE  = 'none'
    /

    &NML_ADDITIONAL_MODELS
    DATA_ASSIMILATION       = F,
    BIOLOGICAL_MODEL        = F,
    SEDIMENT_MODEL  = F,
    SEDIMENT_PARAMETER_TYPE = 'constant'
    SEDIMENT_MODEL_FILE     = 'generic_sediment.inp'
    ICING_MODEL     = F,
    ICE_MODEL       = F,
    /

    &NML_PROBES
    PROBES_ON = T,
    PROBES_NUMBER = 64,
    PROBES_FILE = 'capeisle_timeseries01.nml',
    /

    &NML_TURBINE
    TURBINE_ON = F,
    TURBINE_FILE = 'capeisle_turbines.dat'
    /

    &NML_NESTING
    NESTING_ON = F
    /

    &NML_NCNEST
    NCNEST_ON = F
    /

    &NML_BOUNDSCHK
    BOUNDSCHK_ON  = F
    /

    &NML_STATION_TIMESERIES
    OUT_STATION_TIMESERIES_ON       = F,
    STATION_FILE='NONE'
    LOCATION_TYPE='NONE'
    OUT_ELEVATION=F,
    OUT_VELOCITY_3D=F,
    OUT_VELOCITY_2D=F,
    OUT_SALT_TEMP =F,
    OUT_WIND_VELOCITY=F,
    OUT_INTERVAL= 'seconds=1000.0'
    /
    '''

    top=top.split('\n')
    change=change.split('\n')
    rest=rest.split('\n')

    with open(outputFile, 'w') as f:
        for t in top:
            print >> f, t

        for c in change:
            print >> f, c

        for r in rest:
            print >> f, r


