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
from chiu20_mysql_lib import load2py_mq_av_region
from uncertainties import unumpy

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Initialize the database settings
    YSO_col_list = [
        '`cloud`',
        '`class_i_yso_number`',
        '`class_f_yso_number`',
        '`Av_threshold`',
        '`area_deg2`',
        '`area_pc2`',
        '`e_area_pc2`',
        '`cloud_mass_Msun`',
        '`e_cloud_mass_Msun`',
        '`cloud_surface_density_Msun_per_pc2`',
        '`e_cloud_surface_density_Msun_per_pc2`',
        '`sfr_I_Msun_per_Myr`',
        '`e_sfr_I_Msun_per_Myr`',
        '`sfr_F_Msun_per_Myr`',
        '`e_sfr_F_Msun_per_Myr`',
        '`sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_surface_density_Msun_per_Myr_pc2`',
    ]
    #-----------------------------------
    # Obtain data from database
    # Obtain data from SQL
    c2d_gould_belt_data = load2py_mq_av_region(YSO_col_list)
    cloud = np.array(c2d_gould_belt_data[:,0], dtype = np.dtype('U100'))
    class_i_yso_number = np.array(c2d_gould_belt_data[:,1], dtype = int)
    class_f_yso_number = np.array(c2d_gould_belt_data[:,2], dtype = int)
    Av_threshold = np.array(c2d_gould_belt_data[:,3], dtype = np.dtype('U20'))
    area_deg2 = np.array(c2d_gould_belt_data[:,4], dtype = float)
    area_pc2 = np.array(c2d_gould_belt_data[:,5], dtype = float)
    e_area_pc2 = np.array(c2d_gould_belt_data[:,6], dtype = float)
    cloud_mass_Msun = np.array(c2d_gould_belt_data[:,7], dtype = float)
    e_cloud_mass_Msun = np.array(c2d_gould_belt_data[:,8], dtype = float)
    u_cloud_mass_Msun = unumpy.uarray(cloud_mass_Msun, e_cloud_mass_Msun)
    cloud_surface_density_Msun_per_pc2 = np.array(c2d_gould_belt_data[:,9], dtype = float)
    e_cloud_surface_density_Msun_per_pc2 = np.array(c2d_gould_belt_data[:,10], dtype = float)
    sfr_I_Msun_per_Myr = np.array(c2d_gould_belt_data[:,11], dtype = float)
    e_sfr_I_Msun_per_Myr = np.array(c2d_gould_belt_data[:,12], dtype = float)
    sfr_F_Msun_per_Myr = np.array(c2d_gould_belt_data[:,13], dtype = float)
    e_sfr_F_Msun_per_Myr = np.array(c2d_gould_belt_data[:,14], dtype = float)
    sfr_I_surface_density_Msun_per_Myr_pc2 = np.array(c2d_gould_belt_data[:,15], dtype = float)
    e_sfr_I_surface_density_Msun_per_Myr_pc2 = np.array(c2d_gould_belt_data[:,16], dtype = float)
    sfr_F_surface_density_Msun_per_Myr_pc2 = np.array(c2d_gould_belt_data[:,17], dtype = float)
    e_sfr_F_surface_density_Msun_per_Myr_pc2 = np.array(c2d_gould_belt_data[:,18], dtype = float)
    flag_sfr_surface_density_Msun_per_Myr_pc2 = np.array(c2d_gould_belt_data[:,19], dtype = np.dtype('U4'))
    print(u_cloud_mass_Msun)
    # Print the formatted table
    for i in range(len(c2d_gould_belt_data)):
        latex_line = \
            "%s & " \
            "%d & " \
            "%d & " \
            "%s & " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g & " \
            "%.3g $\pm$ " \
            "%.3g \\\ " % (
                cloud[i],
                class_i_yso_number[i],
                class_f_yso_number[i],
                Av_threshold[i],
                area_deg2[i],
                area_pc2[i],
                e_area_pc2[i],
                cloud_mass_Msun[i],
                e_cloud_mass_Msun[i],
                cloud_surface_density_Msun_per_pc2[i],
                e_cloud_surface_density_Msun_per_pc2[i],
                sfr_I_Msun_per_Myr[i],
                e_sfr_I_Msun_per_Myr[i],
                sfr_F_Msun_per_Myr[i],
                e_sfr_F_Msun_per_Myr[i],
                sfr_I_surface_density_Msun_per_Myr_pc2[i],
                e_sfr_I_surface_density_Msun_per_Myr_pc2[i],
                sfr_F_surface_density_Msun_per_Myr_pc2[i],
                e_sfr_F_surface_density_Msun_per_Myr_pc2[i],
            )
        print(latex_line)
        np_line = \
            "%s, " \
            "%d, " \
            "%d, " \
            "%s, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%.3g, " \
            "%s, " % (
                cloud[i],
                class_i_yso_number[i],
                class_f_yso_number[i],
                Av_threshold[i],
                area_deg2[i],
                area_pc2[i],
                e_area_pc2[i],
                cloud_mass_Msun[i],
                e_cloud_mass_Msun[i],
                cloud_surface_density_Msun_per_pc2[i],
                e_cloud_surface_density_Msun_per_pc2[i],
                sfr_I_Msun_per_Myr[i],
                e_sfr_I_Msun_per_Myr[i],
                sfr_F_Msun_per_Myr[i],
                e_sfr_F_Msun_per_Myr[i],
                sfr_I_surface_density_Msun_per_Myr_pc2[i],
                e_sfr_I_surface_density_Msun_per_Myr_pc2[i],
                sfr_F_surface_density_Msun_per_Myr_pc2[i],
                e_sfr_F_surface_density_Msun_per_Myr_pc2[i],
                flag_sfr_surface_density_Msun_per_Myr_pc2[i],
            )
        #print(np_line)
    # Save the table
    #np.savetxt('cloud_in_latex.txt', c2d_gould_belt_data, delimiter = ' & ', fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
