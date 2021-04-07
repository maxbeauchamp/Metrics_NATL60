import pathlib
import numpy as np
import xarray as xr
import pickle
list_files = list(pathlib.Path('/gpfsscratch/rech/yrf/uba22to/4DVARNN-DinAE_xp/GULFSTREAM/OSSE').glob('**/*.pickle'))

domain="GULFSTREAM"
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

lon = xr.open_dataset(
"/gpfswork/rech/yrf/uba22to/DATA/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).lon.values[:200]
lat = xr.open_dataset(
"/gpfswork/rech/yrf/uba22to/DATA/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).lat.values[:200]
indN_Tt = np.concatenate([np.arange(60,80),np.arange(140,160),\
                             np.arange(220,240),np.arange(300,320)])  # index of evaluation period
indN_Tr = np.delete(range(365),indN_Tt)                               # index of training period
time = xr.open_dataset("/gpfswork/rech/yrf/uba22to/DATA/GULFSTREAM/ref/NATL60-CJM165_GULFSTREAM_ssh_y2013.1y.nc",decode_times=False).time.values[indN_Tt]
mesh_lat, mesh_lon = np.meshgrid(lat, lon)
mesh_lat = mesh_lat.T
mesh_lon = mesh_lon.T


for file in list_files:
    file  = str(file)
    print(file)
    split = file.split("/")
    path  = '/'.join(split[:-1])+"/"
    if("AnDA" in str(file)):
        with open(file, 'rb') as handle:
            AnDA, DINEOF = pickle.load(handle)
        AnDA = AnDA.itrp_postAnDA[:,:indLat,:indLon]
        DINEOF = DINEOF[:,:indLat,:indLon]
        # AnDA
        ssh = AnDA
        xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': range(0,len(time))})
        xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
        xrdata.to_netcdf(path=path+"NATL60_GULFSTREAM_XP1_AnDA.nc", mode='w')
        # DINEOF
        ssh = DINEOF
        xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': range(0,len(time))})
        xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
        xrdata.to_netcdf(path=path+"NATL60_GULFSTREAM_XP1_DINEOF.nc", mode='w')
    else:
        if("GENN" in str(file)):
            suf = (split[-1].split("_"))[2]
            with open(file, 'rb') as handle:
                itrp, rec = pickle.load(handle)[7:9]
            itrp = itrp[:,:indLat,:indLon]
            rec  = rec[:,:indLat,:indLon]
            # itrp
            ssh = itrp
            if(len(ssh)==len(time)):
                xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': range(0,len(time))})
                xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
                xrdata.to_netcdf(path=path+"NATL60_GULFSTREAM_XP1_GENN"+suf+".nc", mode='w')
            # rec
            ssh = rec
            if(len(ssh)==len(time)):
                xrdata = xr.Dataset(\
                data_vars={'longitude': (('lat','lon'),mesh_lon),\
                           'latitude' : (('lat','lon'),mesh_lat),\
                           'Time'     : (('time'),time),\
                           'ssh'  : (('time','lat','lon'),ssh)},\
                coords={'lon': lon,'lat': lat,'time': range(0,len(time))})
                xrdata.time.attrs['units']='days since 2012-10-01 00:00:00'
                xrdata.to_netcdf(path=path+"NATL60_GULFSTREAM_XP1_recGENN"+suf+".nc", mode='w')

