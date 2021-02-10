def PSD(ds,time,method):

    # Compute error = SSH_reconstruction - SSH_true
    err = (ds['GT'] - ds[method])
    # rechunk
    err = err.chunk({"lat":1, 'time': err['time'].size, 'lon': err['lon'].size})
    err['time'] = time

    # Rechunk SSH_true
    signal = ds['GT'].chunk({"lat":1, 'time': ds['time'].size, 'lon': ds['lon'].size})
    # make time vector in days units
    signal['time'] = time

    # Compute PSD_err and PSD_signal
    psd_err = xrft.power_spectrum(err, dim=['time', 'lon'], detrend='linear', window=True).compute()
    psd_signal = xrft.power_spectrum(signal, dim=['time', 'lon'], detrend='linear', window=True).compute()

    # Averaged over latitude
    mean_psd_signal = psd_signal.mean(dim='lat').where((psd_signal.freq_lon > 0.) & (psd_signal.freq_time > 0), drop=True)
    mean_psd_err = psd_err.mean(dim='lat').where((psd_err.freq_lon > 0.) & (psd_err.freq_time > 0), drop=True)

    # return PSD-based score
    psd_based_score = (1.0 - mean_psd_err/mean_psd_signal)

    # Find the key metrics: shortest temporal & spatial scales resolved based on the 0.5 contour criterion of the PSD_score
    level = [0.5]
    cs = plt.contour(1./psd_based_score.freq_lon.values,1./psd_based_score.freq_time.values, psd_based_score, level)
    x05, y05 = cs.collections[0].get_paths()[0].vertices.T

    shortest_spatial_wavelength_resolved = np.min(x05)
    shortest_temporal_wavelength_resolved = np.min(y05)

    return (1.0 - mean_psd_err/mean_psd_signal), np.round(shortest_spatial_wavelength_resolved, 2), np.round(shortest_temporal_wavelength_resolved, 2)

def plot_psd_score(ds_psd,resfile):

    try:
        nb_experiment = len(ds_psd.experiment)
    except:
        nb_experiment = 1

    fig, ax0 =  plt.subplots(1, nb_experiment, sharey=True, figsize=(5*nb_experiment, 5))
    #plt.subplots_adjust(right=0.1, left=0.09)
    for exp in range(nb_experiment):
        try:
            ctitle = ds_psd.experiment.values[exp]
        except:
            ctitle = ''

        if nb_experiment > 1:
            ax = ax0[exp]
            data = (ds_psd.isel(experiment=exp).values)
        else:
            ax = ax0
            data = (ds_psd.values)
        ax.invert_yaxis()
        ax.invert_xaxis()
        c1 = ax.contourf(1./(ds_psd.freq_lon), 1./ds_psd.freq_time, data,
                          levels=np.arange(0,1.1, 0.1), cmap='RdYlGn', extend='both')
        ax.set_xlabel('spatial wavelength (degree_lon)', fontweight='bold', fontsize=18)
        ax0[0].set_ylabel('temporal wavelength (days)', fontweight='bold', fontsize=18)
        #plt.xscale('log')
        ax.set_yscale('log')
        ax.grid(linestyle='--', lw=1, color='w')
        ax.tick_params(axis='both', labelsize=18)
        ax.set_title(f'PSD-based score ({ctitle})', fontweight='bold', fontsize=18)
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_formatter(ScalarFormatter())
        c2 = ax.contour(1./(ds_psd.freq_lon), 1./ds_psd.freq_time, data, levels=[0.5], linewidths=2, colors='k')

        cbar = fig.colorbar(c1, ax=ax, pad=0.01)
        cbar.add_lines(c2)

    bbox_props = dict(boxstyle="round,pad=0.5", fc="w", ec="k", lw=2)
    ax0[-1].annotate('Resolved scales',
                    xy=(1.2, 0.8),
                    xycoords='axes fraction',
                    xytext=(1.2, 0.55),
                    bbox=bbox_props,
                    arrowprops=
                        dict(facecolor='black', shrink=0.05),
                        horizontalalignment='left',
                        verticalalignment='center')

    ax0[-1].annotate('UN-resolved scales',
                    xy=(1.2, 0.2),
                    xycoords='axes fraction',
                    xytext=(1.2, 0.45),
                    bbox=bbox_props,
                    arrowprops=
                    dict(facecolor='black', shrink=0.05),
                        horizontalalignment='left',
                        verticalalignment='center')

    plt.savefig(resfile)
    plt.close()                # close the figure

def plot_psd(ncdf_file,labels_data,list_day,resfile,periods=[[0,20],[20,40],[40,60],[60,80]]):

    ds = xr.open_dataset(ncdf_file)
    dt64 = [ np.datetime64(datetime.strptime(day,'%Y-%m-%d')) for day in list_day ]
    time_u = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 'D')

    # loop over the 4 periods
    list_PSD_all_periods = []
    id1=np.where(["GT" not in l for l in labels_data ])[0]
    id2=np.where(["Obs" not in l for l in labels_data ])[0]
    id_plot=np.intersect1d(id1,id2)
    for i in range(len(periods)):
        list_PSD = []
        ds2  = ds.isel(time=slice(periods[i][0], periods[i][1]))
        time = time_u[periods[i][0]:periods[i][1]]-time_u[periods[i][0]]
        # loop over the methods
        for j in range(len(labels_data[id_plot])):
            list_PSD.append(PSD(ds2,time,labels_data[id_plot[j]])[0])

        ds_psd = xr.concat(list_PSD, dim='experiment')
        ds_psd['experiment'] = labels_data[id_plot]
        plot_psd_score(ds_psd,resfile+"_period"+str(i)+".png")

        list_PSD_all_periods.append(list_PSD)

    # average
    list_PSD = []
    for j in range(len(labels_data[id_plot])):

        ds_psd = xr.concat([list_PSD_all_periods[i][j] for i in range(len(periods))],dim='period')
        mean   = ds_psd.mean('period')
        list_PSD.append(mean)

    ds_psd = xr.concat(list_PSD, dim='experiment')
    ds_psd['experiment'] = labels_data[id_plot]
    plot_psd_score(ds_psd,resfile+"_mean.png")

