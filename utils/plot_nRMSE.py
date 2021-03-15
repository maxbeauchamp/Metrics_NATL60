from Metrics_NATL60 import *

## 1) Function for plotting nRMSE
def plot_nRMSE(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,ymax,resfile,gradient=False):

    N   = len(lday)
    GT  = list_data[0]
    ## Compute spatial coverage  
    if any("Obs (nadir+swot)"==s for s in labels_data):
        spatial_coverage_nadirswot = []
        id_obs = np.where(labels_data=="Obs (nadir+swot)")[0][0]
        OBS = list_data[id_obs]
        for j in range(len(lday)):
            spatial_coverage_nadirswot.append(100*len(np.argwhere(np.isfinite(OBS[j].flatten())))/len(OBS[j].flatten()))
    if any("Obs (nadir)"==s for s in labels_data):
        spatial_coverage_nadir = []
        id_obs = np.where(labels_data=="Obs (nadir)")[0][0]
        OBS = list_data[id_obs]
        for j in range(len(lday)):
            spatial_coverage_nadir.append(100*len(np.argwhere(np.isfinite(OBS[j].flatten())))/len(OBS[j].flatten()))

    # Compute nRMSE time series
    nRMSE = []
    id1=np.where(["GT" not in l for l in labels_data ])[0]
    id2=np.where(["Obs" not in l for l in labels_data ])[0]
    id_plot=np.intersect1d(id1,id2)
    for i in range(len(labels_data[id_plot])):
        nRMSE_=[]
        meth_i=list_data[id_plot[i]]
        for j in range(len(lday)):
            if gradient == False:
                nRMSE_.append((np.sqrt(np.nanmean(((GT[j]-np.nanmean(GT[j]))-(meth_i[j]-np.nanmean(meth_i[j])))**2)))/np.nanstd(GT[j]))
            else:
                nRMSE_.append((np.sqrt(np.nanmean(((Gradient(GT[j],2)-np.nanmean(Gradient(GT[j],2)))-(Gradient(meth_i[j],2)-np.nanmean(Gradient(meth_i[j],2))))**2)))/np.nanstd(Gradient(GT[j],2)))
        nRMSE.append(nRMSE_)

    # plot nRMSE time series
    for i in range(len(labels_data[id_plot])):
        if gradient == False:
            plt.plot(range(N),nRMSE[i],linestyle=lstyle[id_plot[i]],color=colors[id_plot[i]],linewidth=lwidth[id_plot[i]],label=labels_data[id_plot[i]])
        else:
            plt.plot(range(N),nRMSE[i],linestyle=lstyle[id_plot[i]],color=colors[id_plot[i]],linewidth=lwidth[id_plot[i]],label=r"$\nabla_{"+str.split(labels_data[id_plot[i]])[0]+"}$ "+str.split(labels_data[id_plot[i]])[1])

    # add vertical bar to divide the 4 periods
    plt.axvline(x=19)
    plt.axvline(x=39)
    plt.axvline(x=59)
    # graphical options
    plt.ylim(0,ymax)
    plt.ylabel('nRMSE')
    plt.xlabel('Time (days)')
    idx = np.arange(0,len(lday),5,dtype=int)
    plt.set_xticks(idx)
    plt.set_xticklabels([ lday[i] for i in idx ],rotation=45, ha='right')
    plt.margins(x=0)
    plt.grid(True,alpha=.3)
    plt.legend(loc='upper left',prop=dict(size='small'),frameon=False,bbox_to_anchor=(0,1.02,1,0.2),ncol=2,mode="expand")
    # second axis with spatial coverage
    axes2 = plt.twinx()
    width=0.75
    if ( (any("Obs (nadir+swot)"==s for s in labels_data)) and any("Obs (nadir)"==s for s in labels_data) ):
        p1 = axes2.bar(range(N), spatial_coverage_nadir, width,color='r',alpha=0.25)
        p2 = axes2.bar(range(N), [spatial_coverage_nadirswot[i]-spatial_coverage_nadir[i] for i in range(len(spatial_coverage_nadir))], width,bottom=spatial_coverage_nadir,color='g',alpha=0.25)
    elif any("Obs (nadir+swot)"==s for s in labels_data):
        p1 = axes2.bar(range(N), spatial_coverage_nadirswot, width,color='g',alpha=0.25)
    else:
        p1 = axes2.bar(range(N), spatial_coverage_nadir, width,color='r',alpha=0.25)
    axes2.set_ylim(0, 100)
    axes2.set_ylabel('Spatial Coverage (%)')
    axes2.margins(x=0)
    plt.savefig(resfile,bbox_inches="tight")    # save the figure
    plt.close()                                 # close the figure


