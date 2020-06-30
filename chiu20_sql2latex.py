#!/usr/bin/python3
'''
Abstract:
    A function to show my result using latex format 
Usage:
    chiu20_sql2mysql.py
Output:
    The image of dustmap on a given location.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200623
####################################
update log
20200623 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import numpy as np
from chiu20_mysql_lib import load2py_mq_cloud

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Initialize the database settings
    YSO_col_list = [
        '`cloud`',
        '`yso_number`',
        '`class_i_yso_number`',
        '`class_f_yso_number`',
        '`Av_threshold`',
        '`distance_pc`',
        '`e_distance_pc`',
        '`area_deg2`',
        '`area_pc2`',
        '`e_area_pc2`',
        '`cloud_mass_Msun`',
        '`e_cloud_mass_Msun`',
        '`cloud_surface_density_Msun_per_pc2`',
        '`e_cloud_surface_density_Msun_per_pc2`',
        '`sfr_Msun_per_Myr`',
        '`e_sfr_Msun_per_Myr`',
        '`sfr_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_surface_density_Msun_per_Myr_pc2`',
        '`sfe`',
        '`e_sfe`',
    ]
    #-----------------------------------
    # Obtain data from database
    # Obtain data from SQL
    c2d_gould_belt_data = load2py_mq_cloud(YSO_col_list)
    c2d_gould_belt_data = np.array(c2d_gould_belt_data, dtype=object)
    # Save the table
    np.savetxt('cloud_in_latex_sfe.txt', c2d_gould_belt_data, delimiter = '&', fmt = '%.3g')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
