def nRMSE_scores(list_data,labels_data,resfile,gradient=False):

    # select only 10-day windows
    index=list(range(5,16))
    index.extend(range(25,36))
    index.extend(range(45,56))
    index.extend(range(65,76))

    GT  = list_data[0][index]

    # Compute nRMSE scores
    id1=np.where(["GT" not in l for l in labels_data ])[0]
    id2=np.where(["Obs" not in l for l in labels_data ])[0]
    id_plot=np.intersect1d(id1,id2)
    tab_scores = np.zeros((len(labels_data[id_plot]),3))
    for i in range(len(labels_data[id_plot])):
        meth_i=list_data[id_plot[i]][index]
        print(labels_data[id_plot[i]])
        nRMSE=[]
        for j in range(len(meth_i)):
            if gradient==False:
                nRMSE.append((np.sqrt(np.nanmean(((GT[j]-np.nanmean(GT[j]))-(meth_i[j]-np.nanmean(meth_i[j])))**2)))/np.nanstd(GT[j]))
            else:
                nRMSE.append((np.sqrt(np.nanmean(((Gradient(GT[j],2)-np.nanmean(Gradient(GT[j],2)))-(Gradient(meth_i[j],2)-np.nanmean(Gradient(meth_i[j],2))))**2)))/np.nanstd(Gradient(GT[j],2)))
        tab_scores[i,0] = np.nanmean(nRMSE)
        tab_scores[i,1] = np.percentile(nRMSE,5)
        tab_scores[i,2] = np.percentile(nRMSE,95)

    np.savetxt(fname=resfile,X=tab_scores,fmt='%2.2f')

