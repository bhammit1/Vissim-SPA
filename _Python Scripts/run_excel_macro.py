# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 07:26:15 2020

@author: Britton.Hammit
"""

"""
From Internet!
if os.path.exists("excelsheet.xlsm"):
    xl=win32com.client.Dispatch("Excel.Application")
    xl.Workbooks.Open(os.path.abspath("excelsheet.xlsm"), ReadOnly=1)
    xl.Application.Run("excelsheet.xlsm!modulename.macroname")
##    xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
    xl.Application.Quit() # Comment this out if your excel script closes
    del xl
    
if os.path.exists("excelsheet.xlsm"):
    xl=win32com.client.Dispatch("Excel.Application")
    wb = xl.Workbooks.Open(os.path.abspath("excelsheet.xlsm"), ReadOnly=1) #create a workbook object
    xl.Application.Run("excelsheet.xlsm!modulename.macroname")
    wb.Close(False) #close the work sheet object rather than quitting excel
    del wb
    del xl
"""

import os
import win32com.client

def run_excel_macro(open_path, excel_name, excel_scenario, mod1, macro1, mod2=0, macro2=0, 
                    mod3=0, macro3=0, mod4=0, macro4=0):
    f_ = os.path.join(open_path,excel_name)
    if os.path.exists(f_):
        xl=win32com.client.Dispatch("Excel.Application")
        wb = xl.Workbooks.Open(os.path.abspath(f_), ReadOnly=0)
        xl.Application.Run("{}!{}.{}".format(excel_name, mod1, macro1), excel_scenario)
        if mod2 != 0 and macro2 != 0:
            xl.Application.Run("{}!{}.{}".format(excel_name, mod2, macro2))
        if mod3 != 0 and macro3 != 0:
            xl.Application.Run("{}!{}.{}".format(excel_name, mod3, macro3))
        if mod4 != 0 and macro4 != 0:
            xl.Application.Run("{}!{}.{}".format(excel_name, mod4, macro4))  
        
        wb.Close(False)
        del xl, wb
    else:
        print(     "File Does Not Exist - Cannot Run Macro")


if __name__ == "__main__":
    open_path = r'K:\NVA_RDWY\110721000_Route1_Multimodal\Production\Task 2 - Mulitmodal Transportation Analysis\04-Vissim\01-Existing\02-AM\03-Outputs\v13'
    excel_name = 'Route1_MOEs_AM_v13.xlsb'
    mod1, mod2, mod3 = "Module1", "Module2", "Module1"
    macro1, macro2, macro3 = "ClearResultsTabs","Change_Links_Python","Import_Results_Auto"
    
    run_excel_macro(open_path, excel_name, mod1, macro1, mod2, macro2, mod3, macro3)
    