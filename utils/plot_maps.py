def plot_maps(list_data,list_suffix,labels_data,list_day,date,extent,lon,lat,workpath):
    # vmin/vmax based on GT
    iday = np.where(list_day==date)[0][0]
    vmax = np.nanmax(np.abs(list_data[0][iday]))
    vmin = -1.*vmax
    grad_vmax = np.nanmax(np.abs(Gradient(list_data[0][iday],2)))
    grad_vmin = 0
    for i in range(len(list_data)):
        resfile = workpath+"/results_"+list_suffix[i]+'_'+date+".png"
        fig, ax = plt.subplots(1,1,figsize=(10,10),squeeze=False,
                          subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
        plot(ax,0,0,lon,lat,list_data[i][iday],labels_data[i],\
             extent=extent,cmap="coolwarm",vmin=vmin,vmax=vmax)
        plt.savefig(resfile)       # save the figure
        plt.close()                # close the figure

        resfile = workpath+"/results_Grad_"+list_suffix[i]+'_'+date+".png"
        fig, ax = plt.subplots(1,1,figsize=(10,10),squeeze=False,
                          subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
        if len(str.split(labels_data[i]))>1:
            plot(ax,0,0,lon,lat,Gradient(list_data[i][iday],2),r"$\nabla_{"+str.split(labels_data[i])[0]+"}$ "+str.split(labels_data[i])[1],\
                extent=extent,cmap="viridis",vmin=grad_vmin,vmax=grad_vmax)
        else:
            plot(ax,0,0,lon,lat,Gradient(list_data[i][iday],2),r"$\nabla_{"+labels_data[i]+"}$",\
                extent=extent,cmap="viridis",vmin=grad_vmin,vmax=grad_vmax)
        plt.savefig(resfile)       # save the figure
        plt.close()                # close the figure


