#!/usr/bin/python3
'''
Abstract:
    Plot the SFR-gas relation in different Av contour regions (Without error consideration).
Usage:
    plot_sfr_vs_gas.py.
Output:
    1. The figure of SFR surface density and gas surface density.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200522
####################################
update log
20200522 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from chiu20_mysql_lib import load2py_mq_av_region, load2py_mq_cloud
from Heiderman10_lib import Heiderman_cloud, Heiderman_Av_regions_class_f, Heiderman_Av_regions_class_i
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 1:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_sfr_vs_gas.py")
        exit()
    #--------------------------------------------
    # Initialization
    Av_regions_col_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_I_surface_density_Msun_per_Myr_pc2`',
    ]
    cloud_col_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_surface_density_Msun_per_Myr_pc2`',
    ]
    # Obtain data from SQL
    # Each single cloud
    cloud_data = load2py_mq_cloud(cloud_col_list)
    cloud_data = np.array(cloud_data, dtype=object)
    gas_sigma_cloud =       np.array(cloud_data[:,0], dtype = float)
    e_gas_sigma_cloud =     np.array(cloud_data[:,1], dtype = float)
    sfr_sigma_cloud =       np.array(cloud_data[:,2], dtype = float)
    e_sfr_sigma_cloud =     np.array(cloud_data[:,3], dtype = float)
    flag_sfr_sigma_cloud =  np.array(cloud_data[:,4], dtype = str)
    # Av regions
    region_data = load2py_mq_av_region(Av_regions_col_list)
    region_data = np.array(region_data, dtype = object)
    gas_sigma_Av_regions =      np.array(region_data[:,0], dtype = float)
    e_gas_sigma_Av_regions =    np.array(region_data[:,1], dtype = float)
    sfr_sigma_Av_regions =      np.array(region_data[:,2], dtype = float)
    e_sfr_sigma_Av_regions =    np.array(region_data[:,3], dtype = float)
    flag_sfr_sigma_Av_regions = np.array(region_data[:,4], dtype = str)
    index_upper_limit = flag_sfr_sigma_Av_regions == 'U'
    print(flag_sfr_sigma_Av_regions)
    print(index_upper_limit)
    print(~index_upper_limit)
    #--------------------------------------------
    # Plot the figure
    # Each single cloud
    fig, ax = plt.subplots(figsize = (8,8))
    #ax.errorbar(
    #    x = gas_sigma_cloud,
    #    xerr = e_gas_sigma_cloud,
    #    y = sfr_sigma_cloud,
    #    yerr = e_sfr_sigma_cloud,
    #    label='My works (c2d clouds, considering all YSO)',
    #    fmt = 'ro',
    #)
    # Av regions
    ax.errorbar(
        x = gas_sigma_Av_regions[~index_upper_limit],
        xerr = e_gas_sigma_Av_regions[~index_upper_limit],
        y = sfr_sigma_Av_regions[~index_upper_limit],
        yerr = e_sfr_sigma_Av_regions[~index_upper_limit],
        label='My works (c2d Av regions, considering Class I YSO)',
        color = 'b',
        fmt = 'o'
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_Av_regions[index_upper_limit],
        y = sfr_sigma_Av_regions[index_upper_limit],
        label='My works (upper limits in c2d Av regions, considering Class I YSO)',
        marker = 'v',
        color = 'b',
        alpha = 0.5,
    )
        
    #--------------------------------------------
    # Additional data
    #-------------
    # Heiderman+10
    Heiderman_gas_sigma_class_i = np.array(Heiderman_Av_regions_class_i[:,1], dtype = float)
    Heiderman_sfr_sigma_class_i = np.array(Heiderman_Av_regions_class_i[:,2], dtype = float)
    Heiderman_gas_sigma_class_f = np.array(Heiderman_Av_regions_class_f[:,1], dtype = float)
    Heiderman_sfr_sigma_class_f = np.array(Heiderman_Av_regions_class_f[:,2], dtype = float)
    Heiderman_gas_sigma = np.hstack(
        (Heiderman_gas_sigma_class_i, Heiderman_gas_sigma_class_f)
    )
    Heiderman_sfr_sigma = np.hstack(
        (Heiderman_sfr_sigma_class_i, Heiderman_sfr_sigma_class_f)
    )
    ax.scatter(
        Heiderman_gas_sigma,
        Heiderman_sfr_sigma,
        label = 'Heiderman+10 (c2d Av regions, considering Class I and Flat YSO)',
        color = 'g',
    )
    #-------------
    # Kennicutt+98
    # K-S relation
    def Kennicut98_sfr_sigma(gas_sigma):
        # gas_sigma in Msun / pc^2
        # sfr_sigma in Msun / Myr pc^2
        sfr_sigma = 2.5e-4 * np.power(gas_sigma, 1.4)
        return sfr_sigma
    KS_gas_sigma = np.logspace(1, 3, 100)
    KS_sfr_sigma = Kennicut98_sfr_sigma(KS_gas_sigma)
    ax.plot(
        KS_gas_sigma, 
        KS_sfr_sigma, 
        color = 'k', 
        label = 'Kennicut+98 ( KS relation)'
    )
    #-----------------------------------
    # Adjust and Save the figure
    ax.set_xscale('log')
    ax.set_yscale('log')
    #ax.set_xlim(1e0, 1e3)
    #ax.set_ylim(1e-2, 1e1)
    ax.grid(True)
    ax.set_xlabel(r'gas surface density ($M_{sun} / pc^{2}$)')
    ax.set_ylabel(r'SFR surface density ($M_{sun} / Myr pc^{2}$)')
    ax.legend()
    fig.savefig("chiu20_sfr_vs_gas_Av_regions_class_I_YSO.png")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
