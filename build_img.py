#!/usr/bin/python3
'''
Abstract:
    Show the Bayestar 19 dustmap on a given location with WCS coordinate.
Usage:
    build_img.py galactic [l] [b]
    or
    build_img.py icrs [RA] [DEC]
Output:
    The image with WCS coordinate.
Editor:
    Jacob975
    People who contribute this website: https://dustmaps.readthedocs.io/en/latest/examples.html#getting-started

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200327
####################################
update log
20200327 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as units
from astropy import wcs
from astropy.io import fits
from astropy.coordinates import SkyCoord

from dustmaps.planck import PlanckQuery
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
        print ("Usage: build_img.py icrs [RA] [DEC]")
        print ("Or: build_img.py galactic [l] [b]")
        exit()
    frame = argv[1]
    alpha = argv[2]
    delta = argv[3]
    #--------------------------------------------
    # Initialization
    # size of dustmap (degree)
    alpha_size = 5
    delta_size = 1.5
    diag_size = np.sqrt(alpha_size**2 + delta_size**2)
    step = 0.01
    # catalog can be PL13, BS19
    catalog = "PL13"
    #--------------------------------------------
    # Next, we’ll set up a grid of coordinates to plot, centered on the given location: 
    if frame == 'galactic':
        l0 = float(alpha)
        b0 = float(delta)
        xlabel = 'l(deg)'
        ylabel = 'b(deg)'
        l = np.arange(
            l0 + alpha_size, 
            l0 - alpha_size, 
            -step)
        b = np.arange(
            b0 + delta_size, 
            b0 - delta_size, 
            -step)
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
        RA = np.arange(
            RA0 + alpha_size, 
            RA0 - alpha_size, 
            -step)
        DEC = np.arange(
            DEC0 + delta_size, 
            DEC0 - delta_size, 
            -step)
        RA, DEC = np.meshgrid(RA, DEC)
        coords = SkyCoord(
            RA*units.deg, 
            DEC*units.deg,
            distance=1.*units.kpc, 
            frame=frame
        )
    #--------------------------------------------
    # Then, we’ll load up and query three different dust maps:
    Av = None
    if catalog == "PL13":
        planck = PlanckQuery()
        Av = 3.1 * planck(coords)
    if catalog == "BS19":
        bayestar = BayestarQuery(max_samples=1)
        Av = 2.742 * bayestar(coords)
    #--------------------------------------------
    # We’ve assumed RV=3.1, and used the coefficient from Table 6 of Schlafly & Finkbeiner (2011) 
    # to convert SFD and Bayestar reddenings to magnitudes of AV.
    #
    # Finally, we make a image with WCS coordinate.
    # Create a new WCS object.  The number of axes must be set
    # from the start
    w = wcs.WCS(naxis=2) 
    # Set up an "Airy's zenithal" projection
    # Vector properties may be set with Python lists, or Numpy arrays
    w.wcs.crpix = [alpha_size//step, delta_size//step]
    w.wcs.cdelt = np.array([-step, step])
    w.wcs.crval = [float(alpha), float(delta)]
    w.wcs.radesys = frame
    # MER means Mercator’s projection
    # You can find more available projection from here: 
    # https://docs.astropy.org/en/stable/wcs/
    w.wcs.ctype = ["RA---CAR", "DEC--CAR"]
    w.wcs.set_pv([(2, 1, 0.0)])
    #-----------------------------------
    # Save the image
    header = w.to_header()
    print(Av.shape)
    image = Av[::-1]
    fits.writeto(
        "{0}_{1}_{2}_{3}.fits".format(
            catalog,
            frame, 
            alpha, 
            delta), 
        image, 
        header, 
        overwrite = True
    )
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
