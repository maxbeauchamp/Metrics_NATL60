from pathlib import Path

from Metrics_NATL60 import *
import pandas as pd
def nRMSE_scores(list_data,labels_data,resfile,gradient=False,XP=1):

    # select only 10-day windows
    if XP==1:
    	index=list(range(5,16))
    	index.extend(range(25,36))
    	index.extend(range(45,56))
    	index.extend(range(65,76))
    else:
    	index=list(range(5,16))
    	

    GT  = list_data[0][index]

    # Compute nRMSE scores
    id1=np.where(["GT" not in l for l in labels_data ])[0]
    id2=np.where(["Obs" not in l for l in labels_data ])[0]
    id_plot=np.intersect1d(id1,id2)
    scores = []
    for i, label in enumerate(labels_data[id_plot]):
        meth_i=list_data[id_plot[i]][index]
        print(labels_data[id_plot[i]])
        nRMSE=[]
        MSE = []
        for j in range(len(meth_i)):
            if gradient==False:
                nRMSE.append((np.sqrt(np.nanmean(((GT[j]-np.nanmean(GT[j]))-(meth_i[j]-np.nanmean(meth_i[j])))**2)))/np.nanstd(GT[j]))
                MSE.append(np.nanmean(((GT[j]-np.nanmean(GT[j]))-(meth_i[j]-np.nanmean(meth_i[j])))**2))
            else:
                nRMSE.append((np.sqrt(np.nanmean(((Gradient(GT[j],2)-np.nanmean(Gradient(GT[j],2)))-(Gradient(meth_i[j],2)-np.nanmean(Gradient(meth_i[j],2))))**2)))/np.nanstd(Gradient(GT[j],2)))
                MSE.append(np.nanmean(((Gradient(GT[j],2)-np.nanmean(Gradient(GT[j],2)))-(Gradient(meth_i[j],2)-np.nanmean(Gradient(meth_i[j],2))))**2))
        scores.append(
            {
                'label': label,
                'mean_mse': np.nanmean(MSE),
                'mean_rmse': np.nanmean(nRMSE),
                '5_perc_rmse': np.percentile(nRMSE,5),
                '95_perc_rmse': np.percentile(nRMSE,95),
            }
        )
    print(resfile)
    print(pd.DataFrame(scores).to_markdown())
    with open(resfile, 'w') as f:
        pd.DataFrame(scores).set_index('label').to_markdown(f)


