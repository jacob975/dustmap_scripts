#!/usr/bin/python3
'''
Abstract:
    This is a script to perform a quick aperture photometry on map with given location. 
Usage:
    hp_map_photometry.py [healpix map] icrs [RA] [DEC]
    or
    hp_map_photometry.py [healpix map] galactic [l] [b]
Output:
    1. Print The result of photometry. 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200408
####################################
update log
20200408 version alpha 1:
    1. The code works.
'''
import time
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from sys import argv

from astropy.io import fits
from astropy.coordinates import Angle, SkyCoord 
from astropy.wcs import WCS
from astropy import units as u

from hpproj import hp_project
from hpproj import hp_photometry
from hp_map_project import hp_project_script
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-------------------------------------------------
    # Load arguemnts
    if len(argv) != 5:
        print("The number of arguments is wrong.")
        print("Usage: hp_map_photometry.py [healpix map] icrs [RA] [DEC]")
        print("or")
        print("hp_map_photometry.py [healpix map] galactic [l] [b]")
        exit()
    map_name = argv[1]
    frame = argv[2]
    alpha = argv[3]
    delta = argv[4]
    #-------------------------------------------------
    # Load map
    DL07_paras, hp_header = hp.read_map(
        map_name,
        # field indicates which column you choose to load, starting from 0.
        field = 0,
        h = True,
        nest=None,
    )
    hp_hdu = fits.ImageHDU(DL07_paras, fits.Header(hp_header))
    hp_hdu.header['UNIT'] = r"$M_{sun}/kpc^2$"
    # Show the header of this map.
    hdul = fits.open(map_name)
    hdul.info()
    hdr = hdul[1].header
    print("### HEADER for this map ###")
    print(repr(hdr))
    print("### END of HEADER ###") 
    #--------------------------------------------------
    # Initialize
    # The target coordinate
    if frame == 'icrs':
        coord = SkyCoord(float(alpha), float(delta), frame = 'icrs', unit = 'deg')
    elif frame == 'galactic':
        coord = SkyCoord(float(alpha), float(delta), frame = 'galactic', unit = 'deg')
    else:
        print("The given frame is not available.")
        print("Please use 'icrs' or 'galactic'.")
        exit()
    # Image size
    pixsize = hp.nside2resol(hp_hdu.header['NSIDE'], arcmin=True) / 60 / 4
    shape_out = (768,768)
    print("pixel size = {0}".format(pixsize))
    print("image size = {0} x {1} deg^2".format(
        shape_out[0]*pixsize, 
        shape_out[1]*pixsize))
    #-------------------------------------------------
    # Show the first 10 rows as example.
    print("The shape of loaded map is {0}".format(DL07_paras.shape))
    max_DL07_paras = np.amax(DL07_paras)
    min_DL07_paras = np.amin(DL07_paras)
    print("Maximum: {0}".format(max_DL07_paras))
    print("Minimum: {0}".format(min_DL07_paras))
    #-------------------------------------------------
    # Make photometry on the given location. 
    apertures = \
        Angle(hp.nside2resol(hp_hdu.header['NSIDE'], arcmin=True) / 60 / 4, "deg") \
        * [50, 70, 80]
        # [aperture radius, inner annulus radius, outer annulus radius]
        # unit: deg * npix
    print(apertures)
    result = hp_photometry(hp_hdu, coord, apertures=apertures)
    print(result)
    # Cut a small piece of map for reference.
    hp_project_script(hp_hdu, coord, shape_out, frame, alpha, delta)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
