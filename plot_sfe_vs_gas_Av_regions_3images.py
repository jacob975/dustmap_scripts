#!/usr/bin/python3
'''
Abstract:
    Plot the SFR-gas relation in different Av contour regions (Without error consideration).
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

# Condition can be: 'less_500pc', '500_1000pc', 'over_1000pc'
def plot_sfe_gas_relation(ax, condition, panel_order ):
    #--------------------------------------------
    # Initialization
    class_I_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`distance_pc`',
    ]
    class_F_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`distance_pc`',
    ]
    # Obtain data from SQL
    # Class I, Zucker+20 sources only
    class_I_data = load2py_mq_av_region(class_I_list)
    class_I_data = np.array(class_I_data, dtype=object)
    gas_sigma_class_I =       np.array(class_I_data[:,0], dtype = float)
    e_gas_sigma_class_I =     np.array(class_I_data[:,1], dtype = float)
    sfr_sigma_class_I =       np.array(class_I_data[:,2], dtype = float)
    e_sfr_sigma_class_I =     np.array(class_I_data[:,3], dtype = float)
    flag_sfr_sigma_class_I =  np.array(class_I_data[:,4], dtype = str)
    distance_class_I =        np.array(class_I_data[:,5], dtype = float)
    index_U_class_I = flag_sfr_sigma_class_I == 'U'
    # Take the region inside the defined distance range
    index_distance_condition_class_I = None
    if condition == 'less_500pc':
        index_distance_condition_class_I = distance_class_I <= 500
    elif condition == '500_1000pc':
        index_distance_condition_class_I = np.logical_and(
            distance_class_I > 500,
            distance_class_I <= 1000
        )
    elif condition == 'over_1000pc':
        index_distance_condition_class_I = distance_class_I > 1000
    # Class Flat, Zucker+20 sources only
    class_F_data = load2py_mq_av_region(class_F_list)
    class_F_data = np.array(class_F_data, dtype=object)
    gas_sigma_class_F =      np.array(class_F_data[:,0], dtype = float)
    e_gas_sigma_class_F =    np.array(class_F_data[:,1], dtype = float)
    sfr_sigma_class_F =      np.array(class_F_data[:,2], dtype = float)
    e_sfr_sigma_class_F =    np.array(class_F_data[:,3], dtype = float)
    flag_sfr_sigma_class_F = np.array(class_F_data[:,4], dtype = str)
    distance_class_F =        np.array(class_F_data[:,5], dtype = float)
    index_U_class_F = flag_sfr_sigma_class_F == 'U'
    # Take the region inside the defined distance range
    index_distance_condition_class_F = None
    if condition == 'less_500pc':
        index_distance_condition_class_F = distance_class_F <= 500
    elif condition == '500_1000pc':
        index_distance_condition_class_F = np.logical_and(
            distance_class_F > 500,
            distance_class_F <= 1000
        )
    elif condition == 'over_1000pc':
        index_distance_condition_class_F = distance_class_F > 1000
    #----------
    # Class_I 
    ax.errorbar(
        x = gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        xerr = e_gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        y = sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        yerr = e_sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        label= 'Class I YSO',
        color = 'b',
        fmt = 'o',
        markersize = 2,
        linewidth = 1
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_class_I[(index_U_class_I) & (index_distance_condition_class_I)],
        y = sfr_sigma_class_I[(index_U_class_I) & (index_distance_condition_class_I)],
        label='Class I YSO upper limit', 
        marker = 'v',
        s = 3,
        color = 'b',
        alpha = 0.5,
    )
    #----------
    # Class_F
    ax.errorbar(
        x = gas_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)],
        xerr = e_gas_sigma_class_F[(~index_U_class_F) & index_distance_condition_class_F],
        y = sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)],
        yerr = e_sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)],
        label='Class Flat YSO',
        color = 'm',
        fmt = 'o',
        markersize = 2,
        linewidth = 1
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_class_F[(index_U_class_F) & (index_distance_condition_class_F)],
        y = sfr_sigma_class_F[(index_U_class_F) & (index_distance_condition_class_F)],
        label='Class Flat YSO upper limit', 
        marker = 'v',
        color = 'm',
        alpha = 0.5,
        s = 3,
    )
    # Show the text
    ax.text(
        x = 0.05, 
        y = 0.9, 
        s = condition,
        transform = ax.transAxes,
    )    
    #--------------------------------------------
    # Additional data
    #-------------
    # Heiderman+10
    Heiderman_gas_sigma_class_i = np.array(Heiderman_Av_regions_class_i[:,1], dtype = float)
    Heiderman_sfr_sigma_class_i = np.array(Heiderman_Av_regions_class_i[:,2], dtype = float)
    Heiderman_gas_sigma_class_f = np.array(Heiderman_Av_regions_class_f[:,1], dtype = float)
    Heiderman_sfr_sigma_class_f = np.array(Heiderman_Av_regions_class_f[:,2], dtype = float)
    #ax.scatter(
    #    Heiderman_gas_sigma_class_i, 
    #    Heiderman_sfr_sigma_class_i, 
    #    label = 'Heiderman+10 (c2d class I)', 
    #    color = 'g',
    #)
    #ax.scatter(
    #    Heiderman_gas_sigma_class_f, 
    #    Heiderman_sfr_sigma_class_f, 
    #    label = 'Heiderman+10 (c2d class F)', 
    #    color = 'c',
    #)
    #-------------
    # Kennicutt+98
    # K-S relation
    def Kennicut98_sfr_sigma(gas_sigma):
        # gas_sigma in Msun / pc^2
        # sfr_sigma in Msun / Myr pc^2
        sfr_sigma = 2.5e-4 * np.power(gas_sigma, 1.4)
        return sfr_sigma
    KS_gas_sigma = np.logspace(1, 4.5, 100)
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
    x_upper = 1e1
    x_lower = 1e5
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
    ax.set_xlim(x_upper, x_lower)
    ax.set_ylim(1e-3, 1e3)
    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    ax.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    ax2.tick_params(
        axis='x',
        which='both',
        direction='in'
    )
    ax.grid(True)
    if panel_order == 1:
        ax.set_xlabel(r'gas surface density ($M_{sun} / pc^{2}$)')
        ax2.set_xlabel('A$_{v,RC}$')
    if panel_order == 0:
        ax.set_ylabel(r'SFR surface density ($M_{sun} / Myr \cdot pc^{2}$)')
    if panel_order == 2:
        pass
        #ax.legend()

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 1:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_sfe_vs_gas.py")
        exit()
    #--------------------------------------------
    # Plot the figure
    fig, axes = plt.subplots(
        1, 3, 
        sharex=True, 
        sharey=True,
        figsize=(12, 4))
    plot_sfe_gas_relation(axes[0], 'less_500pc', 0)
    plot_sfe_gas_relation(axes[1], '500_1000pc', 1)
    plot_sfe_gas_relation(axes[2], 'over_1000pc', 2)
    plt.tight_layout()
    fig.savefig("chiu20_sfe_vs_gas_Av_regions_3images.png", dpi = 150)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
