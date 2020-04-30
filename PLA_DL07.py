#!/usr/bin/python3
'''
Abstract:
    This is a script provide functions to obtain data from the map, 
    COM_CompMap_Dust-DL07-Parameters_2048_R2.00.fits.
Usage:
    PLA_DL07.py [healpix map]
Output:
    The image of dustmap on a given location.
Editor:
    Jacob975
    People who contribute this website: https://gist.github.com/zonca/9c114608e0903a3b8ea0bfe41c96f255 

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
        print("Usage: PLA_DL07.py [healpix map]")
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
    hp_header = fits.Header(hp_header)
    hp_hdu.header['UNIT'] = r"$M_{sun}/kpc^2$"
    # Show the first 10 rows as example.
    print("The shape of loaded map is {0}".format(DL07_paras.shape))
    print(DL07_paras[:10])
    max_DL07_paras = np.amax(DL07_paras)
    min_DL07_paras = np.amin(DL07_paras)
    print("Maximum: {0}".format(max_DL07_paras))
    print("Minimum: {0}".format(min_DL07_paras))
    index_neg = np.where(DL07_paras < 1)
    DL07_paras[index_neg] = 1
    #-------------------------------------------------
    # Draw the map
    hp.mollview(
        DL07_paras, 
        unit=r"$M_{sun}/kpc^2$",
        norm = 'log',
        nest=True,
        cmap = plt.cm.get_cmap('bone'),
        max = 10,
        min = 1,
    )
    #hp.graticule()
    plt.savefig("PLA_DL07_all_sky_map.png", dpi = 600)
    #-------------------------------------------------
    # Shows the histogram of parameters
    '''
    plt.hist(DL07_paras, bins = 1000)
    plt.show()
    '''
    #-------------------------------------------------
    # Highlight a small piece on the map
    '''
    vec = hp.ang2vec(np.pi / 2, np.pi * 3 / 4)
    print(vec)
    ipix_disc = hp.query_disc(nside=2048, vec=vec, radius=np.radians(10))
    DL07_paras[ipix_disc] = DL07_paras.max()
    hp.mollview(
        DL07_paras, 
        title="Mollview image RING",
        #nest = True,
    )
    plt.show()
    '''
    #-------------------------------------------------
    # Cut a small piece from the map, taking LMC and SMC for example
    '''
    coord_LMC = SkyCoord("05:23:34.60", "-69:45:22.0", unit=(u.hourangle, u.deg))
    coord_SMC = SkyCoord("00h52m38s", "-72:48:01", unit=(u.hourangle, u.deg))
    coord_Perseus = SkyCoord(54, 31.5, frame = 'icrs', unit = 'deg')
    coord_CHA_II = SkyCoord(195, -77, frame = 'icrs', unit = 'deg')
    pixsize = hp.nside2resol(hp_hdu.header['NSIDE'], arcmin=True) / 60 / 4
    hdu = hp_project(
        DL07_paras, 
        hp_header,
        coord_Perseus,
        pixsize=pixsize, 
        shape_out=(768, 1024))
    cut_data = hdu.data
    cut_w = WCS(hdu.header)
    fig = plt.subplot(111, projection = cut_w)
    plt.imshow(cut_data)
    plt.savefig("test_2.png")
    hdu.writeto("test_2.fits", overwrite = True)
    '''
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
