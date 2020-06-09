#!/usr/bin/python3
'''
Abstract:
    This is a script to generate SFR-gas relation in different extinction (Av) range
Usage:
    Av_region_routine.py [option file] [Av_region_mass] [Av_region_YSO] 
Output:
    1. The derive result saved in mysql 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200609
####################################
update log
20200609 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
import numpy as np
from sys import argv
from os import system
from input_lib import option_calc_SF_paras

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #--------------------------------------------
    # Initialization
    # Argument Assistant
    default_input_name = 'option_Av_region.txt'
    aa = option_calc_SF_paras(default_input_name)
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage: Av_region_script.py [option file] [Av_region_mass] [Av_region_YSO]") 
        aa.create()
        exit()
    option_name = argv[1]
    Av_region_mass_name = argv[2]
    Av_region_yso_name = argv[3]
    #--------------------------------------------
    # Load data
    # Load detail options from option file.
    options = aa.load(option_name)
    region_name = options[0]
    #num_yso = int(options[1]) # number
    avg_yso_age = float(options[2])   # Myr
    avg_yso_mass = float(options[3])  # Msun
    #cloud_mass = float(options[4])    # Msun
    #cloud_area_deg2 = float(options[5])   # deg^2
    avg_cloud_distance = float(options[6])    # kpc
    avg_cloud_age = float(options[7]) # Myr
    Av_threshold = float(options[8]) # mag
    comments = options[9]
    # Load mass
    # Av_range, mask_area_deg2, mask_area_pc2, dust_mass_Msun
    Av_region_mass = np.load(Av_region_mass_name)
    # Load YSO
    # Av_range, yso_num_range
    Av_region_yso = np.load(Av_region_yso_name)
    #-----------------------------------
    # Calculate the SFR-gas relation for each Av range.
    for i, Av_mass in enumerate(Av_region_mass):
        aa.show_string()
        string_array = np.array(aa.s)
        # Update the string array by Av ranged data
        string_array[1] = region_name
        string_array[6] = Av_region_yso[i,1]
        string_array[8] = avg_yso_age
        string_array[10] = avg_yso_mass
        string_array[15] = float(Av_region_mass[i, 3]) * 100
        string_array[17] = Av_region_mass[i, 1]
        string_array[19] = avg_cloud_distance
        string_array[21] = avg_cloud_age
        string_array[23] = Av_region_yso[i,0]
        string_array[28] = comments
        # Save the string array
        np.savetxt("string_array.txt", string_array, fmt = '%s')
        # call calc_SF_paras.py to estimate SFR-gas relation
        system('calc_SF_paras.py string_array.txt')
        # Rename the result file from calc_SF_paras.py
        new_result_name = "{0}_{1}".format(string_array[1], i)
        cmd = 'mv input_for_calc_SF_paras_{0}.txt input_for_calc_SF_paras_{1}.txt'.format(
            string_array[1], new_result_name)
        system(cmd)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
