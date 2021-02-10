def RIAE_scores(list_data,labels_data,resfile,gradient=False):

    GT  = list_data[0]

    # apply High-Pass Filter to visualize Taylor diagrams only for small scales
    HR = list_data[2]
    lr = np.copy(HR).reshape(HR.shape[0],-1)
    tmp = lr[0,:]
    sea_v2 = np.where(~np.isnan(tmp))[0]
    lr_no_land = lr[:,sea_v2]
    pca = PCA(n_components=.75)
    score_global = pca.fit_transform(lr_no_land)
    coeff_global = pca.components_.T
    mu_global = pca.mean_
    DataReconstructed_global = np.dot(score_global, coeff_global.T) +mu_global
    lr[:,sea_v2] = DataReconstructed_global
    lr = lr.reshape(HR.shape).flatten()

    def Iscore(mask1,gt,itrp):
        return 100*(1-np.nanmean(((mask1*gt-np.nanmean(mask1*gt))-(mask1*itrp-np.nanmean(mask1*itrp)))**2)/np.nanvar(mask1*gt))
    def Rscore(mask1,gt,itrp):
        return 100*(1-np.nanmean(((mask1*gt-np.nanmean(mask1*gt))-(mask1*itrp-np.nanmean(mask1*itrp)))**2)/np.nanvar(mask1*gt))
    def AEscore(gt,itrp):
        return 100*(1-np.nanmean(((gt-np.nanmean(gt))-(itrp-np.nanmean(itrp)))**2)/np.nanvar(gt))

    ## Compute mask nadir / swot  
    if any("Obs (nadir+swot)"==s for s in labels_data):
        spatial_coverage_nadir = []
        id_obs = np.where(labels_data=="Obs (nadir+swot)")[0][0]
        OBS = list_data[id_obs]
        mask1_nadirswot             = np.where(np.isnan(OBS.flatten()),np.nan,1)
        mask2_nadirswot             = np.where(np.isnan(OBS.flatten()),1,np.nan)
    if any("Obs (nadir)"==s for s in labels_data):
        spatial_coverage_nadir = []
        id_obs = np.where(labels_data=="Obs (nadir)")[0][0]
        OBS = list_data[id_obs]
        mask1_nadir                 = np.where(np.isnan(OBS).flatten(),np.nan,1)
        mask2_nadir                 = np.where(np.isnan(OBS.flatten()),1,np.nan)

    # Compute R/I/AE scores
    id1=np.where(["GT" not in l for l in labels_data ])[0]
    id2=np.where(["Obs" not in l for l in labels_data ])[0]
    id_plot=np.intersect1d(id1,id2)
    tab_scores = np.zeros((len(labels_data[id_plot]),3))
    for i in range(len(labels_data[id_plot])):
        meth_i=list_data[id_plot[i]]
        print(labels_data[id_plot[i]])
        if ("nadir+swot" in labels_data[id_plot[i]]):
            tab_scores[i,0] = Rscore(mask1_nadirswot,GT.flatten()-lr,meth_i.flatten()-lr)
            tab_scores[i,1] = Iscore(mask2_nadirswot,GT.flatten()-lr,meth_i.flatten()-lr)
        else:
            tab_scores[i,0] = Rscore(mask1_nadir,GT.flatten()-lr,meth_i.flatten()-lr)
            tab_scores[i,1] = Rscore(mask2_nadir,GT.flatten()-lr,meth_i.flatten()-lr)
        if ("rec" in labels_data[id_plot[i]]):
            tab_scores[i,2] = AEscore(GT.flatten()-lr,meth_i.flatten()-lr)
        else:
            tab_scores[i,2] = np.nan
    np.savetxt(fname=resfile,X=tab_scores,fmt='%2.2f')

