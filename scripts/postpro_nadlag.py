#!/usr/bin/env python

__author__ = "Maxime Beauchamp"
__version__ = "0.1"
__date__ = "2021-02-10"
__email__ = "maxime.beauchamp@imt-atantique.fr"

from Metrics_NATL60 import *

def mk_dir_recursive(dir_path):
    if os.path.isdir(dir_path):
        return
    h, t = os.path.split(dir_path)  # head/tail
    if not os.path.isdir(h):
        mk_dir_recursive(h)

    new_path = join_paths(h, t)
    if not os.path.isdir(new_path):
        os.mkdir(new_path)

type_obs   = sys.argv[1]
domain     = sys.argv[2] 

workpath = scratchpath+"/"+domain+"/OSSE/scores_allmethods_nadlag_"+type_obs
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
OBS_nadirswot_file          = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_NADIRSWOT.nc"
AnDA_nadir_file_0           = scratchpath+'/resAnDA_nadir_nadlag_0_'+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
AnDA_nadir_file_5           = scratchpath+'/resAnDA_nadir_nadlag_5_'+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
AnDA_nadirswot_file_0       = scratchpath+'/resAnDA_nadirswot_nadlag_0_'+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
AnDA_nadirswot_file_5       = scratchpath+'/resAnDA_nadirswot_nadlag_5_'+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
FP_GENN_nadir_file_0        = scratchpath+'/resIA_nadir_nadlag_0_'+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadir_file_5        = scratchpath+'/resIA_nadir_nadlag_5_'+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswor_file_0    = scratchpath+'/resIA_nadirswot_nadlag_0_'+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswot_file_5    = scratchpath+'/resIA_nadirswot_nadlag_5_'+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'

# Reload results
lday                = xr.open_dataset(GT_file,decode_times=False).Time.values
GT                  = xr.open_dataset(GT_file,decode_times=False).ssh.values
OBS_nadir           = xr.open_dataset(OBS_nadir_file,decode_times=False).ssh.values
OBS_nadirswot       = xr.open_dataset(OBS_nadirswot_file,decode_times=False).ssh.values
AnDA_nadir_0        = xr.open_dataset(AnDA_nadir_file_0,decode_times=False).ssh.values
AnDA_nadir_5        = xr.open_dataset(AnDA_nadir_file_5,decode_times=False).ssh.values
AnDA_nadirswot_0    = xr.open_dataset(AnDA_nadirswot_file_0,decode_times=False).ssh.values
AnDA_nadirswot_5    = xr.open_dataset(AnDA_nadirswot_file_5,decode_times=False).ssh.values
FP_GENN_nadir_0     = xr.open_dataset(FP_GENN_nadir_file_0,decode_times=False).ssh.values
FP_GENN_nadir_5     = xr.open_dataset(FP_GENN_nadir_file_5,decode_times=False).ssh.values
FP_GENN_nadirswot_0 = xr.open_dataset(FP_GENN_nadirswot_file_0,decode_times=False).ssh.values
FP_GENN_nadirswot_5 = xr.open_dataset(FP_GENN_nadirswot_file_5,decode_times=False).ssh.values

if domain=="OSMOSIS":
    ymax = 0.3
else:
    ymax = 0.2

# list_data (AnDA nadir)
list_data   = [GT, OBS_nadir, AnDA_nadir_0, AnDA_nadir_5]
# arguments for plots (nadir)
labels_data = np.array(['GT','Obs (nadir)','Post-AnDA (lag=0)','Post-AnDA (lag=5)'])
colors      = np.array(['k','','red','blue'])
symbols     = np.array(['k','','o','o'])
lstyle      = np.array(['solid','','solid','solid'])
lwidth      = np.array([2,2,1,1])
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
## nRMSE time series
resfile=workpath+"/TS_AnDA_nadir_nadlag.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)

# list_data (AnDA nadirswot)
list_data   = [GT, OBS_nadirswot, AnDA_nadirswot_0, AnDA_nadirswot_5]
# arguments for plots (nadirswot)
labels_data = np.array(['GT','Obs (nadir+swot)','Post-AnDA (lag=0)','Post-AnDA (lag=5)'])
colors      = np.array(['k','','red','blue'])
symbols     = np.array(['k','','o','o'])
lstyle      = np.array(['solid','','solid','solid'])
lwidth      = np.array([2,2,1,1])
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
## nRMSE time series
resfile=workpath+"/TS_AnDA_nadirswot_nadlag.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)

# list_data (GENN nadir)
list_data   = [GT, OBS_nadir, FP_GENN_nadir_0, FP_GENN_nadir_5]
# arguments for plots (nadir)
labels_data = np.array(['GT','Obs (nadir)','FP-GENN (lag=0)','FP-GENN (lag=5)'])
colors      = np.array(['k','','red','blue'])
symbols     = np.array(['k','','o','o'])
lstyle      = np.array(['solid','','solid','solid'])
lwidth      = np.array([2,2,1,1])
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
## nRMSE time series
resfile=workpath+"/TS_GENN_nadir_nadlag.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)

# list_data (GENN nadirswot)
list_data   = [GT, OBS_nadirswot, FP_GENN_nadirswot_0, FP_GENN_nadirswot_5]
# arguments for plots (nadirswot)
labels_data = np.array(['GT','Obs (nadir+swot)','FP-GENN (lag=0)','FP-GENN (lag=5)'])
colors      = np.array(['k','','red','blue'])
symbols     = np.array(['k','','o','o'])
lstyle      = np.array(['solid','','solid','solid'])
lwidth      = np.array([2,2,1,1])
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
## nRMSE time series
resfile=workpath+"/TS_GENN_nadirswot_nadlag.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)

