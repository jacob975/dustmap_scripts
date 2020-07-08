#!/usr/bin/python3
'''
Abstract:
    Plot the flux histogram with the given table.
Usage:
    plot_flux_hist.py [SED table] [Q labels] [SED2 table] [Q2 labels]
Output:
    Histograms of flux.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200501 
####################################
update log
20200501 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv
import numpy as np
from matplotlib import pyplot as plt

def plot_hist(inp_flux, inp_Q, inp_flux2, inp_Q2, band_number):
    non_saturated_inp_flux = inp_flux[inp_Q != 'S']
    #-----------------------------------
    # Plot the histogram
    fig, axes = plt.subplots(figsize = (8,6))
    """
    plt.hist(
        inp_flux,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        #alpha = 0.5,
        color = 'k',
        label = "SEIP sources",
        zorder = 11,
    )
    """
    plt.hist(
        non_saturated_inp_flux,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        #alpha = 0.5,
        color = 'g',
        histtype = 'step',
        label = "Non-saturated SEIP sources",
        zorder = 12,
    )
    plt.hist(
        inp_flux2,
        bins = np.logspace(-4, 4, num = 17),
        lw = 3,
        #alpha = 0.5,
        color = 'c',
        histtype = 'step',
        label = "c2d sources",
        zorder = 10,
    )
    axes.legend()
    axes.set_xscale("log")
    axes.set_yscale("log")
    axes.set_xlabel("flux (mJy)")
    axes.set_ylabel("Number of sources (counts)")
    plt.savefig("flux_hist_{0}.png".format(band_number))
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
        print ("Usage: plot_flux_hist.py [SED table] [Q labels] [SED2 table] [Q2 labels]") 
        exit()
    sed_name = argv[1]
    Q_name = argv[2]
    sed2_name = argv[3]
    Q2_name = argv[4]
    #-----------------------------------------
    # Load data
    # SED data
    # J, H, K, IR1, IR2, IR3, IR4, and MP1 in mJy
    sed_array = np.loadtxt(sed_name, dtype = float)
    sed2_array = np.loadtxt(sed2_name, dtype = float)
    # Q_array
    # Quality flag of 8 bands.
    Q_array = np.loadtxt(Q_name, dtype = str)
    Q2_array = np.loadtxt(Q2_name, dtype = str)
    num_band = len(Q_array[0])
    #-----------------------------------------
    for i in range(num_band):
        print('# Round {0}'.format(i))
        inp_flux = sed_array[:,i]
        inp_Q = Q_array[:,i]
        inp_flux2 = sed2_array[:,i]
        inp_Q2 = Q2_array[:,i]
        plot_hist(inp_flux, inp_Q, inp_flux2, inp_Q2, i)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
