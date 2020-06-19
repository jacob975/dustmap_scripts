#!/usr/bin/python3
'''
Abstract:
    This is a program to calculate the cloud mass based on column density map and extintion map.
Usage:
    cloud_mass.py [contour config] [cloud name] [column density map] [extinction map]
    column density map unit: M_sun / kpc^2
    extinction map unit: Av in mag
Output:
    1. Print the number of total flux
    2. The PNG of selected regions with Av contour.
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
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib.pyplot as plt
from  matplotlib.colors import LogNorm
from uncertainties import unumpy, ufloat
import numpy as np

from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area
from astropy.coordinates import SkyCoord
from astropy import units as u

from input_lib import option_Av_region_paras
import dist_lib

def calc_cloud_mass(col, e_col, mask, pix_area_deg2, u_distance_pc):
    # distance in pc
    print("---")
    selected_col = col[mask]
    e_selected_col = e_col[mask]
    u_selected_col = unumpy.uarray(selected_col, e_selected_col)
    u_sum_col_M_kpc2 = u_selected_col.sum() 
    # Trial 1
    u_sum_col_M_sr = u_sum_col_M_kpc2 * (u_distance_pc/1000)**2
    u_sum_col_M_deg2 = u_sum_col_M_sr * (np.pi**2) / (180**2)
    u_cloud_dust_mass = u_sum_col_M_deg2 * pix_area_deg2
    # Trial 2
    pix_area_sr = pix_area_deg2 * (np.pi**2) / (180**2)
    u_pix_area_kpc2 = pix_area_sr * (u_distance_pc/1000)**2
    u_cloud_dust_mass_2 = u_sum_col_M_kpc2 * u_pix_area_kpc2
    # Not related
    u_mask_area_pc2 = pix_area_deg2 * (np.pi**2) / (180**2) * (u_distance_pc)**2 * len(selected_col)
    #-----------------------------------------------------------
    # Print the answer
    if len(selected_col) == 0:
        print("No data available under this threshold.")
        return
    print("max selected_col: {0}".format(np.max(selected_col)))
    print("num of pixel: {0}".format(len(selected_col)))
    print("sum_col_M_kpc2: {0}".format(u_sum_col_M_kpc2))
    print("pix_area_deg2: {0}".format(pix_area_deg2))
    print("mask_area_deg2: {0}".format(pix_area_deg2 * len(selected_col)))
    print("mask_area_pc2: {0}".format(u_mask_area_pc2))
    print("dust mass: {0} M_sun".format(u_cloud_dust_mass))
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Initialize the arguments
    default_contour_config_name = "contour_config.txt"
    # aa stands for Arguement Assistent
    aa = option_Av_region_paras(default_contour_config_name)
    #-----------------------------------
    # Load argv
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: cloud_mass.py [contour_config] [cloud name] [column density] [extinction map]" )
        aa.create()
        exit()
    contour_config_name = argv[1]
    cloud_name = argv[2]
    col_den_name = argv[3]
    Av_name = argv[4]
    print("Arguments:\n{0}".format(argv))
    #--------------------------------------------
    # Load image
    hdu_col = fits.open(col_den_name)
    col = hdu_col[1].data 
    e_col = hdu_col[2].data 
    h_col = hdu_col[1].header 
    w_col = WCS(h_col)
    hdu_Av = fits.open(Av_name)
    Av = hdu_Av[1].data 
    h_Av = hdu_Av[1].header 
    w_Av = WCS(h_Av)
    #--------------------------------------------
    # Initialize the parameters
    # Contours
    contour_config = aa.load(contour_config_name)
    levels = np.array(contour_config[0], dtype = float)
    linewidths = np.array(contour_config[1], dtype = float)
    colors = contour_config[2]
    print("Av levels: \n{0}".format(levels))
    print("linewidth: \n{0}".format(linewidths))
    print("colors: \n{0}".format(colors))
    # Pixel Size
    pix_area_in_deg2_col = abs(h_col['CDELT1'] * h_col['CDELT2']) 
    pix_area_in_deg2_Av = abs(h_Av['CDELT1'] * h_Av['CDELT2'])
    #--------------------------------------------
    # Given cloud distance
    u_distance = dist_lib.distance_dict[cloud_name]
    # Estimate the cloud mass
    print("distance (pc): {0}".format(u_distance))
    for level in levels:
        Av_mask = np.where(Av > level)
        calc_cloud_mass(col, e_col, Av_mask, pix_area_in_deg2_col, u_distance)
    #--------------------------------------------
    # Plot the contour
    plt.figure(figsize=(10,8))
    axes = plt.subplot(111, projection = w_col)
    ax = plt.imshow(
        col, 
        norm = LogNorm(
            vmax = np.max(col),
            vmin = np.min(col)
        )
    )
    cbar = plt.colorbar(ax)
    cbar.set_label(r"$M_{sun}/kpc^{2}$", rotation = 270, labelpad = 15)
    plt.contour(
        Av, 
        levels = levels,
        linewidths = linewidths,
        colors = colors,   
    )
    plt.savefig("{0}_Av_contour.png".format(col_den_name[:-5]), dpi = 300)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
