#!/usr/bin/python3
'''
Abstract:
    Add a function to obtain the SFR-gas relation latex table and figure
Usage:
    Av_region_numpy2latex.py [data table]
Output:
    
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200325
####################################
update log
20200325 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib.pyplot as plt
import numpy as np
from uncertainties import unumpy, ufloat
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: Av_region_numpy2latex.py [data table]") 
        exit()
    data_table_name = argv[1]
    #--------------------------------------------
    # Load data
    data_table = np.loadtxt(data_table_name, dtype = str, delimiter = ',')
    # Estimate the ratio of SFR between my work and Heiderman's work.
    u_gas_sigma = unumpy.uarray(
        np.array(data_table[:,1], dtype = float),
        np.array(data_table[:,2], dtype = float)
    )
    u_gas_sigma_h = unumpy.uarray(
        np.array(data_table[:,5], dtype = float),
        np.array(data_table[:,6], dtype = float)
    )
    u_sfr_sigma = unumpy.uarray(
        np.array(data_table[:,3], dtype = float),
        np.array(data_table[:,4], dtype = float)
    )
    u_sfr_sigma_h = unumpy.uarray(
        np.array(data_table[:,7], dtype = float),
        np.array(data_table[:,8], dtype = float)
    )
    u_gas_sigma_ratio = u_gas_sigma/u_gas_sigma_h
    u_sfr_sigma_ratio = u_sfr_sigma/u_sfr_sigma_h
    # Print the result as a figure
    fig, axes = plt.subplots(
        1, 2, 
        figsize = (8,5),
    )
    # Gas
    axes[0].errorbar(
        x = unumpy.nominal_values(u_gas_sigma),
        xerr = unumpy.std_devs(u_gas_sigma),
        y = unumpy.nominal_values(u_gas_sigma_ratio),
        yerr = unumpy.std_devs(u_gas_sigma_ratio),
        fmt = 'o',
    )
    axes[0].set_xscale('log')
    axes[0].set_xlabel(r'$\Sigma_{gas}$ ($M_{sun} / pc^{2}$)')
    axes[0].set_ylabel('Ratio ($\Sigma_{gas}$/$\Sigma_{gas,Heiderman10}$)')
    # SFR
    axes[1].errorbar(
        x = unumpy.nominal_values(u_sfr_sigma),
        xerr = unumpy.std_devs(u_sfr_sigma),
        y = unumpy.nominal_values(u_sfr_sigma_ratio),
        yerr = unumpy.std_devs(u_sfr_sigma_ratio),
        fmt = 'o',
    )
    axes[1].set_xscale('log')
    axes[1].set_xlabel(r'$\Sigma_{SFR}$($M_{sun} / Myr \cdot pc^{2}$)')
    axes[1].set_ylabel('Ratio ($\Sigma_{SFR}$/$\Sigma_{SFR,Heiderman10}$)')
    fig.tight_layout()
    plt.savefig("sfr_gas_ratio_between_chiu20_and_Heiderman10", dpi = 300)
    # Save the new table with latex format.
    out_table = np.array(np.transpose([
        data_table[:,0],
        data_table[:,1],
        data_table[:,2],
        data_table[:,5],
        data_table[:,6],
        unumpy.nominal_values(u_gas_sigma_ratio),
        unumpy.std_devs(u_gas_sigma_ratio),
        data_table[:,3],
        data_table[:,4],
        data_table[:,7],
        data_table[:,8],
        unumpy.nominal_values(u_sfr_sigma_ratio),
        unumpy.std_devs(u_sfr_sigma_ratio),
    ]))
    #np.savetxt('test.txt', out_table, delimiter = ' & ', fmt = '%s')
    # Print the average value
    # Gas ratio
    avg_gas_sigma_ratio = np.average(
        unumpy.nominal_values(u_gas_sigma_ratio),
        weights = 1/unumpy.std_devs(u_gas_sigma_ratio),
    )
    std_gas_sigma_ratio = np.std(
        unumpy.nominal_values(u_gas_sigma_ratio)
    )
    avg_sfr_sigma_ratio = np.average(
        unumpy.nominal_values(u_sfr_sigma_ratio),
        weights = 1/unumpy.std_devs(u_sfr_sigma_ratio),
    )
    std_sfr_sigma_ratio = np.std(
        unumpy.nominal_values(u_sfr_sigma_ratio)
    )
    print (avg_gas_sigma_ratio, std_gas_sigma_ratio, avg_sfr_sigma_ratio, std_sfr_sigma_ratio)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
