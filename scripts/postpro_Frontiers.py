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
GT_file               = "/gpfswork/rech/yrf/uba22to/Metrics_NATL60/data/NATL60_"+domain+"_XP1_GT.nc"
OBS_file              = "/gpfswork/rech/yrf/uba22to/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_NADIRSWOT_obs.nc"
OI_file               = "/gpfswork/rech/yrf/uba22to/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OI_NADIRSWOT_obs.nc"
AnDA_file             = scratchpath+'/resAnDA_nadirswot_nadlag_'+AnDA_lag+"_"+type_obs+'/NATL60_'+domain+'_XP1_AnDA.nc'
DINEOF_file           = scratchpath+'/resAnDA_nadirswot_nadlag_'+AnDA_lag+"_"+type_obs+'/NATL60_'+domain+'_XP1_DINEOF.nc'
FP_GENN_sup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_128x128x05_GENN_1_10_05_FP_Supervised_2.nc"
FP_GENN_unsup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_128x128x05_GENN_1_10_05_FP_Unsupervised_2.nc"
SubGrad_GENN_sup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_128x128x05_GENN_1_10_05_SubGradConv_Supervised_2.nc"
SubGrad_GENN_unsup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_128x128x05_GENN_1_10_05_SubGradConv_Unsupervised_2.nc"
FP_ConvAE_sup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_128x128x05_AEMLP10_FP_Supervised_2.nc"
FP_ConvAE_unsup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_128x128x05_AEMLP10_FP_Unsupervised_2.nc"
SubGrad_ConvAE_sup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_200x200x05_AEMLP10_SubGradConv10_Supervised_2.nc"
SubGrad_ConvAE_unsup_file          = "/gpfswork/rech/yrf/commun/ResRONAN/resSWOT_XP2_200x200x05_AEMLP10_SubGradConv5_Unsupervised_2.nc"

# Reload results
lday    = xr.open_dataset(GT_file,decode_times=False).Time.values
GT      = xr.open_dataset(GT_file,decode_times=False).ssh.values
OBS     = xr.open_dataset(OBS_file,decode_times=False).ssh.values
OI      = xr.open_dataset(OI_file,decode_times=False).ssh.values
AnDA    = xr.open_dataset(AnDA_file,decode_times=False).ssh.values
DINEOF  = xr.open_dataset(DINEOF_file,decode_times=False).ssh.values
FP_GENN_sup = xr.open_dataset(FP_GENN_sup_file,decode_times=False).ssh.values
FP_GENN_unsup = xr.open_dataset(FP_GENN_unsup_file,decode_times=False).ssh.values
SubGrad_GENN_sup = xr.open_dataset(SubGrad_GENN_sup_file,decode_times=False).ssh.values
SubGrad_GENN_unsup = xr.open_dataset(SubGrad_GENN_unsup_file,decode_times=False).ssh.values
FP_ConvAE_sup = xr.open_dataset(FP_ConvAE_sup_file,decode_times=False).ssh.values
FP_ConvAE_unsup = xr.open_dataset(FP_ConvAE_unsup_file,decode_times=False).ssh.values
SubGrad_ConvAE_sup = xr.open_dataset(SubGrad_ConvAE_sup_file,decode_times=False).ssh.values
SubGrad_ConvAE_unsup = xr.open_dataset(SubGrad_ConvAE_unsup_file,decode_times=False).ssh.values
# for AE-scores...
rec_FP_GENN_sup = xr.open_dataset(FP_GENN_sup_file,decode_times=False).sshGTAE.values
rec_FP_GENN_unsup = xr.open_dataset(FP_GENN_unsup_file,decode_times=False).sshGTAE.values
rec_SubGrad_GENN_sup = xr.open_dataset(SubGrad_GENN_sup_file,decode_times=False).sshGTAE.values
rec_SubGrad_GENN_unsup = xr.open_dataset(SubGrad_GENN_unsup_file,decode_times=False).sshGTAE.values
rec_FP_ConvAE_sup = xr.open_dataset(FP_ConvAE_sup_file,decode_times=False).sshGTAE.values
rec_FP_ConvAE_unsup = xr.open_dataset(FP_ConvAE_unsup_file,decode_times=False).sshGTAE.values
rec_SubGrad_ConvAE_sup = xr.open_dataset(SubGrad_ConvAE_sup_file,decode_times=False).sshGTAE.values
rec_SubGrad_ConvAE_unsup = xr.open_dataset(SubGrad_ConvAE_unsup_file,decode_times=False).sshGTAE.values

# list_data (nadir+swot)
list_data   = [GT, OBS, OI, AnDA, DINEOF, 
               FP_GENN_sup, FP_GENN_unsup, SubGrad_GENN_sup, SubGrad_GENN_unsup,
               FP_ConvAE_sup, FP_ConvAE_unsup, SubGrad_ConvAE_sup, SubGrad_ConvAE_unsup,
               rec_FP_GENN_sup, rec_FP_GENN_unsup, rec_SubGrad_GENN_sup, rec_SubGrad_GENN_unsup,
               rec_FP_ConvAE_sup, rec_FP_ConvAE_unsup, rec_SubGrad_ConvAE_sup, rec_SubGrad_ConvAE_unsup]
labels_data = np.array(['GT','Obs (nadir+swot)','OI (nadir+swot)','Post-AnDA (nadir+swot)','VE-DINEOF (nadir+swot)','FP-GENN supervised (nadir+swot)', 'FP-GENN unsupervised (nadir+swot)','SubGrad-GENN supervised (nadir+swot)','SubGrad-GENN unsupervised (nadir+swot)','FP-ConvAE supervised (nadir+swot)','FP-ConvAE unsupervised (nadir+swot)','SubGrad-ConvAE supervised (nadir+swot)','SubGrad-ConvAE unsupervised (nadir+swot)','rec FP-GENN supervised (nadir+swot)', 'rec FP-GENN unsupervised (nadir+swot)','rec SubGrad-GENN supervised (nadir+swot)','rec SubGrad-GENN unsupervised (nadir+swot)','rec FP-ConvAE supervised (nadir+swot)','rec FP-ConvAE unsupervised (nadir+swot)','rec SubGrad-ConvAE supervised (nadir+swot)','rec SubGrad-ConvAE unsupervised (nadir+swot)'])
list_suffix = np.array(['GT','Obs_nadirswot','OI_nadirswot','Post_AnDA_nadirswot','VE_DINEOF_nadirswot','FP_GENN_nadirswot_sup','FP_GENN_nadirswot_unsup','SubGrad_GENN_nadirswot_sup','SubGrad_GENN_nadirswot_unsup','FP_ConvAE_nadirswot_sup','FP_ConvAE_nadirswot_unsup','SubGrad_ConvAE_nadirswot_sup','SubGrad_ConvAE_nadirswot_unsup','rec_FP_GENN_nadirswot_sup','rec_FP_GENN_nadirswot_unsup','rec_SubGrad_GENN_nadirswot_sup','rec_SubGrad_GENN_nadirswot_unsup','rec_FP_ConvAE_nadirswot_sup','rec_FP_ConvAE_nadirswot_unsup','rec_SubGrad_ConvAE_nadirswot_sup','rec_SubGrad_ConvAE_nadirswot_unsup'])
colors      = np.array(['k','','red','seagreen','steelblue','darkorange'])
symbols     = np.array(['k','','o','o','o','o'])
lstyle      = np.array(['solid','','solid','solid','solid','solid'])
lwidth      = np.array([2,2,2,1,1,1])

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
plot_maps(list_data,list_suffix,labels_data,lday,"2012-12-08",extent,lon,lat,workpath)
## Compute R/I/AE scores
resfile=workpath+"/RIAE_scores_nadirswot.png"
RIAE_scores(list_data,labels_data,resfile,.25,gradient=False)
resfile=workpath+"/RIAE_Grad_scores_nadirswot.png"
RIAE_scores(list_data,labels_data,resfile,.25,gradient=True)
'''## Export methods to NetCDF
ncdf_file=workpath+"/NetCDF_nadirswot.nc"
export_NetCDF(list_data,labels_data,lday,lon,lat,ncdf_file)
## test PSD
#resfile=workpath+"/BOOST_PSD_nadirswot"
#plot_psd(ncdf_file,labels_data,lday,resfile)
## Compute R/I/AE scores
#resfile=workpath+"/RIAE_scores_nadirswot.png"
#RIAE_scores(list_data,labels_data,resfile,gradient=False)
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
resfile=workpath+"/SNR_nadirswot.png"
resssh=4*dwscale
plot_SNR(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,resssh,resfile)
## average Taylor diagrams
resfile=workpath+"/Taylor_diagram_nadirswot.png"
Taylor_diagram(list_data,labels_data,colors,symbols,resfile)
'''
