# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 12:17:48 2018
Description: Program for time series analysis. It has 3 modules

    1) getts: Fetches a csv or txt file to a pandas dataframe, given date limits. 
    2) hsprinter: Prints the dataframe to a pre-loaded matplotlib figure. Plots single or multiple rainfall/flow series
    3) missingreport: Prints on a pre-loaded matplotlib figure the periods where the data exists
    4) sep_stright: Prints on a pre-loaded matplotlib figure the baseflow hydrograph using the straight 
       line method. It uses a nx2 dataframe. Series can have any timestep.
@author: David Bispo Ferreira // Federal University of Parana
"""

import matplotlib.pyplot as plt
import pandas as pd
import datetime
import math
import numpy as np 
import sys
import os

####################################   TIME SERIES PARSING   ############################

def getts (filename, index_col, indexparse, separator, limits):
    """
    Gets a timeseries in a Pandas dataframe. The module uses date parsing based on collumn names. 
    Module arguments are:
        1. An input file adress(preferably passed as  raw string) as String
        2. The name of the index collumn for the dataframe as String
        3. The name of the index collumn for date parsing as String in List. It is not mandatory, but any functions that depend on sorting
        will not work if you don't provide a value
        4. The separator in the list as String
        Separator values are usually commas(','), tabs or even spaces. A good way to do your files is using
        a spreadsheet application(i.e.: MS Excel(r))
        5. The lower limits to be fetched by the application. The input must be a Python datetime Object. If you don't know what
        that is, I suggest you look it up
        6. The lower limits to be fetched by the application. Same thing from (5) applies.
        """    
    try:
        data_df = pd.read_csv(filename, index_col = index_col, sep = separator , parse_dates = indexparse, infer_datetime_format = True)
        data_df = data_df.loc['%s'%(limits[0]):'%s'%(limits[1])]
        return data_df
    except KeyError:
       print "Warning","Your keys are incorrect. Please review your csv file."
       
def test_getts():
    """Tests the getts function, by calling a pre-loaded file, and verifying the values in certain rows and collumns
    Make sure you change the current working folder to the folder containing the test files"""
    current_folder = os.getcwd()
    test_folder = 'test'
    filename = r'Planilha_mestra_geral_v1.csv'
    almost_filepath = os.path.join(current_folder, test_folder)
    filepath = os.path.join(almost_filepath, filename)
    limits = [datetime.date(2000, 1, 1),datetime.date(2016, 12, 31)]
    data_df = getts (filename = filepath, index_col = 'Datahora', indexparse = ['Datahora'], separator = ',', limits= limits)
    item = data_df.loc[datetime.date(2012,6,18)]
    success = item['Simepar'] == 17.
    msg = """Your getts module is not working properly. Make sure you did not modified the test file. If you did not,
    contact the developer or get a stable copy of the program"""
    assert success, msg



####################################HYDROLOGICAL SERIES PRINTER ############################
    
    
       
def hsprinter (data_df, flow_list, rainfall_list, output = '', print_tofile = True, dpi = 600, size = (30,10)):
    """Prints a set of time series using matplotlib. Flow values are printed normally. rainfalll values are printed upside-down.
    A legend and title are also printed. It uses as inputs:
        1)A Pandas DataFrame - See the getts() module for help
        2)A list containing strings with flow collumn indexes you want plotted in your dataframe as string
        3)A list with the names of collumns to be fetched and printed as string
        4)A fileadress to save the result of the plot. Currently the pictures are saved in 600 dpi in a 10in x 30 in frame.
        5)An optional dpi value(standard = 600 dpi)
        6)A tuple containing values of width and height in inches(standard = (30,10))
    """
    datelist = data_df.index.tolist()
    
    colorflow = ['red', 'blue', 'gray', 'cyan']
    colorrfall = ['purple', 'green', 'yellow', 'orange', 'black', 'navy', 'brown','red']
    
    flow = []
    for i in flow_list:
        fltemp = data_df[i].tolist()
        flow.append(fltemp) 
        
    rfall = []
    for i in rainfall_list:
        rftemp = data_df[i].tolist()
        rfall.append(rftemp) 
    
    fig = plt.figure(figsize = (30,10))
    ax1 = fig.add_subplot(212)
       
    for index in range(len(flow_list)):
        ax1.plot_date(x = datelist , y = flow[index], linestyle='solid', marker='None', 
                      label = flow_list[index], xdate = True, color = colorflow[index] , linewidth=0.2, alpha=0.7)
    ax1.set_ylabel('Vazao (m3/s)')
    fig_limit = data_df.index.tolist()
    fig_limits_lower = fig_limit[1]
    fig_limits_upper = fig_limit[-1]
    ax1.set_xlim(fig_limits_lower, fig_limits_upper)
    ax1.grid()
    ax1.legend()
    ax1.tick_params(axis='x',\
    which='both',      # both major and minor ticks are affected
    top='off')         # ticks along the top edge are off    
    
    ax2 = fig.add_subplot(211, sharex = ax1)
    
    for index in range(len(rainfall_list)):
        ax2.plot_date(x = datelist , y = rfall[index], linestyle='solid', marker='None', 
                      label = rainfall_list[index], xdate = True, color = colorrfall[index], linewidth=0.2, alpha=0.7)
    ax2.legend()
    ax2.set_ylabel('Precipitacao (mm)')
    plt.gca().invert_yaxis()
    fig_limit = data_df.index.tolist()
    fig_limits_lower = fig_limit[1]
    fig_limits_upper = fig_limit[-1]
    ax2.set_xlim(fig_limits_lower, fig_limits_upper)
    ax2.grid()
    ax1.legend()
    ax2.tick_params(axis='x',\
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.yaxis.set_ticks_position('left')
    plt.subplots_adjust(hspace=.0)
    
    plt.setp(ax2.get_xticklabels(), visible=False)
    if print_tofile == True:
        plt.savefig(output,format = 'png', dpi = dpi)
    plt.show()    

####################################HYDROLOGICAL SERIES PRINTER - TEST ###########################


def test_hsprinter():
    """
    Tests the ts printer function with a pre-loaded time series. The main goal here is to see if the 
    printing will work. MatplotLib does not save a file if one of the lines did not work(i.e.:it did not 
    parsed a axe title). Running the test will save a figure to the current working directory. If it does 
    not work, you should obtain a new copy of the program or contact the developer
    """
    import os
    cwd = os.getcwd()
    test_folder = os.path.join(cwd,'test')
    fileinput = os.path.join(test_folder, 'Planilha_mestra_geral_v1.csv') #Example. should be with the install folder
    output = os.path.join(test_folder, 'series_output.png')
    limits = [datetime.date(2000, 1, 1),datetime.date(2016, 12, 31)]
    flowlist = ['65019700_cax', '65019675_stq', 'Tmd_vaz']
    rflist = ['2549107']
    data_df = getts(fileinput, index_col = 'Datahora', indexparse = ['Datahora'], separator = ',', limits = limits)
    hsprinter (data_df, flowlist, rflist, output = output, print_tofile = True, dpi = 600, size = (30,10))
    success = os.path.isfile(output) == True
    
    msg = """Your missing report module is not printing to a file. Please verify the code. Preferably,
    obtain a stable version of the program or contact the developer"""
    assert success, msg


###################################################MISSING DATA VERIFIER##################################
    
    
    
def missingreport (data_df, flow_list, rainfall_list, output = '', printfig = True, output_flaw = '', dpi = 600, figsize=(20,10)):
    """Prints a missing report figure, showing flaw periods within the DataFrame Limits. Oprtionally
    prints to a file. Is this is the case, an output adress must be provided
    Arguments:
        data_df : A pandas dataframe(refer to getts() function)
        flow_list: A list containing the headers of flow collumns which the user wants plotted
        rainfalll_list: A list containing the headers of rainfalll collumns which the user wants plotted
        printfig : A boolean for printing an output file
        output : A string with the output folder and file
    """
    k = 0
    plt.ion()
    datelist = data_df.index.tolist()
    colorflow = ['red', 'blue', 'green', 'cyan', 'gold', 'tomato', 'steelblue', 'coral', 'sandybrown', 'goldenrod']
    colorrfall = ['purple', 'orange', 'darkmagenta', 'navy', 'slategray', 'black','mediumblue','fuchsia', 'navy', 'brown']
    
    flow = []
    for i in flow_list:
        global k
        k = k+1
        fltemp = data_df[i].tolist()
        for j in range(len(fltemp)):
            if math.isnan(float(fltemp[j])) == False:
                fltemp[j] = k
        flow.append(fltemp) 
            
    rfall = []
    
    for i in rainfall_list:
        global k
        k = k+1
        rftemp = data_df[i].tolist()
        for j in range(len(rftemp)):
            if math.isnan(float(rftemp[j])) == False:
                rftemp[j] = k
        rfall.append(rftemp) 
        
    fig, ax = plt.subplots(figsize=figsize, dpi = dpi)          
       
    for index in range(len(flow)):
        ax.plot_date(x = datelist , y = flow[index], linestyle='solid', marker='None', 
                      label = flow_list[index], xdate = True, color = colorflow[index] , linewidth=6)
  
    for index in range(len(rfall)):
        ax.plot_date(x = datelist , y = rfall[index], linestyle='solid', marker='None', 
                      label = rainfall_list[index], xdate = True, color = colorrfall[index] , linewidth=6)
    ax.set_ylabel('Vazao (m3/s)')
    fig_limit = data_df.index.tolist()
    fig_limits_lower = fig_limit[1]
    fig_limits_upper = fig_limit[-1]
    ax.set_xlim(fig_limits_lower, fig_limits_upper)
    ax.get_yaxis().set_visible(False)
    
                 
    ax.grid(b=True, which = 'major', linewidth = 0.7)
    ax.grid(b=True, which = 'minor', linewidth = 0.1, color = 'black')
    plt.title('Flaw report', y = 1.0)
    plt.legend(loc='lower left', bbox_to_anchor=(-0.1115,0))
    
#OUTPUT#
    if printfig == True:
        plt.savefig(output, dpi = dpi)
    
    plt.show()
        
#####################################   MISSING DATA REPORT - TEST ######################
    
    
    
def test_missingreport():
    """Tests the missing report function with a known set of values. The main goal is to see if a 
    file as saved to the current working folder. Since MatplotLib does not save a file unless all
    the lines are parsed, it is not working properly if the file is not saved. If any of 
    the printed series is different from the model, you should contact the developer or obtain a
    stable version of the program"""
    cwd = os.getcwd()
    flowlist = ['65019700_cax', '65019675_stq', 'Tmd_vaz']
    rflist = ['2549080', '2549080','2549081','2549100','Simepar', '2549107']
    limits = [datetime.date(2000, 1, 1),datetime.date(2016, 12, 31)]
    test_folder = os.path.join(cwd,r'test')
    fileinput_sep = os.path.join(test_folder,'Planilha_mestra_geral_v1.csv')
    output = os.path.join(test_folder,'output_flaw.png')
    data_df = getts(fileinput_sep, index_col = 'Datahora', separator = ',', indexparse = ['Datahora'], limits = limits) 
    output = os.path.join(test_folder,'output_flaw.jpg')
    missingreport(data_df,flowlist,rflist,output = output,printfig = True, dpi = 300)
    success = os.path.isfile(output) == True
    
    msg = """Your missing report module is not printing to a file. Please verify the code. Preferably,
    obtain a stable version of the program or contact the developer"""
    assert success, msg
    
######################################RUNOFF SEP - STRAIGHT LINE METHOD#############
    
    
    
    
def sep_straight(data_df, event_datelist, FLOWFieldName, output):
    """
    Returns two values: maximum flow and the total runoff in in an event. It also 
    prints a report, containing the flow series, and returns the total volume 
    along in an event.
    
    The dates you enter dictate tha starting and ending point. In other words, it's the user
    that selects them, so it's recommended that you have a first guess of such limits. 
    Suggestion: Use hsprinter() from this module.
    
    The volume is obtained through the straight line method. It connects the endpoint with the
    starting point. Total volume is calculated by integration. FLOW Values must be in cms. The
    function requires:
        1. A Pandas DataFrame - Using getts is suggested as String
        2. List of dates - A list with dates in the Python datetime.datetime format. Only two values 
        are requires: Start date and end date(suggestion: use datetime.datetime) as String
        3. The name of the field to be taken into consideration for runoff separation
        4. An output string with the location and format of the printed figure."""
    
#VERIFICATIONS FOR CONSISTENCY OF ARGUMENTS#
    try:
        len(event_datelist) != 2
    except:
        print """Your list of dates does not has 2 elements. Please fix that. A good way 
        to get what you need from getts is to slice a dataframe with 
        data_df2 = data_df['collumn_name']"""
        sys.exit(1)
    
    
    try: 
        a = event_datelist[0]
        b = event_datelist[1]
        isinstance(a, datetime.datetime) == True
        isinstance(b, datetime.datetime) == True
    except:
        print """Your dates do not have the datetime format. Please convert them before preceeding"""
        sys.exit(1)
        
        
#BASIC COMPUTATIONS FOR THE STRAIGHT LINE METHOD#
    data_df_limited = data_df.loc['%s'%(event_datelist[0]):'%s'%(event_datelist[1])]
    flow_start_row = data_df_limited.iloc[0]
    flow_start = flow_start_row['%s' % (FLOWFieldName)]
    flow_end_row = data_df_limited.iloc[-1]
    flow_end = flow_end_row['%s' % (FLOWFieldName)]
    delta_t = event_datelist[1]-event_datelist[0]
    delta_t = delta_t.total_seconds()
    
##STRAIGHT LINE METHOD#
    flow_obs_lim = data_df_limited['%s' % (FLOWFieldName)].tolist()
    m = (flow_end-flow_start)/(len(flow_obs_lim))
    x = np.arange(0,len(flow_obs_lim))
    y0 = np.zeros(len(flow_obs_lim)) + flow_start
    x = np.arange(0,len(flow_obs_lim))
    vaz_sub = y0 + m*x
    difference = flow_obs_lim-vaz_sub
    sumdif = np.sum(difference)
    vol = sumdif * len(flow_obs_lim)
    
#PLOTTING#
    datelist = data_df.index.tolist()
    fig = plt.figure(figsize = (30,10))
    ax = plt.gca()
    flow_obs = data_df[FLOWFieldName].tolist()
    datelist_sub = data_df_limited.index.tolist()
    
    plt.plot_date(x = datelist , y = flow_obs, 
             linestyle='solid', marker='None', label = 'Observed Flow', xdate = True, color = 'blue' , linewidth=1)
    plt.plot_date(x = datelist_sub , y = vaz_sub, 
             linestyle='solid', marker='None', label = 'Separated Flow', xdate = True, color = 'red' , linewidth=1)
    ax.set_ylabel('Flow (cms)', fontsize=16)
    ax.set_xlabel('Date', fontsize=16)
    fig_limit = data_df.index.tolist()
    fig_limits_lower = fig_limit[1]
    fig_limits_upper = fig_limit[-1]
    ax.set_xlim(fig_limits_lower, fig_limits_upper)
    ax.grid()
    ax.legend()
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    ax.annotate('The total runoff volume is %.3f \n cms for this event' % (vol)
                , xy= (0.8,0.75), xytext=(0.8, 0.75), xycoords='figure fraction', bbox=bbox_props)
    plt.title('Separated Runuff - Straight Line method', fontsize=20)
    fig.autofmt_xdate()
    plt.savefig(output)
    plt.show()
    return vol


#########################   RUNOFFF SEPARATOR - TEST FUNCTION   ###############################
def test_sep_straight():
    """Tests the function of runoff separation in an event. The functions tests the results
    of an event between 1/9/2016 18:00 to 1/23/2016 at 23:00. Case the function return an expected value,
    no value is printed. Also, the graphic is plotted for evaluation and matplotlib library functionality"""
    
    limits = [datetime.datetime(2016, 1, 9, 18),datetime.datetime(2016, 1, 23, 23)]

    event_duration = [datetime.datetime(2016, 1, 9, 19),datetime.datetime(2016, 1, 18, 20, 01),]
    cwd = os.getcwd()
    test_folder = os.path.join(cwd,r'test')
    fileinput_str = os.path.join(test_folder,'tamandare_2016.csv')
    saida = os.path.join(test_folder,'sep_fig.png')
    data_df = getts(fileinput_str, index_col = 'Datahora', indexparse = ['Datahora'], separator = ',', limits = limits)
    calculated = sep_straight(data_df,event_duration, FLOWFieldName = 'Vazao', output = saida)
    expected = 24909909
    success = calculated - expected < 5
    
    msg = """calculated %s, expected %s. Values for total runoff are not
    the same. Please contact the Administrator or obtain a stable version""" % (calculated, expected)
    assert success, msg
    
############################   FUNCTION CALLERS    ############################################

filename = r'C:\Users\david\Desktop\hidrots_1.0\test\Planilha_mestra_geral_v1.csv'
limits = [datetime.date(2000, 1, 1),datetime.date(2016, 12, 31)]
data_df = getts (filename = filename, index_col = 'Datahora', indexparse = ['Datahora'], separator = ',', limits= limits)
#test_getts()

#flowlist = ['65019700_cax', '65019675_stq', 'Tmd_vaz']
#rflist = ['2549077' , '2549080', '2549081','2549100','Simepar', '2549107']
#hsprinter(data_df,flowlist, rflist, output = r'C:\Users\david\Desktop\hidrots_1.0\hs_print.png', print_tofile = True, dpi = 600)
#test_hsprinter()
    
flowlist = ['65019700_cax', '65019675_stq', 'Tmd_vaz']
rflist = ['2549077' , '2549080', '2549081','2549100','Simepar', '2549107']
output_flaw = r'C:\Users\david\Desktop\hidrots_1.0\output_flaw.png'
missingreport (data_df, flow_list = flowlist, rainfall_list=rflist, output = 'output_flaw.png', printfig = True, output_flaw = output_flaw, dpi = 600, figsize=(16,8))
#test_missingreport()


#############
    
    
#event_duration = [datetime.datetime(2016, 8, 17, 13),datetime.datetime(2016, 8, 28, 11)]
#fileinput_sep = r'C:\Users\david\Desktop\hidrots_1.0\test\tamandare_2016.csv'
#limits = [datetime.datetime(2016, 8, 17, 5),datetime.datetime(2016, 8, 29, 1)]
#saida = r'C:\Users\david\Desktop\hidrots_1.0\runoff_sep_plot.png'
#data_df = getts(fileinput_sep, index_col = 'Datahora', indexparse = ['Datahora'], separator = ',', limits = limits )
#sep_straight(data_df,event_duration, FLOWFieldName = 'Vazao', output = saida)
#test_sep_straight()

    
 
