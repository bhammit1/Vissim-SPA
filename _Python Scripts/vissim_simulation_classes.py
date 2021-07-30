import numpy as np
from math import sqrt
import win32com.client as com  # COM-Server
import os

class Vissim_Network:
    """
    VISSIM Simulation
    """
    def __init__(self, network_name, layout_name, network_path, save_path, layout_path, version):
        self.network_name = network_name
        self.network_path = network_path
        self.layout_name = layout_name
        self.save_path = save_path
        self.layout_path = layout_path
        self.version = version

        self.vissim = com.gencache.EnsureDispatch(version) # Vissim 11 - Connecting the COM Server => Open a new Vissim Window:
	     # Vissim = com.Dispatch("Vissim.Vissim-32.800") # Vissim 8 - 32 bit
        # Vissim = com.Dispatch("Vissim.Vissim-64.800") # Vissim 8 - 64 bit
        # Vissim = com.Dispatch("Vissim.Vissim-32.900") # Vissim 9 - 32 bit
        # Vissim = com.Dispatch("Vissim.Vissim-64.900") # Vissim 9 - 64 bit 
        # Vissim = com.gencache.EnsureDispatch("Vissim.Vissim.10") # Vissim 10 
        # Vissim = com.gencache.EnsureDispatch("Vissim.Vissim.11") # Vissim 11 
        # Vissim = com.client.Dispatch("Vissim.Vissim.900")

        # Initialize Simulation
        self.initialize_network()

    def initialize_network(self):
        ## Load a Vissim Network:
        inpx_file = os.path.join(self.network_path, self.network_name + '.inpx')
        flag_read_additionally = False  # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
        self.vissim.LoadNet(inpx_file, flag_read_additionally)

        ## Load a Layout:
        layx_file = os.path.join(self.layout_path, self.layout_name + '.layx')
        self.vissim.LoadLayout(layx_file)

    def update_layout(self,layout_name):
        ## Load a Layout:
        self.layout_name = layout_name
        layx_file = os.path.join(self.layout_path, self.layout_name + '.layx')
        self.vissim.LoadLayout(layx_file)

    def activate_quickmode(self):
        self.vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode",1)
        self.vissim.SuspendUpdateGUI()
        self.vissim.Simulation.SetAttValue('UseMaxSimSpeed',True)

    def deactivate_quickmode(self):
        self.vissim.Graphics.CurrentNetworkWindow.SetAttrValue("QuickMode",0)  # deactivate quick mode
        self.vissim.ResumeUpdateGUI()  #allow updating of the complete Vissim workspace (network editor, list, chart and signal time table windows)

    def set_number_of_runs(self,no_runs):
        self.vissim.Simulation.SetAttValue('NumRuns',no_runs)

    def set_random_seed(self,random_seed=1,increment=1):
        self.vissim.Simulation.SetAttValue('RandSeed',random_seed)
        self.vissim.Simulation.SetAttValue('RandSeedIncr',increment)
        
    def set_evaluation(self,keep_prev_results,veh_class_recording,
                       data_collection_active = False, data_collection_setup = False, data_collection_save = False,
                       node_collection_active = False, node_collection_setup = False, node_collection_save = False,
                       travel_time_collection_active = False, travel_time_collection_setup = False, travel_time_collection_save = False,
                       veh_net_performance_active = False, veh_net_performance_setup = False, veh_net_performance_save = False,
                       link_collection_active = False, link_collection_setup = False, link_collection_save = False,
                       queue_collection_active = False, queue_collection_setup = False, queue_collection_save = False,
                       autosave_after_simulation = False):
        self.vissim.Evaluation.SetAttValue('KeepPrevResults',keep_prev_results)
        #self.vissim.Evaluation.SetAttValue('VehClasses',veh_class_recording)
        #self.vissim.Evaluation.SetAttValue('ListAutoExportType', autosave_after_simulation)
        if data_collection_active is True:
            self.vissim.Evaluation.SetAttValue('DataCollCollectData',data_collection_active)
            self.vissim.Evaluation.SetAttValue('DataCollFromTime',data_collection_setup[0])
            self.vissim.Evaluation.SetAttValue('DataCollToTime',data_collection_setup[1])
            self.vissim.Evaluation.SetAttValue('DataCollInterval',data_collection_setup[2])
        if node_collection_active is True:
            self.vissim.Evaluation.SetAttValue('NodeResCollectData',node_collection_active)
            self.vissim.Evaluation.SetAttValue('NodeResFromTime',node_collection_setup[0])
            self.vissim.Evaluation.SetAttValue('NodeResToTime',node_collection_setup[1])
            self.vissim.Evaluation.SetAttValue('NodeResInterval',node_collection_setup[2])
        if travel_time_collection_active is True:
            self.vissim.Evaluation.SetAttValue('VehTravTmsCollectData',travel_time_collection_active)
            self.vissim.Evaluation.SetAttValue('VehTravTmsFromTime',travel_time_collection_setup[0])
            self.vissim.Evaluation.SetAttValue('VehTravTmsToTime',travel_time_collection_setup[1])
            self.vissim.Evaluation.SetAttValue('VehTravTmsInterval',travel_time_collection_setup[2])
        if veh_net_performance_active is True:
            self.vissim.Evaluation.SetAttValue('VehNetPerfCollectData',veh_net_performance_active)
            self.vissim.Evaluation.SetAttValue('VehNetPerfFromTime',veh_net_performance_setup[0])
            self.vissim.Evaluation.SetAttValue('VehNetPerfToTime',veh_net_performance_setup[1])
            # added interval:
            self.vissim.Evaluation.SetAttValue('VehNetPerfInterval',travel_time_collection_setup[2])
            # this was already commented:
            #self.vissim.Evaluation.SetAttValue('VehNetPerfRawWriteFile',veh_net_performance_setup[2])
        if link_collection_active is True:
            self.vissim.Evaluation.SetAttValue('LinkResCollectData',link_collection_active)
            self.vissim.Evaluation.SetAttValue('LinkResFromTime',link_collection_setup[0])
            self.vissim.Evaluation.SetAttValue('LinkResToTime',link_collection_setup[1])
            self.vissim.Evaluation.SetAttValue('LinkResInterval',link_collection_setup[2])
        if queue_collection_active is True:
            self.vissim.Evaluation.SetAttValue('QueuesCollectData',queue_collection_active)
            self.vissim.Evaluation.SetAttValue('QueuesFromTime',queue_collection_setup[0])
            self.vissim.Evaluation.SetAttValue('QueuesToTime',queue_collection_setup[1])
            self.vissim.Evaluation.SetAttValue('QueuesInterval',queue_collection_setup[2])            

    def set_run_time(self,run_time):
        """
        :param run_time: [seconds]
        """
        self.vissim.Simulation.SetAttValue('SimPeriod',run_time)

    def set_evaluation_output_directory(self,save_path):
        self.vissim.Evaluation.SetAttValue('EvalOutDir',save_path)

    def set_break_time(self,break_time):
        self.vissim.Simulation.SetAttValue('SimBreakAt',break_time)

    def set_vehicle_input(self,input_no,input_vol):
        self.vissim.Net.VehicleInputs.ItemByKey(input_no).SetAttValue('Volume({})'.format(input_no), input_vol)

    def set_vehicle_type(self,veh_comp_no,veh_type_no):
        rel_flows = self.vissim.net.VehicleCompositions.ItemByKey(veh_comp_no).VehCompRelFlows.GetAll()
        rel_flows[0].SetAttValue('VehType',veh_type_no)

    def set_desired_speed_distribution(self,veh_comp_no,des_spd_dist_no):
        rel_flows = self.vissim.net.VehicleCompositions.ItemByKey(veh_comp_no).VehCompRelFlows.GetAll()
        rel_flows[0].SetAttValue('DesSpeedDistr',des_spd_dist_no)

    def get_all_vehicles(self):
        return self.vissim.Net.Vehicles.GetAll()

    def set_driving_params(self,driving_behavior_no,cc0):
        self.vissim.DrivBehav.ItemByKey(driving_behavior_no).SetAttValue('W99cc0', cc0)

    def save_network_files(self,new_save_path=None):
        if new_save_path is None:
            inpx_file = os.path.join(self.network_path, self.network_name + '.inpx')
            layx_file = os.path.join(self.network_path, self.network_name + '.layx')
        else:
            inpx_file = os.path.join(new_save_path, self.network_name + '.inpx')
            layx_file = os.path.join(new_save_path, self.network_name + '.layx')

        self.vissim.SaveNetAs(inpx_file)
        self.vissim.SaveLayout(layx_file)

    def close(self):
        self.vissim = None

    def update_vehicle_classes(self):
        all_veh_attributes = self.vissim.Net.Vehicles.GetMultipleAttributes(('No','Length','Pos','Lane',
                                                                             'Speed','Acceleration',
                                                                             'DesSpeed','LeadVehNo',
                                                                             'Lead_Speed','Lead_Pos',
                                                                             'Lead_Len','FollDist','SpeedDiff'))

    def advance_single_timestep(self):
        self.vissim.Simulation.RunSingleStep()

    def run_complete_simulation(self):
        self.vissim.Simulation.RunContinuous()