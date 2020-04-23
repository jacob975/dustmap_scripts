#!/usr/bin/python3
'''
Abstract:
    Plot the mid-infrared luminosity histogram with the given table.
Usage:
    plot_L_mir_hist.py [paras of luminosity func.] [Q labels]
Output:
    A histogram of luminosity.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200422
####################################
update log
20200421 version alpha 1:
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
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_L_hist.py [paras of luminosity func.] [Q labels]") 
        exit()
    paras_array_name = argv[1]
    Q_name = argv[2]
    #-----------------------------------------
    # Load data
    # paras_array
    # alpha, L_mir, L_bol
    paras_array = np.loadtxt(paras_array_name, dtype = float)
    # Q_array
    # Quality flag of 8 bands.
    Q_array = np.loadtxt(Q_name, dtype = str)
    #-----------------------------------------
    # List 1: All sources
    L_mir_list_1 = paras_array[:, 1]
    # List 2: Source without saturation. 
    index_non_saturated = find_non_saturated(Q_array)
    L_mir_list_2 = paras_array[index_non_saturated, 1]
    #-----------------------------------
    # Plot the histogram
    fig, axes = plt.subplots(figsize = (8,6))
    plt.hist(
        L_mir_list_1,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'k',
        label = "All sources"
    )
    plt.hist(
        L_mir_list_2,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'g',
        label = "Non-saturated sources"
    )
    axes.legend()
    axes.set_xscale("log")
    axes.set_xlabel(r"$L_{mir} (L_{solar})$")
    plt.savefig("L_mir_hist.png")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
