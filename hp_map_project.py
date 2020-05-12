#!/usr/bin/python3
'''
Abstract:
    This is a script to cut a small piece from healpix map and converted to wcs coordinate. 
Usage:
    hp_map_project.py [option file] [map name]
Output:
    1. The image of dustmap on a given location.
    2. The option file
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
20200505 version alpha 2:
    1. Update the arguement implementation.
'''
import time
import matplotlib.pyplot as plt
import numpy as np
import healpy as hp
from sys import argv
from os import system

from astropy.io import fits
from astropy.coordinates import SkyCoord 
from astropy.wcs import WCS
from astropy import units as u
from input_lib import option_hp_map_project
from hpproj import hp_project

def hp_project_script(hp_hdu, coord, shape_out, frame, alpha, delta):
    #-------------------------------------------------
    # Cut a small piece from the map, taking LMC and SMC for example
    # examples of coordinates
    # coord_LMC = SkyCoord("05:23:34.60", "-69:45:22.0", unit=(u.hourangle, u.deg))
    # coord_SMC = SkyCoord("00h52m38s", "-72:48:01", unit=(u.hourangle, u.deg))
    # coord_Perseus = SkyCoord(54, 31.5, frame = 'icrs', unit = 'deg')
    # coord_CHA_II = SkyCoord(195, -77, frame = 'icrs', unit = 'deg')
    pixsize = hp.nside2resol(hp_hdu.header['NSIDE'], arcmin=True) / 60 / 4
    hdu = hp_project(
        hp_hdu,
        coord,
        pixsize=pixsize, 
        shape_out = shape_out,
        projection = ("EQUATORIAL", "TAN"),
    )
    plt.title("healpix {0} at ({1}, {2})".format(frame, alpha, delta))
    cut_data = hdu.data
    cut_w = WCS(hdu.header)
    fig = plt.subplot(111, projection = cut_w)
    ax = plt.imshow(cut_data)
    cbar = plt.colorbar(ax)
    cbar.set_label(hp_hdu.header['UNIT'], rotation=270, labelpad=15)
    plt.savefig("healpix_{0}_{1}_{2}.png".format(frame, alpha, delta))
    hdu.writeto("healpix_{0}_{1}_{2}.fits".format(frame, alpha, delta), overwrite = True)
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-------------------------------------------------
    # Load arguemnts
    # Argument Assistent (aa)
    default_option_file_name = 'option_hp_map_project.txt'
    aa = option_hp_map_project(default_option_file_name)
    if len(argv) != 3:
        print("The number of arguments is wrong.")
        print("Usage: hp_map_project.py [option file] [map name]")
        print("Please edit option file (option_hp_map_project.txt) before execution.")
        aa.create()
        exit()
    option_file_name = argv[1]
    map_name = argv[2]
    # Load detail options from option file.
    option_list = aa.load(option_file_name)
    frame = option_list[0]
    alpha = option_list[1]
    delta = option_list[2]
    ds9_width = option_list[3]
    ds9_height = option_list[4]
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
    # Initialize the target coordinate
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
    #shape_out = (height, width)
    #shape_out = (1024,1024) # Perseus
    #shape_out = (512,1024) # Ophiuchus
    #shape_out = (512,512) # Lupus I
    #shape_out = (300,300) # Lupus III
    #shape_out = (128,150) # Lupus IV
    #shape_out = (2048, 2048)
    #shape_out = (300,200) # Serpens
    #shape_out = (300,256) # Chamaeleon
    shape_out = (int(ds9_height), int(ds9_width))
    print("pixel size = {0}".format(pixsize))
    print("image size = {0} x {1} deg^2".format(
        shape_out[0]*pixsize, 
        shape_out[1]*pixsize
    ))
    #-------------------------------------------------
    # Show the first 10 rows as example.
    print("The shape of loaded map is {0}".format(DL07_paras.shape))
    max_DL07_paras = np.amax(DL07_paras)
    min_DL07_paras = np.amin(DL07_paras)
    print("Maximum: {0}".format(max_DL07_paras))
    print("Minimum: {0}".format(min_DL07_paras))
    #-------------------------------------------------
    # Cut a small piece from the map, taking LMC and SMC for example
    hp_project_script(hp_hdu, coord, shape_out, frame, alpha, delta)
    # Rename the option file
    new_name = 'healpix_{0}_{1}_{2}_option.txt'.format(frame, alpha, delta)
    cmd_line = 'cp {0} {1}'.format( 
        option_file_name,
        new_name)
    system(cmd_line)
    print("The option file has been renamed from '{0}' to '{1}'".format(
        option_file_name,
        new_name))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
