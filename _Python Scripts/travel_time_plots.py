# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 19:40:07 2020

@author: Britton.Hammit
"""

import os, glob
import pandas as pd
import matplotlib.pyplot as plt
import warnings

def Travel_Time_Plots(TT_ylim, results_path): # NOTE - ONLY WORKS IF MULTIPLE TT SEGMENT TIME PERIODS

    warnings.filterwarnings("ignore")  # Eventually get rid of this if we get rid of the warnings.    

    save_path = results_path+"\TT_Plots"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ### Vissim Travel Time Results ###
    f_vissim_tt = glob.glob(os.path.join(results_path+"\ATT_Files",'*TravTime*.att'))[0]
    s_simrun = '$VEHICLETRAVELTIMEMEASUREMENTEVALUATION:SIMRUN'
    s_msmtnum = r'VEHICLETRAVELTIMEMEASUREMENT\NO'
    s_msmtname = r'VEHICLETRAVELTIMEMEASUREMENT\NAME'
    s_timeint = 'TIMEINT'
    s_msmt = 'TRAVTM(ALL)'
    
    # Determine Header Row (Line after the last asterisk)
    i=0
    with open(f_vissim_tt) as f:
        for line in f:
           if ":SIMRUN" in line: # indicator of header row
                break
           else:
                i+=1
    # Open file based on identified header row i
    df_vissim_tt = pd.read_csv(f_vissim_tt,sep=";", header=i, dtype={s_simrun:str})
    del i
    
    # Convert Time interval into just the starting time for plotting
    def convert_timeint(series): 
        return float(series[s_timeint].split('-')[0])
    df_vissim_tt['TimePeriodStart'] = df_vissim_tt.apply(lambda series: convert_timeint(series),axis=1)
    
    # Plot Travel Time Results by Segment for each Seed
    l_tt_segs = df_vissim_tt[s_msmtnum].unique() # List of travel time segments
    l_simruns = list(df_vissim_tt[s_simrun].unique())  # List of simulation runs (includes AVE/STDEV)
    l_simruns = filter(lambda val: str(val).isnumeric(), l_simruns)  # Filter out AVE/STDEV
    
    d_colors = {'1':'tab:blue','2':'tab:orange','3':'tab:green','4':'tab:red','5':'tab:purple',
                '6':'tab:brown','7':'tab:pink','8':'tab:gray','9':'tab:olive','10':'tab:cyan'}
    d_seeds = {'1':'100','2':'101','3':'102','4':'103','5':'104',
                '6':'105','7':'106','8':'107','9':'108','10':'109'}
    # Individual Plots
    for tt_seg in l_tt_segs:
        fig, ax=plt.subplots()
        df_ = df_vissim_tt[(df_vissim_tt[s_msmtnum]==tt_seg)&(df_vissim_tt[s_simrun].str.isnumeric())] # If AVG/STD in Results
        for key, grp in df_.groupby([s_simrun],sort=False):   
            ax=grp.plot(ax=ax, kind='line', x='TimePeriodStart',y=s_msmt,label=d_seeds[key],color=d_colors[key],ylim=(0,TT_ylim))
        ax.set_title(grp[s_msmtname].unique()[0])
        try: fig.savefig(os.path.join(save_path,grp[s_msmtname].unique()[0]+'.png'))
        except: pass

def main():
    results_path = r'K:\NVA_Transit\110293002_Benning_Streetcar\Production\2b_Traffic\VISSIM\04-MOT\01_Phase 1\PM\05-Outputs\v17'
    TT_ylim=2000
    Travel_Time_Plots(TT_ylim, results_path)

if __name__ == "__main__":
    main()

""" Next Steps
* key for the seeds (would have to come from simulation results file - could hard code for now)
* set up formatting for plots (y-axis limits, axis titles, data labels)
* subplot designs specifically for K Street
* save figures to desktop
* computations from the "Sample Size Tool" for all possible TT segments and time periods to highlight trouble areas
* ^^ Much better gridlock check based on travel times.
* Calculate the Coefficient of Varienace

    # Subplots
    
    fig = plt.figure()
    i=1
    for tt_seg in l_tt_segs:
        df_ = df_vissim_tt[(df_vissim_tt[s_msmtnum]==tt_seg)&(df_vissim_tt[s_simrun].str.isnumeric())] # If AVG/STD in Results
        ax=fig.add_subplot(3,3,i)
        for key, grp in df_.groupby([s_simrun],sort=False):   
            ax=grp.plot(ax=ax, kind='line', x='TimePeriodStart',y=s_msmt,c=key,label=key,color=d_colors[key])
        ax.set_title(grp[s_msmtname].unique()[0])
        i+=1
    del i
"""