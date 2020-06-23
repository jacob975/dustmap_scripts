#!/usr/bin/python3
'''
Abstract:
    A function to estimate the offset between my result and Heiderman result.
Usage:
    cmp_mywork_Heiderman10.py
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

from uncertainties import ufloat, unumpy

import numpy as np
from chiu20_mysql_lib import load2py_mq_cloud
from Heiderman10_lib import Heiderman_cloud

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 1:
        print ("The number of arguments is wrong.")
        print ("Usage: cmp_mywork_Heiderman10.py")
        exit()
    #--------------------------------------------
    # Initialize the database settings
    YSO_col_list = [
        '`index`',
        '`cloud`',
        '`cloud_surface_density_Msun_per_pc2`',
        '`e_cloud_surface_density_Msun_per_pc2`',
        '`sfr_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_surface_density_Msun_per_Myr_pc2`',
    ]
    YSO_sub_col_list = [
        '`index`',
        '`cloud`',
        '`area_pc2`',
        '`e_area_pc2`',
        '`yso_lifetime_Myr`',
        '`e_yso_lifetime_Myr`',
        '`cloud_mass_Msun`',
        '`e_cloud_mass_Msun`',
        '`total_yso_mass_Msun`',
        '`e_total_yso_mass_Msun`',
    ]
    #-----------------------------------
    # Obtain data from database
    # Obtain data from SQL
    c2d_gould_belt_data = load2py_mq_cloud(YSO_col_list)
    c2d_gould_belt_data = np.array(c2d_gould_belt_data, dtype=object)
    index_c2d_gould_belt =           np.array(c2d_gould_belt_data[:31,0], dtype = int)
    cloud_c2d_gould_belt =           np.array(c2d_gould_belt_data[:31,1], dtype = str)
    gas_sigma_c2d_gould_belt =       np.array(c2d_gould_belt_data[:31,2], dtype = float)
    e_gas_sigma_c2d_gould_belt =     np.array(c2d_gould_belt_data[:31,3], dtype = float)
    sfr_sigma_c2d_gould_belt =       np.array(c2d_gould_belt_data[:31,4], dtype = float)
    e_sfr_sigma_c2d_gould_belt =     np.array(c2d_gould_belt_data[:31,5], dtype = float)
    flag_sfr_sigma_c2d_gould_belt =  np.array(c2d_gould_belt_data[:31,6], dtype = str)
    
    sub_data = load2py_mq_cloud(YSO_sub_col_list)
    sub_data = np.array(sub_data, dtype=object)

    def calc_sfr_gas_relation(index_list, inp_data):
        index_sub =             np.array(sub_data[index_list,0], dtype = int)
        cloud_sub =             np.array(sub_data[index_list,1], dtype = str)
        area_pc2_sub =          np.array(sub_data[index_list,2], dtype = float)
        e_area_pc2_sub =        np.array(sub_data[index_list,3], dtype = float)
        yso_lifetime_sub =      np.array(sub_data[index_list,4], dtype = float)
        e_yso_lifetime_sub =    np.array(sub_data[index_list,5], dtype = float)
        cloud_mass_sub =        np.array(sub_data[index_list,6], dtype = float)
        e_cloud_mass_sub =      np.array(sub_data[index_list,7], dtype = float)
        total_yso_mass_sub =    np.array(sub_data[index_list,8], dtype = float)
        e_total_yso_mass_sub =  np.array(sub_data[index_list,9], dtype = float)
        #return sfr_sigma, e_sfr_sigma, gas_sigma, e_gas_sigma 
        u_area_pc2_sub = unumpy.uarray(area_pc2_sub, e_area_pc2_sub)
        u_yso_lifetime_sub = unumpy.uarray(yso_lifetime_sub, e_yso_lifetime_sub)
        u_cloud_mass_sub = unumpy.uarray(cloud_mass_sub, e_cloud_mass_sub)
        u_total_yso_mass_sub = unumpy.uarray(total_yso_mass_sub, e_total_yso_mass_sub)
        u_area_pc2 = u_area_pc2_sub.sum()
        u_yso_lifetime = u_yso_lifetime_sub[0]
        u_cloud_mass = u_cloud_mass_sub.sum()
        u_total_yso_mass = u_total_yso_mass_sub.sum()
        print(u_area_pc2, u_yso_lifetime, u_cloud_mass, u_total_yso_mass)
        u_sfr = u_total_yso_mass / u_yso_lifetime
        u_sfr_per_area_pc2 = u_sfr / u_area_pc2
        u_cloud_surface_density = u_cloud_mass / u_area_pc2
        # gas_sigma, e_gas_sigma, sfr_sigma, e_sfr_sigma
        print(u_cloud_surface_density.n, u_cloud_surface_density.s, u_sfr_per_area_pc2.n, u_sfr_per_area_pc2.s) 
        return u_cloud_surface_density.n, u_cloud_surface_density.s, u_sfr_per_area_pc2.n, u_sfr_per_area_pc2.s 


    #-----------------------------------
    # Combine regions
    # Cepheus
    cepheus_index_list = np.array([9, 10, 11, 12, 13])
    cepheus_gas_sigma, cepheus_e_gas_sigma, cepheus_sfr_sigma, cepheus_e_sfr_sigma = calc_sfr_gas_relation(cepheus_index_list, sub_data)
    # Scorpius
    scorpius_index_list = np.array([22, 23, 24, 25, 30])
    scorpius_gas_sigma, scorpius_e_gas_sigma, scorpius_sfr_sigma, scorpius_e_sfr_sigma = calc_sfr_gas_relation(scorpius_index_list, sub_data)
    # Aquila
    aquila_index_list = np.array([26, 27, 28, 29])
    aquila_gas_sigma, aquila_e_gas_sigma, aquila_sfr_sigma, aquila_e_sfr_sigma = calc_sfr_gas_relation(aquila_index_list, sub_data)
    # Total
    total_index_list = np.arange(31)
    total_gas_sigma, total_e_gas_sigma, total_sfr_sigma, total_e_sfr_sigma = calc_sfr_gas_relation(total_index_list, sub_data)
    print(total_gas_sigma, total_e_gas_sigma, total_sfr_sigma, total_e_sfr_sigma)
    #-----------------------------------
    # Save the table
    out_data = c2d_gould_belt_data[:31]
    out_data = np.append(
        out_data,
        np.array([35, 'Cepheus', cepheus_gas_sigma, cepheus_e_gas_sigma, cepheus_sfr_sigma, cepheus_e_sfr_sigma, 'A']))
    out_data = np.append(
        out_data,
        np.array([36, 'Scorpius', scorpius_gas_sigma, scorpius_e_gas_sigma, scorpius_sfr_sigma, scorpius_e_sfr_sigma, 'A']))
    out_data = np.append(
        out_data,
        np.array([37, 'Aquila', aquila_gas_sigma, aquila_e_gas_sigma, aquila_sfr_sigma, aquila_e_sfr_sigma, 'A']))
    out_data = out_data.reshape((-1, 7))
    print(out_data)
    np.savetxt('c2d_gould_belt_sfr_gas_relation.txt', out_data, fmt ='%s', delimiter = ' & ')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
