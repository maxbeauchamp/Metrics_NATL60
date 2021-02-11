#!/usr/bin/env python


__author__ = "Maxime Beauchamp"
__version__ = "0.1"
__date__ = "2021-02-10"
__email__ = "maxime.beauchamp@imt-atantique.fr"

from Metrics_NATL60 import *

# function to create recursive paths
def mk_dir_recursive(dir_path):
    if os.path.isdir(dir_path):
        return
    h, t = os.path.split(dir_path)  # head/tail
    if not os.path.isdir(h):
        mk_dir_recursive(h)

    new_path = join_paths(h, t)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)

AnDA_lag   = sys.argv[1]
NN_lag     = sys.argv[2]
type_obs   = sys.argv[3]
domain     = sys.argv[4] 

workpath = scratchpath+"/"+domain+"/OSSE/scores_AnDAnadlag_"+AnDA_lag+"_NNnadlag_"+NN_lag+"_"+type_obs
scratchpath = scratchpath+"/"+domain+"/OSSE"
if not os.path.exists(workpath):
    mk_dir_recursive(workpath)
#else:
#    shutil.rmtree(workpath)
#    mk_dir_recursive(workpath)    

## parameters
if domain=="OSMOSIS":
    extent     = [-19.5,-11.5,45.,55.]
    indLat     = 200
    indLon     = 160
elif domain=='GULFSTREAM':
    extent     = [-65.,-55.,33.,43.]
    indLat     = 200
    indLon     = 200
else:
    extent=[-65.,-55.,30.,40.]
    indLat     = 200
    indLon     = 200

## store all data in a list
GT_file                     = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_GT.nc"
OBS_nadir_file              = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_NADIR.nc"
OI_nadir_file               = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OI_NADIR.nc"
AnDA_nadir_file             = scratchpath+'/resAnDA_nadir_nadlag_'+AnDA_lag+"_"+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
DINEOF_nadir_file           = scratchpath+'/resAnDA_nadir_nadlag_'+AnDA_lag+"_"+type_obs+'/NATL60_'+domain+'_XP1_DINEOF.nc'
FP_GENN_nadir_file          = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
OBS_nadirswot_file              = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_nadirswot.nc"
OI_nadirswot_file               = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OI_nadirswot.nc"
AnDA_nadirswot_file             = scratchpath+'/resAnDA_nadirswot_nadlag_'+AnDA_lag+"_"+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
DINEOF_nadirswot_file           = scratchpath+'/resAnDA_nadirswot_nadlag_'+AnDA_lag+"_"+type_obs+'/NATL60_'+domain+'_XP1_DINEOF.nc'
FP_GENN_nadirswot_file          = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'

# Reload results
lday    = xr.open_dataset(GT_file,decode_times=False).Time.values
GT      = xr.open_dataset(GT_file,decode_times=False).ssh.values
OBS_nadir     = xr.open_dataset(OBS_nadir_file,decode_times=False).ssh.values
OI_nadir      = xr.open_dataset(OI_nadir_file,decode_times=False).ssh.values
AnDA_nadir    = xr.open_dataset(AnDA_nadir_file,decode_times=False).ssh.values
DINEOF_nadir  = xr.open_dataset(DINEOF_nadir_file,decode_times=False).ssh.values
FP_GENN_nadir = xr.open_dataset(FP_GENN_nadir_file,decode_times=False).ssh.values
OBS_nadirswot     = xr.open_dataset(OBS_nadirswot_file,decode_times=False).ssh.values
OI_nadirswot      = xr.open_dataset(OI_nadirswot_file,decode_times=False).ssh.values
AnDA_nadirswot    = xr.open_dataset(AnDA_nadirswot_file,decode_times=False).ssh.values
DINEOF_nadirswot  = xr.open_dataset(DINEOF_nadirswot_file,decode_times=False).ssh.values
FP_GENN_nadirswot = xr.open_dataset(FP_GENN_nadirswot_file,decode_times=False).ssh.values

# list_data (nadir+swot)
list_data   = [GT, OBS_nadir, OI_nadir, AnDA_nadir, DINEOF_nadir, FP_GENN_nadir,
               OBS_nadirswot, OI_nadirswot, AnDA_nadirswot, DINEOF_nadirswot, FP_GENN_nadirswot]

# arguments for plots (nadir+swot)
labels_data = np.array(['GT','Obs (nadir)','OI (nadir)','Post-AnDA (nadir)','VE-DINEOF (nadir)','FP-GENN (nadir)','Obs (nadir+swot)','OI (nadir+swot)','Post-AnDA (nadir+swot)','VE-DINEOF (nadir+swot)','FP-GENN (nadir+swot)'])
colors      = np.array(['k','','red','seagreen','steelblue','darkorange','','red','seagreen','steelblue','darkorange'])
symbols     = np.array(['k','','p','p','p','p','p','','o','o','o','o','o'])
lstyle      = np.array(['solid','','dashed','dashed','dashed','dashed','dashed','','solid','solid','solid','solid','solid'])
lwidth      = np.array([2,2,2,1,1,1,1,2,2,1,1,1,1])

# compare shapes and do appropriate downscaling with minimal resolution
min_res=1e9
for i in range(len(list_data)):
    min_res=min(min_res,list_data[i].shape[1])
for i in range(len(list_data)):
    if list_data[i].shape[1]>min_res:
        dwscale      = int(list_data[i].shape[1]/min_res)
        list_data[i] = einops.reduce(list_data[i], '(t t1) (h h1) (w w1) -> t h w', t1=1, h1=dwscale, w1=dwscale, reduction=np.nanmean)
    print(list_data[i].shape)
dwscale = int(200/min_res)
indLon  = int(indLon/dwscale)
indLat  = int(indLat/dwscale)
lon = np.arange(extent[0],extent[1],1/(20/dwscale))
lat = np.arange(extent[2],extent[3],1/(20/dwscale))

## list of dates
lday1 = [ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=60+i),"%Y-%m-%d") for i in range(20) ]
lday2 = [ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=140+i),"%Y-%m-%d") for i in range(20) ]
lday3 = [ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=220+i),"%Y-%m-%d") for i in range(20) ]
lday4 = [ datetime.strftime(datetime.strptime("2012-10-01",'%Y-%m-%d')\
                          + timedelta(days=300+i),"%Y-%m-%d") for i in range(20) ]
lday  = np.concatenate([lday1,lday2,lday3,lday4])
lday2 = [ datetime.strptime(lday[i],'%Y-%m-%d') for i in range(len(lday)) ] 

## Export methods to NetCDF
ncdf_file=workpath+"/NetCDF_nadir_nadirswot.nc"
#export_NetCDF(list_data,labels_data,lday,lon,lat,ncdf_file)
## nRMSE time series
if domain=="OSMOSIS":
    ymax = 0.3
else:
    ymax = 0.2
resfile=workpath+"/TS_nRMSE_nadir_nadirswot.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)
resfile=workpath+"/TS_nRMSE_Grad_nadir_nadirswot.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=True)
## average SNR
resfile=workpath+"/SNR_nadir_nadirswot.png"
resssh=4*dwscale
#plot_SNR(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,resssh,resfile)
## average Taylor diagrams
resfile=workpath+"/Taylor_diagram_nadir_nadirswot.png"
#Taylor_diagram(list_data,labels_data,colors,symbols,resfile)

