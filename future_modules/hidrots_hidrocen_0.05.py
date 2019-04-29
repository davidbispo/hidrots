# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 12:17:48 2018

@author: David Bispo Ferreira // Federal University of Parana
"""
import numpy as np
import matplotlib.pyplot as plt

monthly_file = r'D:/OneDrive/JZ_mensais.txt'
annual_file = r'D:/OneDrive/JZ_sint_anual.txt'

def fromfile(fileinput):
    from_file = open(fileinput, 'r')
    series = from_file.readlines()
    vazoes = []

    for linha in series:
        keys = linha.split() 
        vazoes.append(keys)
    return vazoes
    from_file.close()  

def gethid_sen(monthly_file, annual_file):

    monthly_series = fromfile(monthly_file)
    monthly_series_size = np.shape(monthly_series)
    monthly_array = np.array(monthly_series, dtype = float)

    annual_series = fromfile(annual_file)
    annual_series_size = np.shape(annual_series)
    annual_array = np.array(annual_series, dtype = float)

    monthly_means = np.mean(monthly_array, axis=0).reshape(1,84)
    ch = monthly_array/monthly_means
######################FIRST COLLUMN - FIRST RANDOM YEAR#####################################
    sorteio1 = np.random.randint(0,83,1)
    year1 = ch[:,sorteio1] * annual_array[0,0]
    sint_flows = np.concatenate(year1)
######################FIND MINIMUM RATIO VALUES BETWEEN YEARS###############################
    monthly_means_fst = monthly_array[0,1:83]
    monthly_means_lst = monthly_array[11,0:82]

    prev_q_ratio_fst = monthly_means_fst/monthly_means_lst
    max_prev_q_ratio = np.max(prev_q_ratio_fst)
    min_prev_q_ratio = np.min(prev_q_ratio_fst)

    raffle_array = np.random.permutation(monthly_series_size[1]).reshape(1,monthly_series_size[1])
    ch_cand = ch[:,raffle_array].reshape(12,monthly_series_size[1])
        
    qcand = ch_cand * annual_array[2,0]
    lst_fst = year1[11]
    candidate_array = qcand[0,0:].reshape(1,84)
    prev_ratio_can = candidate_array/lst_fst

    for n in range(83):
        if prev_ratio_can[0,n] > min_prev_q_ratio and prev_ratio_can[0,n] < max_prev_q_ratio:
            ch_chosen = qcand[:,n]
        break
    sint_flows = np.hstack([sint_flows, ch_chosen]).reshape(12,2)
    for l in range(2, annual_series_size[1]): # gets the number of input years for the number of series to be generated
        raffle_array = np.random.permutation(monthly_series_size[1]).reshape(1,monthly_series_size[1])
        ch_cand = ch[:,raffle_array].reshape(12,monthly_series_size[1])
        qcand = ch_cand * annual_array[0,l]
        lst_lst = sint_flows[11,(l-1)]
        candidate_array = qcand[0,0:].reshape(1,84)
        prev_ratio_can = candidate_array/lst_lst
        for n in range(monthly_series_size[1]-1):
            if prev_ratio_can[0,n] > min_prev_q_ratio and prev_ratio_can[0,n] < max_prev_q_ratio:
                q_chosen = qcand[:,n].reshape(12,1)
                break
        sint_flows = np.concatenate([sint_flows, q_chosen], axis = 1)

    datelist = np.arange(np.size(sint_flows))
    synt_flows_plot_array = sint_flows.reshape((np.size(sint_flows)),1)
    
    plt.plot(datelist,synt_flows_plot_array, label = 'Synthetic Monthly series')
    plt.xlim(0, annual_series_size[1]*12)
    plt.grid()
    plt.title('Synthetic series - Hydrologic Scenarios method')
    plt.legend(loc = 'best')
    plt.xlabel('Months')
    plt.ylabel('Flow(cms)')
    plt.show()
    
    #CHECK IF IT WORKS !!!!!!!###
	#DO FOR ALL YEARS INPUTTED#

gethid_sen(monthly_file, annual_file)