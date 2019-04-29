# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 12:17:48 2018

@author: David
"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import pandas as pd
import datetime
import numpy as np

fileinput = r'D:\OneDrive\Planilha-mestra_geral_v1.csv'
limits = [datetime.date(2010, 12, 1),datetime.date(2016, 12, 31)]
resample = False
output = r'D:\saida2.png'
boxplotout = r'D:\saida_boxplot.png'
dpi = 800
indextime = 'Datahora'
indexparse = [indextime]
flowlist = ['65019700_cax', '65019675_stq', 'Tmd_vaz']
rflist = ['2549107']
######################################CONTROL##########################
def getts (fileinput = fileinput, index_col = indextime, indexparse = indexparse, separator = ',', lower = limits[0] , 
             upper = limits[1], ):
    
    df = pd.read_csv(fileinput, index_col = indextime, sep = separator , parse_dates = indexparse, infer_datetime_format = True)
    df = df.loc['%s'%(limits[0]):'%s'%(limits[1])]
    return df
#################################PLOTTING CODE#######################
def boxplot(df, flow_list, output = output, plot_tofile = True):
    dfsample = df.dropna()
    flow_lists = []
    
    for element in flowlist:
        flow_temp = dfsample[element].tolist()
        flow_lists.append(flow_temp)
        
        fig = plt.figure(1, figsize=(16, 12))
        ax = fig.add_subplot(111)
        ax.boxplot(flow_lists)
        yticks = np.arange(0, 110, 2)
        ax.set_yticks(yticks)
        ax.set_title('Boxplot of Flows')
        ax.set_xticklabels(flowlist, rotation=45, fontsize=12)
        ax.grid(b= True)
        if plot_tofile == True:
            fig.savefig(boxplotout, bbox_inches='tight')
            fig.show()

df = getts()
boxplot(df, flowlist, output = boxplotout, plot_tofile = True)


