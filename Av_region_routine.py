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
from uncertainties import ufloat
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
    l_deg = options[1] # deg
    b_deg = options[2] # deg
    #num_yso = int(options[3]) # number
    #num_i = int(options[4]) # number
    #num_f = int(options[5]) # number
    u_avg_yso_lt = ufloat(
        float(options[6]),
        float(options[7])
    ) # Myr
    u_avg_class_i_yso_lt = ufloat(
        float(options[8]),
        float(options[9])
    )   # Myr
    #avg_class_f_yso_lt = float(options[10])   # Myr
    u_avg_class_f_yso_lt = ufloat(
        float(options[10]),
        float(options[11])
    )   # Myr
    u_avg_yso_mass = ufloat(
        float(options[12]),
        float(options[13])
    )   # Msun
    #u_cloud_mass = ufloat(
    #    float(options[14]),
    #    float(options[15])
    #)   # Msun
    #cloud_area_deg2 = float(options[16])   # deg^2
    #u_avg_cloud_distance = ufloat(
    #    float(options[17]),
    #    float(options[18])
    #)   # kpc 
    #Av_threshold = options[19] # mag
    comments = options[20]
    # Load mass
    # Av_range, mask_area_deg2, mask_area_pc2, dust_mass_Msun, distance
    Av_region_mass = np.load(Av_region_mass_name)
    # Load YSO
    # Av_range, YSO_num, class_I_yso_num, class_Flat_YSO_num
    Av_region_yso = np.load(Av_region_yso_name)
    #-----------------------------------
    # Calculate the SFR-gas relation for each Av range.
    for i, Av_mass in enumerate(Av_region_mass):
        aa.show_string()
        string_array = np.array(aa.s)
        # Update the string array by Av ranged data
        string_array[1] = region_name
        string_array[3] = l_deg
        string_array[5] = b_deg 
        string_array[10] = Av_region_yso[i,1]
        string_array[12] = Av_region_yso[i,2]
        string_array[14] = Av_region_yso[i,3]
        string_array[16] = u_avg_yso_lt.n
        string_array[17] = u_avg_yso_lt.s
        string_array[19] = u_avg_class_i_yso_lt.n
        string_array[20] = u_avg_class_i_yso_lt.s
        string_array[22] = u_avg_class_f_yso_lt.n
        string_array[23] = u_avg_class_f_yso_lt.s
        string_array[25] = u_avg_yso_mass.n
        string_array[26] = u_avg_yso_mass.s
        string_array[31] = float(Av_region_mass[i, 3].n) * 100
        string_array[32] = float(Av_region_mass[i, 3].s) * 100
        string_array[34] = Av_region_mass[i, 1]
        string_array[36] = Av_region_mass[i, 4].n 
        string_array[37] = Av_region_mass[i, 4].s 
        string_array[39] = Av_region_yso[i,0]
        string_array[44] = comments
        # Save the string array
        np.savetxt("string_array.txt", string_array, fmt = '%s')
        # call calc_Av_region_paras.py to estimate SFR-gas relation
        system('calc_Av_region_paras.py string_array.txt')
        # Rename the result file from calc_Av_region_paras.py
        new_result_name = "{0}_{1}".format(string_array[1], i)
        cmd = 'mv input_for_calc_SF_paras_{0}.txt input_for_calc_SF_paras_{1}.txt'.format(
            string_array[1], new_result_name)
        system(cmd)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
