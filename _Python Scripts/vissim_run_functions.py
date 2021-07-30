
from vissim_simulation_classes import Vissim_Network
from travel_time_plots import *
from organize_att_files import *
from run_excel_macro import *
from transit_metrics import *
import shutil, os, time


def RunVissim(fn_scenario, peak_pd, excel_scenario, fn_start, fn_end, run_vissim, copy_moe_sheet, transit_veh_records, travel_time_plots, 
                  clean_output_files, run_excel_macros, no_runs, vissim_version, sim_run_time, random_seed_start, random_seed_increment,
                  keep_prev_results, veh_class_recording, data_collection_active, data_collection_setup, node_collection_active, 
                  node_collection_setup, travel_time_collection_active, travel_time_collection_setup, veh_net_performance_active,
                  veh_net_performance_setup, link_collection_active, link_collection_setup, queue_collection_active,
                  queue_collection_setup, TT_ylim, layout_fn, layout_fn_post, open_path, save_path_start, moe_spreadsheet_fn,
                  moe_spreadsheet_path, layout_path):

           
    # =============================================================================
    # Executing Desired Functions
    # =============================================================================
    
    # Initialize Log File
    log_fn = 'calibration_logfile.txt'
    log_file = open(os.path.join(save_path_start,log_fn),'a') 
    
    # Iterative process to archive and save-over all Model files
    if run_vissim is True:
        print ("Copying over RBC and V3D Files")

        fn = fn_start + fn_end
    
        # Define the save path directory and create if needed
        save_path = save_path_start + '\{}'.format(fn_end)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        else:
            overwrite_file = input("Output folder {} already exists - do you want to overwrite it?  (Y/N):  ".format(fn))
            if overwrite_file == "N":  # End script if you don't want to overwrite the folder.
                SystemExit()
    
        # Copy RBC files and Vehicle files to Output path/Running Path
        for f_ in os.listdir(open_path):
            if f_.endswith('.rbc') or f_.endswith('.v3d'):
                shutil.copyfile(src=open_path+'\{}'.format(f_),dst=save_path+'\{}'.format(f_))
    
    # Iterative process to run model(s)

    fn = fn_start + fn_end

    start_time = time.time()
    

    print ("Starting: {} at {}".format(fn, time.asctime(time.localtime(start_time))))
    log_file.write("Starting: {} at {}".format(fn, time.asctime(time.localtime(start_time))))
    log_file.write("\n")
    
    # Define the save path directory and create if needed
    save_path = save_path_start + '\{}'.format(fn_end)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    if run_vissim is True:
        # Open Vissim
        print ("Opening Vissim")
        network = Vissim_Network(network_name=fn,layout_name=layout_fn,network_path=open_path,save_path=save_path,layout_path=layout_path,version=vissim_version)
        network.save_network_files(new_save_path=save_path)
        
        # Setup Vissim Settings
        print ("Applying Vissim Settings")
        network.set_evaluation_output_directory(save_path=save_path)
        network.activate_quickmode()
        network.set_number_of_runs(no_runs=no_runs)
        network.set_run_time(run_time=sim_run_time)
        network.set_random_seed(random_seed = random_seed_start, 
                                increment = random_seed_increment)
        network.set_evaluation(keep_prev_results = keep_prev_results,
                               veh_class_recording = veh_class_recording,
                               data_collection_active = data_collection_active, 
                               data_collection_setup = data_collection_setup,
                               node_collection_active = node_collection_active, 
                               node_collection_setup = node_collection_setup,
                               travel_time_collection_active = travel_time_collection_active, 
                               travel_time_collection_setup = travel_time_collection_setup,
                               veh_net_performance_active = veh_net_performance_active,
                               veh_net_performance_setup = veh_net_performance_setup,
                               link_collection_active = link_collection_active,
                               link_collection_setup = link_collection_setup,
                               queue_collection_active = queue_collection_active,
                               queue_collection_setup = queue_collection_setup)
        
        # Run Vissim model
        print ("Running Vissim Model")
        network.run_complete_simulation()
        network.save_network_files(new_save_path=save_path)
        network.update_layout(layout_name=layout_fn_post)
        network.close()
        print ("Vissim Model Runs Complete")
    
        time.sleep(5)  # Wait loop for Vissim to shut down

    # Copy empty MOE spreadsheet to save path
    if copy_moe_sheet is True:
        try:
            print ("Copying MOE Spreadsheet into Path")
            moe_spreadsheet_fn_new = moe_spreadsheet_fn.replace('template',"{}_{}_{}".format(fn_scenario,peak_pd,fn_end))
            
            # Check if sheet exists in folder and if it does, rename it before copying
            if os.path.exists(save_path+'\{}'.format(moe_spreadsheet_fn_new)):
                if not os.path.exists(save_path+'\!Archive'):
                    os.makedirs(save_path+'\!Archive')
                shutil.copyfile(src=save_path+'\{}'.format(moe_spreadsheet_fn_new),dst=save_path+'\!Archive'+'\{}_{}'.format(time.strftime("%Y-%m-%d_%H-%M"),moe_spreadsheet_fn_new))
            
            # Copy New File
            shutil.copyfile(src=moe_spreadsheet_path+'\{}'.format(moe_spreadsheet_fn),dst=save_path+'\{}'.format(moe_spreadsheet_fn_new))
        except:
            print("     *Error Copying Out MOE Sheet")
    
    # Clean .ATT Files (only keep the last)
    if clean_output_files is True:
        print ("Clean up folder to remove unnecessary .ATT files")
        try: Clean_Output_Files(results_path=save_path, no_seeds=no_runs)
        except:
            print("     *Error Cleaning .ATT Output Files")
            
    # Process Transit Data
    if transit_veh_records is True:
        print ("Process Transit Data - Produce Summary Spreadsheet")
        try: Transit_Data_Processing(version=fn_end, save_path=save_path, file_name_start=fn, transit_data_path=transit_data_path)
        except:
            print("     *Error Reporting Transit Data")
    
    # Process Travel Time Data
    if travel_time_plots is True:
        print ("Process Travel Time Data - Produce Travel Time Plots")
        try: Travel_Time_Plots(TT_ylim, results_path=save_path)
        except:
            print("     *Error Reporting Travel Time Plots")

    # Run MOE Sheet Macros
    if run_excel_macros is True:
        print ("Run MOE Sheet Macros to Process Results")
        try: 
            # Execute Macro to Clear all results, Toggle between AM and PM, then Process new .ATT results
            run_excel_macro(open_path=save_path, excel_name=moe_spreadsheet_fn_new, excel_scenario=excel_scenario,
                            mod1="Main", macro1="Change_Links_Python",
                            mod2="Main", macro2="Import_Results_Auto")
        except:
            print("     *Error Running MOE Sheet Macro")
    
    total_time = (time.time()-start_time)/60
    print ("Finished - {} min".format(round(total_time,1)))
    print ("")
    log_file.write("Finished - {} min".format(round(total_time,1)))
    log_file.write("\n")
    log_file.write("\n")

    log_file.close()