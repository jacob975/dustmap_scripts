#!/usr/bin/python3
'''
Abstract:
    This is a script provide functions to obtain SNR from  
    COM_CompMap_Dust-DL07-Parameters_2048_R2.00.fits.
Usage:
    PLA_DL07_snr.py [healpix map]
Output:
    The SNR image of column density provided from COM_CompMap_Dust-DL07-Parameters_2048_R2.00.fits. 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200409
####################################
update log
20200409 version alpha 1:
    1. The code works.
'''
import time
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from sys import argv

from astropy.io import fits
from astropy.coordinates import SkyCoord 
from astropy.wcs import WCS
from astropy import units as u

from hpproj import hp_to_wcs
from hpproj import build_wcs_2pts
from hpproj import CutSky, to_coord
from hpproj import hp_project
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-------------------------------------------------
    # Load arguemnts
    if len(argv) != 2:
        print("The number of arguments is wrong.")
        print("Usage: PLA_DL07_snr.py [healpix map]")
        exit()
    map_name = argv[1]
    #-------------------------------------------------
    # Show the header of this map.
    hdul = fits.open(map_name)
    hdul.info()
    hdr = hdul[1].header
    print("### HEADER for this map ###")
    print(repr(hdr))
    print("### END of HEADER ###") 
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
    e_DL07_paras, e_hp_header = hp.read_map(
        map_name,
        # field indicates which column you choose to load, starting from 0.
        field = 1,
        h = True,
        nest=None,
    )
    e_hp_hdu = fits.ImageHDU(DL07_paras, fits.Header(hp_header))
    e_hp_hdu.header['UNIT'] = r"$M_{sun}/kpc^2$"
    #-------------------------------------------------
    # Draw the map
    '''
    hp.mollview(
        DL07_paras/e_DL07_paras, 
        unit="S/N",
        #norm = 'log',
        nest=True,
        min = 0,
        max = 10,
    )
    hp.graticule()
    plt.show()
    '''
    #-------------------------------------------------
    # Save the SNR all-sky map
    hp.write_map(
        "SNR.fits", 
        DL07_paras/e_DL07_paras, 
        nest = True, 
        coord = 'G',
        overwrite = True,
    ) 
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
