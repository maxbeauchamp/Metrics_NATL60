def plot_SNR(list_data,labels_data,colors,symbols,lstyle,lwidth,lday,resssh,resfile):

    # select only 10-day windows
    index=list(range(5,16))
    index.extend(range(25,36))
    index.extend(range(45,56))
    index.extend(range(65,76))

    GT  = list_data[0][index]

    # Compute Signal-to-Noise ratio
    SNR = []
    id1=np.where(["GT" not in l for l in labels_data ])[0]
    id2=np.where(["Obs" not in l for l in labels_data ])[0]
    id_plot=np.intersect1d(id1,id2)
    for i in range(len(labels_data[id_plot])):
        print(labels_data[id_plot[i]])
        f, Pf  = avg_err_raPsd2dv1(list_data[id_plot[i]][index],GT,resssh,True)
        wf     = 1./f
        SNR.append([wf, Pf])

    # plot Signal-to-Noise ratio
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(len(labels_data[id_plot])):
        wf, Pf = SNR[i]
        ax.plot(wf,Pf,linestyle=lstyle[id_plot[i]],color=colors[id_plot[i]],linewidth=lwidth[id_plot[i]],label=labels_data[id_plot[i]])
    #plt.axhline(y=0.5, color='r', linestyle='-')
    ax.set_xlabel("Wavenumber", fontweight='bold')
    ax.set_ylabel("Signal-to-noise ratio", fontweight='bold')
    ax.set_xscale('log') ; ax.set_yscale('log')
    plt.legend(loc='best',prop=dict(size='small'),frameon=False)
    plt.xticks([50, 100, 200, 500, 1000], ["50km", "100km", "200km", "500km", "1000km"])
    ax.invert_xaxis()
    plt.grid(which='both', linestyle='--')
    plt.savefig(resfile) # save the figure
    plt.close()          # close the figure


