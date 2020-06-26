#!/usr/bin/python3
'''
Abstract:
    Add a function to obtain the SFR-gas relation latex table and figure
Usage:
    sfr_gas_relation_numpy2latex.py [data table]
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
        print ("Usage: sfr_gas_relation_numpy2latex.py [data table]") 
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
    #----------------------------------------------------
    # Print the result as a figure
    fig, axes = plt.subplots(
        1, 2, 
        figsize = (8,4),
    )
    #-------------------
    # Gas
    axes[0].errorbar(
        x = unumpy.nominal_values(u_gas_sigma),
        xerr = unumpy.std_devs(u_gas_sigma),
        y = unumpy.nominal_values(u_gas_sigma_ratio),
        yerr = unumpy.std_devs(u_gas_sigma_ratio),
        fmt = 'o',
        color = 'k',
        mfc='none',
        linewidth = 1,
        ecolor = 'k',
        zorder = 100,
    )
    # Twin axis
    x_lower = 4e1
    x_upper = 5e2
    # A_v,DL = 0.74*(dust_sigma/ (10^5 * M_sun / kpc^-2))
    def get_AvDL(cloud_sigma):
        nominator = 0.74 * cloud_sigma # M_sun pc-2
        denominator = 10 # M_sun pc-2
        return nominator/denominator
    # A_v,RC = (0.38*U_min + 0.27) * A_v,DL
    # by Assuming U_min = 0.5
    def get_AvRC(AvDL):
        return (0.38*0.5 + 0.27) * AvDL
    ax2 = axes[0].twiny()
    ax2.set_xscale('log')
    ax2.set_xlim(
        get_AvRC(get_AvDL(x_lower)),
        get_AvRC(get_AvDL(x_upper)),
    )
    axes[0].set_xlim(x_lower, x_upper)
    ax2.set_xlabel(r'A$_{V,RQ}$')
    # Average value
    out_x = np.logspace(np.log10(x_lower), np.log10(x_upper), 100)
    out_y = np.ones(100)*avg_gas_sigma_ratio
    e_out_y = np.ones(100)*std_gas_sigma_ratio
    axes[0].fill_between(
        out_x, 
        out_y-e_out_y, 
        out_y+e_out_y, 
        alpha = 0.3,
        facecolor='orange',
        edgecolor='orange',
        zorder = 50
    )
    axes[0].plot(
        out_x, out_y, 
        linestyle = '--', 
        c= 'orange',
        zorder = 51,
    )
    # fine tune the table
    axes[0].set_xscale('log')
    axes[0].set_xlabel(r'$\Sigma_{gas}$ ($M_{sun} / pc^{2}$)')
    axes[0].set_ylabel('Ratio$_{\Sigma_{gas}}$ ($\Sigma_{gas}$/$\Sigma_{gas,Heiderman10}$)')
    axes[0].tick_params(
        axis = 'x',
        which='both',
        direction='in',
    )
    axes[0].tick_params(
        axis = 'y',
        which='both',
        direction='in',
    )
    ax2.tick_params(
        axis='x',
        which='both',
        direction='in',
    )
    #---------------
    # SFR
    x_upper = 1e1
    x_lower = 1e-2
    axes[1].errorbar(
        x = unumpy.nominal_values(u_sfr_sigma),
        xerr = unumpy.std_devs(u_sfr_sigma),
        y = unumpy.nominal_values(u_sfr_sigma_ratio),
        yerr = unumpy.std_devs(u_sfr_sigma_ratio),
        fmt = 'o',
        color = 'k',
        mfc='none',
        linewidth = 1,
        ecolor = 'k',
        zorder = 100,
    )
    # Average value
    out_x = np.logspace(np.log10(x_lower), np.log10(x_upper), 100)
    out_y = np.ones(100)*avg_sfr_sigma_ratio
    e_out_y = np.ones(100)*std_sfr_sigma_ratio
    axes[1].fill_between(
        out_x, 
        out_y-e_out_y, 
        out_y+e_out_y, 
        alpha = 0.3,
        facecolor='orange',
        edgecolor='orange',
        zorder = 50,
    )
    axes[1].plot(
        out_x, out_y, 
        linestyle = '--', 
        c= 'orange',
        zorder = 51,
    )
    # fine tune the table
    axes[1].set_xlim(x_lower, x_upper)
    axes[1].set_xscale('log')
    axes[1].set_xlabel(r'$\Sigma_{SFR}$($M_{sun} / Myr \cdot pc^{2}$)')
    axes[1].set_ylabel('Ratio$_{\Sigma_{SFR}}$ ($\Sigma_{SFR}$/$\Sigma_{SFR,Heiderman10}$)')
    axes[1].tick_params(
        axis = 'x',
        which='both',
        direction='in',
    )
    axes[1].tick_params(
        axis = 'y',
        which='both',
        direction='in',
    )
    fig.tight_layout()
    plt.savefig(
        "sfr_gas_ratio_between_chiu20_and_Heiderman10", 
        dpi = 200
    )
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
