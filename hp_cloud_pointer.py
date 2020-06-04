#!/usr/bin/python3
'''
Abstract:
    This is a script to cut a small piece from healpix map and converted to wcs coordinate.
    Then it point out the position provided in cloud coordinate file. 
Usage:
    hp_cloud_pointer.py [cloud list] [cloud name] [map name]
Output:
    1. The image of dustmap on a given location with cloud center denoted.
    2. The option file
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200528
####################################
update log
20200528 version alpha 1:
    1. The code works.
'''
import time
import matplotlib.pyplot as plt
from  matplotlib.colors import LogNorm
import numpy as np
import healpy as hp
from sys import argv
from os import system

from astropy.io import fits
from astropy.coordinates import SkyCoord 
from astropy.wcs import WCS
from astropy import units as u
from input_lib import option_hp_cloud_pointer
from hpproj import hp_project

def hp_project_script(hp_hdu, cnt_coord, cloud_ra_list, cloud_dec_list, shape_out, cloud_name): 
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
        cnt_coord,
        pixsize=pixsize, 
        shape_out = shape_out,
        #projection = ("EQUATORIAL", "TAN"),
        projection = ("GALACTIC", "TAN"),
    )
    plt.title(
        "healpix {0} at ({1}, {2})".format(
            'icrs', 
            cnt_coord.icrs.ra.degree, 
            cnt_coord.icrs.dec.degree))
    cut_data = hdu.data
    cut_w = WCS(hdu.header)
    # Plot the figure
    fig = plt.figure(figsize = (6,6))
    ax = fig.add_axes([0.09, 0.16, 0.84, 0.70], projection = cut_w)
    #ax = plt.subplot(111, projection = cut_w) 
    img = plt.imshow(
        cut_data,
        norm = LogNorm(
            vmax = np.max(cut_data),
            vmin = np.min(cut_data)
        )
    )
    ax.set_xlabel('Galactic longitude')
    ax.set_ylabel('Galactic latitude')
    plt.grid(color='white', ls='solid')
    # Draw galactic coordinate
    overlay = ax.get_coords_overlay('icrs')
    overlay.grid(color='white', ls='dotted')
    overlay[0].set_axislabel('Right Ascention')
    overlay[1].set_axislabel('Declination')
    # Denote all cloud center on image
    ax.scatter(
        cloud_ra_list, 
        cloud_dec_list,
        marker = 'X',
        c = 'r', 
        transform=ax.get_transform('icrs')
    )
    # Set colorbar.
    cbar_ax = fig.add_axes([0.09, 0.06, 0.84, 0.02])
    cbar = plt.colorbar(img, cax = cbar_ax, orientation="horizontal")
    cbar.set_label(hp_hdu.header['UNIT'], labelpad=15)
    plt.savefig("healpix_{0}.png".format(cloud_name))
    hdu.writeto("healpix_{0}.fits".format(cloud_name), overwrite = True)
    return

def coord_np2sky(alpha, delta, frame):
    if frame == 'icrs':
        coord = SkyCoord(float(alpha), float(delta), frame = 'icrs', unit = 'deg')
    elif frame == 'galactic':
        coord = SkyCoord(float(alpha), float(delta), frame = 'galactic', unit = 'deg')
    else:
        print("The given frame is not available.")
        print("Please use 'icrs' or 'galactic'.")
        exit()
    return coord

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-------------------------------------------------
    # Load arguemnts
    # Argument Assistent (aa)
    default_cloud_list_name = 'option_hp_cloud_pointer.txt'
    aa = option_hp_cloud_pointer(default_cloud_list_name)
    if len(argv) != 4:
        print("The number of arguments is wrong.")
        print("Usage: hp_cloud_pointer.py [cloud list] [map name]")
        print("Please edit option file ({0}) before execution.".format(default_cloud_list_name))
        aa.create()
        exit()
    cloud_list_name = argv[1]
    cloud_name = argv[2]
    map_name = argv[3]
    # Load detail options from option file.
    cloud_list = aa.load(cloud_list_name)
    print (cloud_list)
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
    cloud_skycoord_list = []
    cloud_ra_list = []
    cloud_dec_list = []
    for c in cloud_list:
        coord = coord_np2sky(c[0], c[1], c[2])
        cloud_skycoord_list.append(coord)
        cloud_ra_list.append(coord.icrs.ra.deg)
        cloud_dec_list.append(coord.icrs.dec.deg)
    center_ra = np.mean(cloud_ra_list)
    center_dec = np.mean(cloud_dec_list)
    center_coord = coord_np2sky(center_ra, center_dec, 'icrs')
    print('--- center ---')
    print(center_coord)
    print('--- cloud list ---')
    print(cloud_skycoord_list)
    #--------------------------------------------------
    # Determine the image `location` and `size` by using the mean position of all cloud center.
    pixsize = hp.nside2resol(hp_hdu.header['NSIDE'], arcmin=True) / 60 / 4
    
    offset_list = []
    for c in cloud_skycoord_list:
        offset = c.separation(center_coord)
        offset_list.append(offset.degree)
    offset_array = np.array(offset_list, dtype = float)
    max_offset = np.amax(offset_array)
    print(max_offset)
    size_pix_num = 2 * max_offset/pixsize + 100 
    #shape_out = (int(ds9_height), int(ds9_width))
    shape_out = (int(size_pix_num), int(size_pix_num))
    # Print the size information
    print("pixel size = {0}".format(pixsize))
    print("image size = {0} x {1} deg^2".format(
        shape_out[0]*pixsize, 
        shape_out[1]*pixsize
    ))
    print("The shape of loaded map is {0}".format(DL07_paras.shape))
    max_DL07_paras = np.amax(DL07_paras)
    min_DL07_paras = np.amin(DL07_paras)
    print("Maximum: {0}".format(max_DL07_paras))
    print("Minimum: {0}".format(min_DL07_paras))
    #-------------------------------------------------
    # Cut a small piece from the map, taking LMC and SMC for example
    hp_project_script(hp_hdu, center_coord, cloud_ra_list, cloud_dec_list, shape_out, cloud_name)
    # Rename the option file
    new_name = 'healpix_{0}_option.txt'.format(cloud_name)
    cmd_line = 'cp {0} {1}'.format( 
        cloud_list_name,
        new_name)
    system(cmd_line)
    print("The option file has been renamed from '{0}' to '{1}'".format(
        cloud_list_name,
        new_name))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
