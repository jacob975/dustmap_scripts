#!/usr/bin/python3
'''
Abstract:
    Plot the flux histogram with two given table.
Usage:
    plot_cmp_flux_hist.py [SED table] [Q labels]
Output:
    Histograms of two flux sampling.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200504 
####################################
update log
20200504 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv
import numpy as np
from matplotlib import pyplot as plt

def plot_cmp_hist(inp_1_flux, inp_1_Q, inp_2_flux, inp_2_Q, band_number):
    #non_saturated_inp_flux = inp_flux[inp_Q != 'S']
    #-----------------------------------
    # Plot the histogram
    fig, axes = plt.subplots(figsize = (8,6))
    plt.hist(
        inp_1_flux,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'k',
        label = "sample 1 sources"
    )
    plt.hist(
        inp_2_flux,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        alpha = 0.5,
        color = 'g',
        label = "sample 2 sources"
    )
    axes.legend()
    axes.set_xscale("log")
    axes.set_yscale("log")
    axes.set_xlabel("flux (mJy)")
    plt.savefig("flux_cmp_hist_{0}.png".format(band_number))
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #----------------------------------------
    # Load argv
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_cmp_flux_hist.py [SED 1 table] [Q 1 labels] [SED 2 table] [Q 2 table]") 
        exit()
    sed_1_name = argv[1]
    Q_1_name = argv[2]
    sed_2_name = argv[3]
    Q_2_name = argv[4]
    #-----------------------------------------
    # Load data
    # SED data
    # J, H, K, IR1, IR2, IR3, IR4, and MP1 in mJy
    sed_1_array = np.loadtxt(sed_1_name, dtype = float)
    sed_2_array = np.loadtxt(sed_2_name, dtype = float)
    # Q_array
    # Quality flag of 8 bands.
    Q_1_array = np.loadtxt(Q_1_name, dtype = str)
    Q_2_array = np.loadtxt(Q_2_name, dtype = str)
    num_band = len(Q_1_array[0])
    #-----------------------------------------
    for i in range(num_band):
        print('# Round {0}'.format(i))
        inp_1_flux = sed_1_array[:,i]
        inp_2_flux = sed_2_array[:,i]
        inp_1_Q = Q_1_array[:,i]
        inp_2_Q = Q_2_array[:,i]
        plot_cmp_hist(inp_1_flux, inp_1_Q, inp_2_flux, inp_2_Q, i)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
