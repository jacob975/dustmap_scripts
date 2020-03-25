#!/usr/bin/python3
'''
Abstract:
    Show the Bayestar 19 dustmap on a given location, 10x10 deg square.
Usage:
    show_dustmaps.py galactic [l] [b]
    or
    show_dustmaps.py icrs [RA] [DEC]
Output:
    The picture that compare different dustmap on a given location.
Editor:
    Jacob975
    People who contribute this website: https://dustmaps.readthedocs.io/en/latest/examples.html#getting-started

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200325
####################################
update log
20200325 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as units
from astropy.coordinates import SkyCoord

from dustmaps.bayestar import BayestarQuery
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage: cmp_dustmaps.py icrs [RA] [DEC]")
        print ("Or: cmp_dustmaps.py galactic [l] [b]")
        exit()
    frame = argv[1]
    alpha = argv[2]
    delta = argv[3]
    #--------------------------------------------
    # Initialization
    # size of dustmap (degree)
    alpha_size = 2.5
    delta_size = 1
    #--------------------------------------------
    # Next, we’ll set up a grid of coordinates to plot, centered on the given location: 
    if frame == 'galactic':
        l0 = float(alpha)
        b0 = float(delta)
        xlabel = 'l(deg)'
        ylabel = 'b(deg)'
        extent = [
            l0+alpha_size, 
            l0-alpha_size, 
            b0-delta_size, 
            b0+delta_size
        ]
        # e.g. Aquila South cloud
        # l0, b0 = (37., -16.)
        l = np.arange(
            l0 + alpha_size, 
            l0 - alpha_size, 
            -0.05)
        b = np.arange(
            b0 + delta_size, 
            b0 - delta_size, 
            -0.05)
        l, b = np.meshgrid(l, b)
        coords = SkyCoord(
            l*units.deg, 
            b*units.deg,
            distance=1.*units.kpc, 
            frame=frame
        )
    elif frame == 'icrs':
        RA0 = float(alpha)
        DEC0 = float(delta)
        xlabel = 'RA(deg)'
        ylabel = 'DEC(deg)'
        extent = [
            RA0+alpha_size, 
            RA0-alpha_size, 
            DEC0-delta_size, 
            DEC0+delta_size]
        RA = np.arange(
            RA0 + alpha_size, 
            RA0 - alpha_size, 
            -0.05)
        DEC = np.arange(
            DEC0 + delta_size, 
            DEC0 - delta_size, 
            -0.05)
        RA, DEC = np.meshgrid(RA, DEC)
        coords = SkyCoord(
            RA*units.deg, 
            DEC*units.deg,
            distance=1.*units.kpc, 
            frame=frame
        )
    #--------------------------------------------
    # Then, we’ll load up and query three different dust maps:
    bayestar = BayestarQuery(max_samples=1)
    Av = 2.742 * bayestar(coords)
    #--------------------------------------------
    # We’ve assumed RV=3.1, and used the coefficient from Table 6 of Schlafly & Finkbeiner (2011) 
    # to convert SFD and Bayestar reddenings to magnitudes of AV.
    #
    # Finally, we create the figure using matplotlib:
    fig, ax = plt.subplots(
        figsize = (8, 6), 
        dpi = 150
    )
    cs = ax.imshow(
        np.sqrt(Av)[::-1],
        vmin=0.,
        vmax=2.,
        origin='lower',
        interpolation='nearest',
        cmap='binary',
        aspect='equal',
        extent = extent,
    )
    plt.colorbar(cs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(
        'Bayestar 19 dust map on {0} ({1},{2})'.format(
            frame, 
            alpha, 
            delta
        )
    ) 
    fig.subplots_adjust(wspace=0., hspace=0.)
    plt.savefig('BS19_on_{0}_{1}_{2}.png'.format(frame, alpha, delta), dpi=150)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
