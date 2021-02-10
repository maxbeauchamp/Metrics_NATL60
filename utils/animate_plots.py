def animate_plots(list_data,labels_data,lday,extent,lon,lat,resfile,gradient=False):

    def animate(i, fig, ax):
        print(i)
        for ivar in range(len(list_data)):
            ii = int(np.floor(ivar/3))
            jj = int(np.floor(ivar%3))
            ax[ii][jj].cla()
            if gradient==True:
                cmap="viridis"
                if len(str.split(labels_data[ivar]))>1:
                    title = r"$\nabla_{"+str.split(labels_data[ivar])[0]+"}$ "+str.split(labels_data[ivar])[1]
                else:
                    title = r"$\nabla_{"+labels_data[ivar]+"}$"
                plot(ax,ii,jj,lon,lat,Gradient(list_data[ivar][i],2),title,
                     extent=extent,cmap=cmap,vmin=vmin,vmax=vmax,colorbar=False)
            else:
                cmap="coolwarm"
                plot(ax,ii,jj,lon,lat,list_data[ivar][i],labels_data[ivar],
                     extent=extent,cmap=cmap,vmin=vmin,vmax=vmax,colorbar=False)
            fig.suptitle(lday[i])
        return fig, ax

    if gradient==False:
        vmax = np.nanmax(np.abs(list_data[0]))
        vmin = -1.*vmax
    else:
        vmax = np.nanmax(np.abs(Gradient(list_data[0],2)))
        vmin = 0

    fig, ax = plt.subplots(int(np.ceil(len(list_data)/3)),3,figsize=(15,10),\
              subplot_kw=dict(projection=ccrs.PlateCarree(central_longitude=0.0)))
    plt.subplots_adjust(hspace=0.5)
    ani = animation.FuncAnimation(fig, animate, frames=np.arange(1,len(list_data[0])), fargs=(fig,ax,), interval=1000, repeat=False)
    writer = animation.FFMpegWriter(fps=1, bitrate=5000)
    ani.save(resfile, writer = writer)
    plt.close()

