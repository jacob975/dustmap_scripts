#!/usr/bin/python3
'''
Abstract:
    Print a figure that show the relation between SFR surface density and gas surface density.
Usage:
    plot_sfe_vs_distance.py.
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

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
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
        print ("Usage: plot_sfe_vs_distance.py")
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
        '`distance_pc`',
        '`e_distance_pc`',
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
    distance_pc =                    np.array(c2d_gould_belt_data[:,7], dtype = float)
    e_distance_pc =                  np.array(c2d_gould_belt_data[:,8], dtype = float)
    index_U_c2d_gould_belt = flag_sfr_sigma_c2d_gould_belt == 'U'
    #--------------------------------------------
    # Make a color scheme
    colors = cm.rainbow(gas_sigma_c2d_gould_belt/np.max(gas_sigma_c2d_gould_belt))
    # Plot the figure
    fig = plt.figure(figsize = (6,6))
    ax = fig.add_axes((0.1, 0.1, 0.78, 0.8))
    ax.tick_params(
        axis = 'x',
        which='both',
        reset = True,
    )
    cax = fig.add_axes((0.88, 0.1, 0.02, 0.8))
    inp_x = distance_pc[~index_U_c2d_gould_belt]
    inp_xerr = e_distance_pc[~index_U_c2d_gould_belt]
    inp_y = sfe[~index_U_c2d_gould_belt]*100
    inp_yerr = e_sfe[~index_U_c2d_gould_belt]*100
    for i in range(len(inp_x)):
        ax.errorbar(
            x = inp_x[i],
            xerr = inp_xerr[i],
            y = inp_y[i],
            yerr = inp_yerr[i],
            #label = 'SFE-d relation',
            color = colors[i],
            fmt = 'o',
        )
    # Plot average number of regions within 500 pc.
    sfe_500pc = sfe[distance_pc < 500]*100
    e_sfe_500pc = e_sfe[distance_pc < 500]*100
    avg_sfe_500pc = np.average(sfe_500pc, weights = 1/e_sfe_500pc)
    std_sfe_500pc = np.std(sfe_500pc)
    print(avg_sfe_500pc, std_sfe_500pc)
    sfe_1000pc = sfe[(distance_pc >= 500) & (distance_pc < 1000)]*100
    e_sfe_1000pc = e_sfe[(distance_pc >= 500) & (distance_pc < 1000)]*100
    avg_sfe_1000pc = np.average(sfe_1000pc, weights = 1/e_sfe_1000pc)
    std_sfe_1000pc = np.std(sfe_1000pc)
    print(avg_sfe_1000pc, std_sfe_1000pc)
    out_x = np.array([1e2, 5e2])
    out_y = np.ones(2)*avg_sfe_500pc
    e_out_y = np.ones(2)*std_sfe_500pc
    ax.fill_between(
        out_x,
        out_y- e_out_y,
        out_y+ e_out_y,
        alpha = 0.3,
        facecolor = 'orange',
        edgecolor = 'orange',
    )
    ax.plot(
        out_x, out_y,
        linestyle = '--',
        c = 'orange',
        zorder = 100,
    )
    # Plot colorbar
    cmap = cm.rainbow
    norm = mpl.colors.Normalize(
        vmin=0, 
        vmax=np.max(gas_sigma_c2d_gould_belt)
    )
    cb1 = mpl.colorbar.ColorbarBase(cax, cmap = cmap, norm = norm)
    cb1.set_label(r'$\Sigma_{gas}$ (M$_{\odot}$pc$^{-2}$)')
    #--------------------------------------------
    #-----------------------------------
    # Adjust and Save the figure
    ax.set_xscale('log')
    ax.set_yscale('log')
    # Set the second x tick for Av,RC
    x_upper = 1e2
    x_lower = 1e4
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
    ax.text(
        x = 0.55,
        y = 0.95,
        s = 'SFE$_{d<500pc}$=%.2g$\pm$%.2f %%' % (
            avg_sfe_500pc,
            std_sfe_500pc
        ),
        transform = ax.transAxes,
        horizontalalignment='left',
        verticalalignment='top',
        bbox=dict(facecolor='white', edgecolor='black', pad=5.0),
        zorder = 101,
    )
    ax.set_xlim(x_upper, x_lower)
    #ax.set_ylim(1e-2, 1e1)
    ax.grid(True)
    ax.set_xlabel(r'average distance (pc)')
    ax.set_ylabel(r'SFE (%)')
    ax.legend()
    fig.savefig("chiu20_sfe_vs_distance.png", dpi = 200)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
