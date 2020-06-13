#!/usr/bin/python3
'''
Abstract:
    Print a figure that show the relation between SFR surface density and gas surface density.
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
from chiu20_mysql_lib import load2py_mq_cloud
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
    col_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`sfr_surface_density_Msun_per_Myr_pc2`'
    ]
    col_list_str = '|'.join(col_list)
    # Obtain data from SQL
    data = load2py_mq_cloud(col_list)
    data = np.array(data, dtype=float)
    # Each single cloud from c2d and Gould belt
    gas_sigma_c2d_gould_belt = data[:20,0]
    sfr_sigma_c2d_gould_belt = data[:20,1]
    # Each single cloud from Zucker+20
    gas_sigma_others = data[20:52,0]
    sfr_sigma_others = data[20:52,1]
    # Av regions, all YSO only
    gas_sigma_Av_regions = data[52:131,0]
    sfr_sigma_Av_regions = data[52:131,1]
    # c2d, Gould belt with All YSO, Class I YSO, and Class Flat YSO.

    #--------------------------------------------
    # Plot the figure
    fig, ax = plt.subplots(figsize = (8,8))
    #ax.scatter(
    #    gas_sigma_c2d_gould_belt, 
    #    sfr_sigma_c2d_gould_belt, 
    #    label='My works (clouds from c2d, Gould belt)'
    #)
    #ax.scatter(
    #    gas_sigma_others, 
    #    sfr_sigma_others, 
    #    label='My works (clouds from Zucker+20)'
    #)
    ax.scatter(
        gas_sigma_Av_regions,
        sfr_sigma_Av_regions,
        label='My works (c2d Av regions)'
    )
        
    #--------------------------------------------
    # Additional data
    #-------------
    # Heiderman+10
    Heiderman_cloud = np.array([
    # Cloud, gas_sigma, sfr_sigma
        [ 'Cha II  ', 64.3, 0.605],
        [ 'Lup I   ', 57.9, 0.367],
        [ 'Lup III ', 59.2, 1.10],
        [ 'Lup IV  ', 75.0, 1.19],
        [ 'Oph     ', 105 , 2.45],
        [ 'Per     ', 90.0, 1.31],
        [ 'Ser     ', 138 , 3.29],
        [ 'AurN    ', 92.9, 0.207],
        [ 'Aur     ', 92.4, 0.854],
        [ 'Cep     ', 68.7, 0.776],
        [ 'Cha III ', 47.5, 0.0357],
        [ 'Cha I   ', 91.1, 2.36],
        [ 'CrA     ', 92.1, 3.37],
        [ 'IC5146E ', 54.9, 0.378],
        [ 'IC5146NW', 59.1, 0.108],
        [ 'Lup VI  ', 67.5, 1.66],
        [ 'Lup V   ', 60.3, 0.915],
        [ 'Mus     ', 49.1, 0.440],
        [ 'Sco     ', 85.2, 0.343],
        [ 'Ser-Aqu ', 136 , 2.01],
    ], dtype = object)
    Heiderman_Av_regions_class_f = np.array([
    # Cloud, gas_sigma, sfr_sigma
        ['Cha II 1', 53.6, 0.18],
        ['Cha II 2', 92.6, 0.795],
        ['Cha II 3', 147, 4.68],
        ['Cha II 4', 193, 19.3],
        ['Lup I 1 ', 51.9, 0.174],
        ['Lup I 2', 109, 1.97],
        ['Lup I 3', 185, 15.0],
        ['Lup III 1', 54.8, 0.188],
        ['Lup III 2', 153, 3.29],
        ['Lup III 3', 248, 11.1],
        ['Lup IV 1', 61.5, 0.619],
        ['Lup IV 2', 157, 8.43],
        ['Lup IV 3', 267, 15.4],
        ['Oph 1', 87.2, 0.105],
        ['Oph 2', 198, 2.26],
        ['Oph 3', 319, 12.1],
        ['Oph 4', 435, 57.4],
        ['Oph 5', 542, 96.0],
        ['Per 1', 66.9, 0.0268],
        ['Per 2', 122, 0.364],
        ['Per 3', 194, 5.12],
        ['Per 4', 261, 10.3],
        ['Per 5', 317, 6.36],
        ['Per 6', 404, 78.7],
        ['Ser 1', 120, 0.105],
        ['Ser 2', 180, 1.10],
        ['Ser 3', 243, 7.57],
        ['Ser 4', 307, 54.8],
    ], dtype = object)
    #Heiderman_gas_sigma = np.array(Heiderman_cloud[:,1], dtype = float)
    #Heiderman_sfr_sigma = np.array(Heiderman_cloud[:,2], dtype = float)
    Heiderman_gas_sigma = np.array(Heiderman_Av_regions_class_f[:,1], dtype = float)
    Heiderman_sfr_sigma = np.array(Heiderman_Av_regions_class_f[:,2], dtype = float)
    ax.scatter(
        Heiderman_gas_sigma, 
        Heiderman_sfr_sigma, 
        label = 'Heiderman+10 (c2d Av regions)')
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
    ax.set_ylim(1e-2, 1e1)
    ax.grid(True)
    ax.set_xlabel(r'gas surface density ($M_{sun} / pc^{2}$)')
    ax.set_ylabel(r'SFR surface density ($M_{sun} / Myr pc^{2}$)')
    ax.legend()
    fig.savefig("chiu20_sfr_vs_gas_Av_regions.png")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
