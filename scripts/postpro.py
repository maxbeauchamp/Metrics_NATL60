#!/usr/bin/env python

__author__ = "Maxime Beauchamp"
__version__ = "0.1"
__date__ = "2020-12-10"
__email__ = "maxime.beauchamp@imt-atantique.fr"

from pathlib import Path

from Metrics_NATL60 import *

# function to create recursive paths
from ruamel import yaml

#
# AnDA_lag   = sys.argv[1]
# NN_lag     = sys.argv[2]
# type_obs   = sys.argv[3]
# domain     = sys.argv[4]

workpath = Path("work")
workpath.mkdir(exist_ok=True, parents=True)

XP=2 # XP = 1....5
workpath = Path("work")
workpath.mkdir(exist_ok=True, parents=True)
subm = 'submissions_XP'+str(XP)
submissions_files = list(Path(subm).glob('*'))
submission_data =[]
for sub_file in submissions_files:
    with open(sub_file, 'r') as f:
        submission_data.append(yaml.load(f))

sub_df = pd.DataFrame(submission_data)
(workpath / "submission.md").write_text(sub_df.to_markdown())
for domain in sub_df.domain.drop_duplicates():
    sub_domain = sub_df.loc[lambda df: df.domain == domain]
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
    GT_file               = "https://s3.eu-central-1.wasabisys.com/melody/Metrics_NATL60/data/NATL60_"+domain+"_XP1_GT.nc#mode=bytes"
    OBS_file              = "https://s3.eu-central-1.wasabisys.com/melody/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OBS_NADIRSWOT_mod.nc#mode=bytes"
    OI_file               = "https://s3.eu-central-1.wasabisys.com/melody/Metrics_NATL60/data/NATL60_"+domain+"_XP1_OI_NADIRSWOT_mod.nc#mode=bytes"
    sub_files = sub_domain['data']

    # Reload results
    lday    = xr.open_dataset(GT_file,decode_times=False).Time.values
    GT      = xr.open_dataset(GT_file,decode_times=False).ssh.values
    OBS     = xr.open_dataset(OBS_file,decode_times=False).ssh.values
    OI      = xr.open_dataset(OI_file,decode_times=False).ssh.values
    sub_ds      = [xr.open_dataset(f"{sub_file}#mode=bytes",decode_times=False).ssh.values for sub_file in sub_files]

    # list_data (nadir+swot)
    list_data   = [GT, OBS, OI, *sub_ds]
    labels_data = np.array(['GT','Obs (nadir+swot)','OI (nadir+swot)', *sub_domain['experiment_label']])
    list_suffix = np.array(['GT','Obs_nadirswot','OI_nadirswot',*sub_domain['experiment_slug']])
    colors = np.array(
        ['k', '', 'red', 'seagreen', 'steelblue', 'darkorange', '', 'red', 'seagreen', 'steelblue', 'darkorange'])[:len(list_data)]
    symbols = np.array(['k', '', 'p', 'p', 'p', 'p', 'p', '', 'o', 'o', 'o', 'o', 'o'])[:len(list_data)]
    lstyle = np.array(
        ['solid', '', 'dashed', 'dashed', 'dashed', 'dashed', 'dashed', '', 'solid', 'solid', 'solid', 'solid',
         'solid'])[:len(list_data)]
    lwidth = np.array([2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1])[:len(list_data)]

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


    if domain=="OSMOSIS":
        ymax = 0.3
    else:
        ymax = 0.2
    resfile=workpath / f"{domain}_TS_nRMSE_nadirswot.png"
    plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False)
    resfile=workpath / f"{domain}_TS_nRMSE_Grad_nadirswot.png"
    plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=True)

    resfile=workpath / f"{domain}_nrmse_score.txt"
    nRMSE_scores(list_data,labels_data,resfile,gradient=False)

