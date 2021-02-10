from Metrics_NATL60 import *

def export_NetCDF(list_data,labels_data,list_day,lon,lat,resfile):

    GT  = list_data[0]
    dt64 = [ np.datetime64(datetime.strptime(day,'%Y-%m-%d')) for day in list_day ]
    time_u = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    mesh_lat, mesh_lon = np.meshgrid(range(len(lat)),range(len(lon)))
    mesh_lat, mesh_lon = mesh_lat.T, mesh_lon.T
    data = xr.Dataset(\
                    data_vars={'longitude': (('lat','lon'),mesh_lon),\
                                'latitude' : (('lat','lon'),mesh_lat),\
                                'Time'     : (('time'),time_u),\
                                'GT'       : (('time','lat','lon'),GT)},\
                    coords={'lon': lon,\
                            'lat': lat,\
                            #'time': range(0,len(time_u))})
                            'time': time_u})
    # add variables
    for i in range(len(labels_data[1:])):
        data[labels_data[i+1]] = (('time','lat','lon'), list_data[i+1])
    # write to file
    data.to_netcdf(resfile)


