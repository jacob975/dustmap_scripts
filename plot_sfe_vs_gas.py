#!/usr/bin/python3
'''
Abstract:
    Print a figure that show the relation between SFR surface density and gas surface density.
Usage:
    plot_sfe_vs_gas.py.
Output:
    1. The figure of SFR surface density and gas surface density.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200629
####################################
update log
20200629 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from chiu20_mysql_lib import load2py_mq_cloud
from Heiderman10_lib import Heiderman_cloud, index_HC
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
    YSO_col_list = [
        '`cloud_surface_density_Msun_per_pc2`',
        '`e_cloud_surface_density_Msun_per_pc2`',
        '`sfr_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_surface_density_Msun_per_Myr_pc2`',
        '`sfe`',
        '`e_sfe`',
    ]
    col_list_str = '|'.join(YSO_col_list)
    # Obtain data from SQL
    c2d_gould_belt_data = load2py_mq_cloud(YSO_col_list)
    c2d_gould_belt_data = np.array(c2d_gould_belt_data, dtype=object)
    gas_sigma_c2d_gould_belt =       np.array(c2d_gould_belt_data[:,0], dtype = float)
    e_gas_sigma_c2d_gould_belt =     np.array(c2d_gould_belt_data[:,1], dtype = float)
    sfr_sigma_c2d_gould_belt =       np.array(c2d_gould_belt_data[:,2], dtype = float)
    e_sfr_sigma_c2d_gould_belt =     np.array(c2d_gould_belt_data[:,3], dtype = float)
    flag_sfr_sigma_c2d_gould_belt =  np.array(c2d_gould_belt_data[:,4], dtype = str)
    sfe =                            np.array(c2d_gould_belt_data[:,5], dtype = float)
    e_sfe =                          np.array(c2d_gould_belt_data[:,6], dtype = float)
    index_U_c2d_gould_belt = flag_sfr_sigma_c2d_gould_belt == 'U'
    #--------------------------------------------
    # Plot the figure
    fig, ax = plt.subplots(figsize = (6,6))
    ax.errorbar(
        x = gas_sigma_c2d_gould_belt[~index_U_c2d_gould_belt],
        xerr = e_gas_sigma_c2d_gould_belt[~index_U_c2d_gould_belt],
        y = sfe[~index_U_c2d_gould_belt]*100,
        yerr = e_sfe[~index_U_c2d_gould_belt]*100,
        label = 'SFE-gas relation',
        color = 'k',
        fmt = 'o',
    )
    #--------------------------------------------
    # Additional data
    #-------------
    # Heiderman+10
    '''
    #TODO
    Heiderman_gas_sigma = np.array(Heiderman_cloud[:,index_HC.index('gas_sigma')], dtype = float)
    e_Heiderman_gas_sigma = np.array(Heiderman_cloud[:,index_HC.index('e_gas_sigma')], dtype = float)
    Heiderman_sfr_sigma = np.array(Heiderman_cloud[:,index_HC.index('sfr_sigma')], dtype = float)
    e_Heiderman_sfr_sigma = np.array(Heiderman_cloud[:,index_HC.index('e_sfr_sigma')], dtype = float)
    ax.errorbar(
        x = Heiderman_gas_sigma,
        xerr = e_Heiderman_gas_sigma,
        y = Heiderman_sfr_sigma, 
        yerr = e_Heiderman_sfr_sigma,
        label = 'Heiderman+10 (c2d and Gould belt clouds)',
        color = 'g',
        fmt = 'o',
    )
    '''
    #-------------
    # Kennicutt+98
    # K-S relation
    '''
    def Kennicut98_sfr_sigma(gas_sigma):
        # gas_sigma in Msun / pc^2
        # sfr_sigma in Msun / Myr pc^2
        sfr_sigma = 2.5e-4 * np.power(gas_sigma, 1.4)
        return sfr_sigma
    KS_gas_sigma = np.logspace(1, 5, 100)
    KS_sfr_sigma = Kennicut98_sfr_sigma(KS_gas_sigma)
    ax.plot(
        KS_gas_sigma, 
        KS_sfr_sigma, 
        color = 'k', 
        label = 'Kennicut+98 ( KS relation)'
    )
    '''
    #-----------------------------------
    # Adjust and Save the figure
    ax.set_xscale('log')
    ax.set_yscale('log')
    # Set the second x tick for Av,RC
    x_upper = 1e1
    x_lower = 1e3
    # A_v,DL = 0.74*(dust_sigma/ (10^5 * M_sun / kpc^-2))
    def get_AvDL(cloud_sigma):
        nominator = 0.74 * cloud_sigma # M_sun pc-2
        denominator = 10 # M_sun pc-2
        return nominator/denominator
    # A_v,RC = (0.38*U_min + 0.27) * A_v,DL
    # by Assuming U_min = 0.5
    def get_AvRC(AvDL):
        return (0.38*0.5 + 0.27) * AvDL
    ax2 = ax.twiny()
    ax2.set_xscale('log')
    ax2.set_xlim(
        get_AvRC(get_AvDL(x_upper)),
        get_AvRC(get_AvDL(x_lower)),
    )
    ax2.set_xlabel(r'A$_{V, RQ}$')
    # Fine tune the panel
    ax.tick_params(
        axis = 'x',
        which='both',
        direction='in',
    )
    ax.tick_params(
        axis = 'y',
        which='both',
        direction='in',
    )
    ax2.tick_params(
        axis='x',
        which='both',
        direction='in',
    )
    ax.set_xlim(x_upper, x_lower)
    #ax.set_ylim(1e-2, 1e1)
    ax.grid(True)
    ax.set_xlabel(r'gas surface density ($M_{sun} / pc^{2}$)')
    ax.set_ylabel(r'SFE (%)')
    ax.legend()
    fig.savefig("chiu20_sfe_vs_gas.png", dpi = 200)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
