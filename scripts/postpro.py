#!/usr/bin/env python

__author__ = "Maxime Beauchamp"
__version__ = "0.1"
__date__ = "2020-12-10"
__email__ = "maxime.beauchamp@imt-atantique.fr"

from pathlib import Path
import sys
sys.path.append('..')
from Metrics_NATL60 import *

# function to create recursive paths
from ruamel import yaml

#
# AnDA_lag   = sys.argv[1]
# NN_lag     = sys.argv[2]
# type_obs   = sys.argv[3]
# domain     = sys.argv[4]

workpath = "work"
Path(workpath).mkdir(exist_ok=True, parents=True)

submissions_file = list(Path('submissions').glob('*'))[0]
with open(submissions_file, 'r') as f:
    sub_data = yaml.load(f)

domain = sub_data.get('domain', 'GULFSTREAM')

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
GT_file               = "data/NATL60_"+domain+"_XP1_GT.nc"
OBS_file              = "data/NATL60_"+domain+"_XP1_OBS_NADIRSWOT.nc"
OI_file               = "data/NATL60_"+domain+"_XP1_OI_NADIRSWOT.nc"
sub_file = sub_data['data']

# Reload results
lday    = xr.open_dataset(GT_file,decode_times=False).Time.values
GT      = xr.open_dataset(GT_file,decode_times=False).ssh.values
OBS     = xr.open_dataset(OBS_file,decode_times=False).ssh.values
OI      = xr.open_dataset(OI_file,decode_times=False).ssh.values
sub_ds      = xr.open_dataset(f"{sub_file}#mode=bytes",decode_times=False).ssh.values

# list_data (nadir+swot)
list_data   = [GT, OBS, OI, sub_ds]
labels_data = np.array(['GT','Obs (nadir+swot)','OI (nadir+swot)', sub_data['experiment_label']])
list_suffix = np.array(['GT','Obs_nadirswot','OI_nadirswot',sub_data['experiment_slug']])
colors      = np.array(['k','','red','seagreen'])
symbols     = np.array(['k','','o','o'])
lstyle      = np.array(['solid','','solid','solid'])
lwidth      = np.array([2,2,2,1])

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

## animation plots
#resfile=workpath+"/animation_nadirswot.mp4"
#animate_plots(list_data,labels_data,lday,extent,lon,lat,resfile,gradient=True)
## plot individual maps (SSH & Gradients)
# plot_maps(list_data,list_suffix,labels_data,lday,"2013-08-04",extent,lon,lat,workpath)
## Export methods to NetCDF
## test PSD
#resfile=workpath+"/BOOST_PSD_nadirswot"
#plot_psd(ncdf_file,labels_data,lday,resfile)
## Compute R/I/AE scores
# resfile=workpath+"/RIAE_scores_nadirswot.png"
# RIAE_scores(list_data,labels_data,resfile, pct_var=10,gradient=False)
## nRMSE time series
if domain=="OSMOSIS":
    ymax = 0.3
else:
    ymax = 0.2
resfile=workpath+"/TS_nRMSE_nadirswot.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)
resfile=workpath+"/TS_nRMSE_Grad_nadirswot.png"
plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=True)
## average SNR
# resfile=workpath+"/SNR_nadirswot.png"
# resssh=4*dwscale
# plot_SNR(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,resssh,resfile)
## average Taylor diagrams
# resfile=workpath+"/Taylor_diagram_nadirswot.png"
# Taylor_diagram(list_data,labels_data,colors,symbols,resfile)
resfile=workpath+"/nrmse_score.txt"
nRMSE_scores(list_data,labels_data,resfile,gradient=False)

