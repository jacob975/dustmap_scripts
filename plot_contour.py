#!/usr/bin/python3
'''
Abstract:
    This is a program to plot the contour of input image. 
Usage:
    plot_contour.py [input fits] 
Output:
    2. The PNG of selected contour.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200429
####################################
update log
20200429 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib.pyplot as plt
from  matplotlib.colors import LogNorm
import numpy as np

from astropy.io import fits
from astropy.wcs import WCS

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_contour.py [input fits]" )
        exit()
    fits_name = argv[1]
    print("Arguments:\n{0}".format(argv))
    #--------------------------------------------
    # Load image
    hdu = fits.open(fits_name)
    data = hdu[0].data
    hdr = hdu[0].header
    w = WCS(hdr)
    #--------------------------------------------
    # Set contour levels
    levels = [2, 4, 12] 
    linewidths = [2, 1.5, 1.5]
    colors = ['k', 'r', 'b']
    print("Contour levels: \n{0}".format(levels))
    #--------------------------------------------
    # Plot the contour
    plt.figure(figsize=(10,5))
    axes = plt.subplot(111, projection = w)
    ax = plt.imshow(data)
    cbar = plt.colorbar(ax)
    plt.contour(
        data, 
        levels = levels,
        linewidths = linewidths,
        colors = colors,   
    )
    plt.savefig("{0}_contour.png".format(fits_name[:-5]))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
