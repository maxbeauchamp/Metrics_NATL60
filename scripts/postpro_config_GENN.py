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

NN_lag     = sys.argv[1]
type_obs   = sys.argv[2]
domain     = sys.argv[3] 

workpath = scratchpath+"/"+domain+"/OSSE/scores_GENN_NNnadlag_"+NN_lag+"_"+type_obs
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
# nadir
OBS_nadir_file              = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_NADIR.nc"
FP_GENN_nadir_file_sup1        = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_womissing_wocov/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadir_file_sup2        = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wmissing_wocov/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadir_file_unsup       = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wwmissing_wocov/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadir_file_sup1_wOI    = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_womissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadir_file_sup2_wOI    = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadir_file_unsup_wOI   = scratchpath+'/resIA_nadir_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wwmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
# nadir+SWOT
OBS_nadirswot_file              = basepath+"/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_NADIRSWOT.nc"
FP_GENN_nadirswot_file_sup1        = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_womissing_wocov/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswot_file_sup2        = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wmissing_wocov/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswot_file_unsup       = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wwmissing_wocov/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswot_file_sup1_wOI    = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_womissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswot_file_sup2_wOI    = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'
FP_GENN_nadirswot_file_unsup_wOI   = scratchpath+'/resIA_nadirswot_nadlag_'+NN_lag+"_"+type_obs+'/FP_GENN_wwmissing_wOI/NATL60_'+domain+'_XP1_GENN002.nc'

# Reload results
lday    = xr.open_dataset(GT_file,decode_times=False).Time.values
GT      = xr.open_dataset(GT_file,decode_times=False).ssh.values
OBS_nadir     = xr.open_dataset(OBS_nadir_file,decode_times=False).ssh.values
OBS_nadirswot     = xr.open_dataset(OBS_nadirswot_file,decode_times=False).ssh.values
FP_GENN_nadir_sup1 = xr.open_dataset(FP_GENN_nadir_file_sup1,decode_times=False).ssh.values
FP_GENN_nadir_sup2 = xr.open_dataset(FP_GENN_nadir_file_sup2,decode_times=False).ssh.values
FP_GENN_nadir_unsup = xr.open_dataset(FP_GENN_nadir_file_unsup,decode_times=False).ssh.values
FP_GENN_nadir_sup1_wOI = xr.open_dataset(FP_GENN_nadir_file_sup1_wOI,decode_times=False).ssh.values
FP_GENN_nadir_sup2_wOI = xr.open_dataset(FP_GENN_nadir_file_sup2_wOI,decode_times=False).ssh.values
FP_GENN_nadir_unsup_wOI = xr.open_dataset(FP_GENN_nadir_file_unsup_wOI,decode_times=False).ssh.values
FP_GENN_nadirswot_sup1 = xr.open_dataset(FP_GENN_nadirswot_file_sup1,decode_times=False).ssh.values
FP_GENN_nadirswot_sup2 = xr.open_dataset(FP_GENN_nadirswot_file_sup2,decode_times=False).ssh.values
FP_GENN_nadirswot_unsup = xr.open_dataset(FP_GENN_nadirswot_file_unsup,decode_times=False).ssh.values
FP_GENN_nadirswot_sup1_wOI = xr.open_dataset(FP_GENN_nadirswot_file_sup1_wOI,decode_times=False).ssh.values
FP_GENN_nadirswot_sup2_wOI = xr.open_dataset(FP_GENN_nadirswot_file_sup2_wOI,decode_times=False).ssh.values
FP_GENN_nadirswot_unsup_wOI = xr.open_dataset(FP_GENN_nadirswot_file_unsup_wOI,decode_times=False).ssh.values

## store all data in a list
if domain=="OSMOSIS":
    ymax = 0.3
else:
    ymax = 0.2

# list_data (nadir)
list_data   = [GT, OBS_nadir, FP_GENN_nadir_sup1, FP_GENN_nadir_sup2, FP_GENN_nadir_unsup,
               FP_GENN_nadir_sup1_wOI, FP_GENN_nadir_sup2_wOI, FP_GENN_nadir_unsup_wOI]

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

# arguments for plots (nadir)
labels_data = np.array(['GT','Obs (nadir)','Supervised 1','Supervised 2','Unsupervised','Supervised 1 + OI','Supervised 2 + OI','Unsupervised + OI'])
colors      = np.array(['k','','red','red','red','blue','blue','blue'])
symbols     = np.array(['k','','o','o','o','o','o','o'])
lstyle      = np.array(['solid','','solid','dashed','dotted','solid','dashed','dotted'])
lwidth      = np.array([2,2,1,1,1,1,1,1])
## Export methods to NetCDF
ncdf_file=workpath+"/NetCDF_nadir_GENNs.nc"
export_NetCDF(list_data,labels_data,lday,lon,lat,ncdf_file)
## nRMSE time series
resfile=workpath+"/TS_nRMSE_nadir_GENNs.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)

# list_data (nadir+swot)
list_data   = [GT, OBS_nadirswot, FP_GENN_nadirswot_sup1, FP_GENN_nadirswot_sup2, FP_GENN_nadirswot_unsup,
               FP_GENN_nadirswot_sup1_wOI, FP_GENN_nadirswot_sup2_wOI, FP_GENN_nadirswot_unsup_wOI]

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

labels_data = np.array(['GT','Obs (nadir+swot)','Supervised 1','Supervised 2','Unsupervised','Supervised 1 + OI','Supervised 2 + OI','Unsupervised + OI'])

## Export methods to NetCDF
ncdf_file=workpath+"/NetCDF_nadirswot_GENNs.nc"
export_NetCDF(list_data,labels_data,lday,lon,lat,ncdf_file)
## nRMSE time series
resfile=workpath+"/TS_nRMSE_nadirswot_GENNs.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)
