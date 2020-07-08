#!/usr/bin/python3
'''
Abstract:
    Plot the luminosity histogram with the given table.
Usage:
    plot_two_L_hist.py [paras of luminosity func.] [Q labels] [paras of luminosity func.] [Q labels]
Output:
    A histogram of luminosity.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200706 
####################################
update log
20200706 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv
import numpy as np
from matplotlib import pyplot as plt

import convert_lib

def find_non_saturated(Q_array):
    # Initialize
    non_saturated_source_index = np.arange(len(Q_array))
    band_number = len(Q_array[0])
    for band in range(band_number):
        tmp_index = np.where(Q_array[:,band] != "S")[0]
        non_saturated_source_index = np.intersect1d(
            non_saturated_source_index,
            tmp_index
        )
        '''
        # Debug
        print("---")
        print(tmp_index)
        print(non_saturated_source_index)
        '''
    return non_saturated_source_index

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #----------------------------------------
    # Load argv
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_L_hist.py [paras1 of luminosity func.] [Q1 labels] [paras2 of luminosity func.] [Q2 labels]") 
        exit()
    paras_array_name = argv[1]
    Q_name = argv[2]
    paras2_array_name = argv[3]
    Q2_name = argv[4]
    #-----------------------------------------
    # Load data
    # paras_array
    # alpha, L_mir, L_bol
    paras_array = np.loadtxt(paras_array_name, dtype = float)
    paras2_array = np.loadtxt(paras2_array_name, dtype = float)
    # Q_array
    # Quality flag of 8 bands.
    Q_array = np.loadtxt(Q_name, dtype = str)
    Q2_array = np.loadtxt(Q_name, dtype = str)
    #-----------------------------------------
    # List 1: All sources
    L_bol_list_1 = paras_array[:, 2]
    # List 2: Source without saturation. 
    index_non_saturated = find_non_saturated(Q_array)
    L_bol_list_2 = paras_array[index_non_saturated, 2]
    # List 3: c2d sources
    L_bol_list_3 = paras2_array[:,2]
    #-----------------------------------
    # Plot the histogram
    fig, axes = plt.subplots(figsize = (8,6))
    plt.hist(
        L_bol_list_1,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'k',
        label = "SEIP sources",
        zorder = 11,
    )
    plt.hist(
        L_bol_list_2,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'g',
        label = "Non-saturated SEIP sources",
        zorder = 12,
    )
    plt.hist(
        L_bol_list_3,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'r',
        label = "c2d sources",
        zorder = 10,
    )
    axes.legend()
    axes.set_xscale("log")
    axes.set_xlabel(r"$L_{bol} (L_{solar})$")
    plt.savefig("L_bol_hist.png")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
