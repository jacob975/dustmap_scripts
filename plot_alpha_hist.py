#!/usr/bin/python3
'''
Abstract:
    Plot the luminosity histogram with the given table.
Usage:
    plot_alpha_hist.py [alpha table] [cls pred]
Output:
    A histogram of power law index, alpha.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200714
####################################
update log
20200714 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv
import numpy as np
from matplotlib import pyplot as plt

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #----------------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_alpha_hist.py [alpha table] [cls pred]")
        exit()
    alpha_array_name = argv[1]
    cls_pred_name = argv[2]
    #-----------------------------------------
    # Load data
    # alpha_array
    alpha_array = np.loadtxt(alpha_array_name, dtype = float)
    cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    yso_alpha_array = alpha_array[cls_pred == 2]
    print(len(yso_alpha_array))
    #-----------------------------------
    # Plot the histogram
    fig, axes = plt.subplots(figsize = (8,6))
    plt.hist(
        yso_alpha_array,
        bins = np.linspace(-4, 4, 41),
        lw = 3,
        color = 'k',
        #label = "All sources",
        histtype = 'step',
        #normed = True,
    )
    axes.legend()
    axes.set_xlabel(r"$\alpha$")
    axes.set_ylabel("percentage(%)")
    plt.savefig("alpha_hist.png")
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
