# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:05:29 2020

@author: Britton.Hammit
"""

import os, glob, shutil, time

def Clean_Output_Files(results_path, no_seeds):

    d_att_ends = {1:'*001.att',2:'*002.att',3:'*003.att',4:'*004.att',5:'*005.att',
                    6:'*006.att',7:'*007.att',8:'*008.att',9:'*009.att',10:'*010.att'}
    d_txt_ends = {1:'*001.txt',2:'*002.txt',3:'*003.txt',4:'*004.txt',5:'*005.txt',
                    6:'*006.txt',7:'*007.txt',8:'*008.txt',9:'*009.txt',10:'*010.txt'}
    
    # Change final file to txt file
    l_file_names = glob.glob(os.path.join(results_path,d_att_ends[no_seeds]))
    for fn in l_file_names:
        os.rename(fn, fn[:-4] + '.txt')
    
    # Delete other ATT files
    l_file_names = glob.glob(os.path.join(results_path,'*.att'))
    for fn in l_file_names:
        os.remove(fn)
    
    # Change final files back to ATT
    l_file_names = glob.glob(os.path.join(results_path,d_txt_ends[no_seeds]))
    for fn in l_file_names:
        os.rename(fn, fn[:-4] + '.att')
        
    # Move Output Files into special folder
    save_path = results_path+"\ATT_Files"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    l_file_names = glob.glob(os.path.join(results_path,'*.att'))
    for fn in l_file_names:
        fn = os.path.basename(fn)
        shutil.move("{}/{}".format(results_path,fn), "{}/{}".format(save_path,fn))

    time.sleep(60)  # Wait loop for files to move folders
    
    # Shorten Vehicle Network Performance File
    fn = glob.glob(os.path.join(save_path,'*Vehicle Network Performance Evaluation Results*'))[0]
    os.rename(fn,fn.replace('Vehicle Network Performance Evaluation Results', 'Veh Network Perf'))
    #os.remove(fn)
    
    # Shorten Data Collection Point Performance File
    fn = glob.glob(os.path.join(save_path,'*Data Collection Results*'))[0]
    os.rename(fn,fn.replace('Data Collection Results', 'DCM'))
    
    # Shorten Travel Time Results File
    fn = glob.glob(os.path.join(save_path,'*Vehicle Travel Time Results*'))[0]
    os.rename(fn,fn.replace('Vehicle Travel Time Results', 'TravTime'))
    
    # Shorten Link Segment Results File
    fn = glob.glob(os.path.join(save_path,'*Link Segment Results*'))[0]
    os.rename(fn,fn.replace('Link Segment Results', 'Link'))
    
    # Shorten Node Results File
    fn = glob.glob(os.path.join(save_path,'*Node Results*'))[0]
    os.rename(fn,fn.replace('Node Results', 'Node'))
    
    # Shorten Queue Counters File
    fn = glob.glob(os.path.join(save_path,'*Queue Results*'))[0]
    os.rename(fn,fn.replace('Queue Results', 'Queue'))
    
    # Shorten Simulation Runs Results File
    fn = glob.glob(os.path.join(save_path,'*Simulation Runs*'))[0]
    os.rename(fn,fn.replace('Simulation Runs', 'SimRun'))

def main():
    results_path = r'K:\NVA_Transit\110293002_Benning_Streetcar\Production\2b_Traffic\VISSIM\04-MOT\01_Phase 1\AM\05-Outputs\v4test'
    no_seeds = 10
    Clean_Output_Files(results_path, no_seeds)

if __name__ == "__main__":
    main()