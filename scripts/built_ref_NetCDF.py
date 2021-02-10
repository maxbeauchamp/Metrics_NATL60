from Metrics_NATL60 import *

lon = xr.open_dataset(
datapath+"/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).lon.values[:200]
lat = xr.open_dataset(
datapath+"/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).ssh.values[indN_Tt,:200,:200]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_GULFSTREAM_XP1_GT.nc", mode='w')

lon = xr.open_dataset(
datapath+"/OSMOSIS/ref/NATL60-CJM165_OSMOSIS_ssh_y2013.1y.nc",decode_times=False).lon.values[:160]
lat = xr.open_dataset(
datapath+"/OSMOSIS/ref/NATL60-CJM165_OSMOSIS_ssh_y2013.1y.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)  # index of training period
time = xr.open_dataset(datapath+"/OSMOSIS/ref/NATL60-CJM165_OSMOSIS_ssh_y2013.1y.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/OSMOSIS/ref/NATL60-CJM165_OSMOSIS_ssh_y2013.1y.nc",decode_times=False).ssh.values[indN_Tt,:200,:160]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_OSMOSIS_XP1_GT.nc", mode='w')

# % OI

lon = xr.open_dataset(
datapath+"/GULFSTREAM/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).lon.values[:200]
lat = xr.open_dataset(
datapath+"/GULFSTREAM/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/GULFSTREAM/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/GULFSTREAM/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:200]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_GULFSTREAM_XP1_OI_NADIRSWOT.nc", mode='w')

lon = xr.open_dataset(
datapath+"/OSMOSIS/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).lon.values[:160]
lat = xr.open_dataset(
datapath+"/OSMOSIS/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/OSMOSIS/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/OSMOSIS/oi/ssh_NATL60_swot_4nadir.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:160]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_OSMOSIS_XP1_OI_NADIRSWOT.nc", mode='w')

lon = xr.open_dataset(
datapath+"/GULFSTREAM/oi/ssh_NATL60_4nadir.nc",decode_times=False).lon.values[:200]
lat = xr.open_dataset(
datapath+"/GULFSTREAM/oi/ssh_NATL60_4nadir.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/GULFSTREAM/oi/ssh_NATL60_4nadir.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/GULFSTREAM/oi/ssh_NATL60_4nadir.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:200]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_GULFSTREAM_XP1_OI_NADIR.nc", mode='w')

lon = xr.open_dataset(
datapath+"/OSMOSIS/oi/ssh_NATL60_4nadir.nc",decode_times=False).lon.values[:160]
lat = xr.open_dataset(
datapath+"/OSMOSIS/oi/ssh_NATL60_4nadir.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/OSMOSIS/oi/ssh_NATL60_4nadir.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/OSMOSIS/oi/ssh_NATL60_4nadir.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:160]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_OSMOSIS_XP1_OI_NADIR.nc", mode='w')


# % DATA

lon = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).lon.values[:160]
lat = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:160]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_OSMOSIS_XP1_OBS_NADIR.nc", mode='w')

lon = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).lon.values[:160]
lat = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/OSMOSIS/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:160]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_OSMOSIS_XP1_OBS_NADIRSWOT.nc", mode='w')


lon = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).lon.values[:200]
lat = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:200]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_GULFSTREAM_XP1_OBS_NADIR.nc", mode='w')

lon = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).lon.values[:200]
lat = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T
ssh = xr.open_dataset(datapath+"/GULFSTREAM/data/gridded_data_swot_wocorr/dataset_nadir_0d_swot.nc",decode_times=False).ssh_obs.values[indN_Tt,:200,:200]
xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': indN_Tt})
xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
xrdata.to_netcdf(path=basepath+"/Metrics_NATL60/data/NATL60_GULFSTREAM_XP1_OBS_NADIRSWOT.nc", mode='w')

