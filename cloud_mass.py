#!/usr/bin/python3
'''
Abstract:
    This is a program to calculate the cloud mass based on column density map and extintion map.
Usage:
    cloud_mass.py [column density map] [extinction map]
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
import numpy as np

from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area
from astropy.coordinates import SkyCoord
from astropy import units as u

def calc_cloud_mass(col, mask, pix_area_deg2, distance_pc):
    # distance in pc
    print("---")
    selected_col = col[mask]
    sum_col_M_kpc2 = np.sum(selected_col)
    # Trial 1
    sum_col_M_sr = sum_col_M_kpc2 * (distance_pc/1000)**2
    sum_col_M_deg2 = sum_col_M_sr * (np.pi**2) / (180**2)
    cloud_dust_mass = sum_col_M_deg2 * pix_area_deg2
    # Trial 2
    pix_area_sr = pix_area_deg2 * (np.pi**2) / (180**2)
    pix_area_kpc2 = pix_area_sr * (distance_pc/1000)**2
    cloud_dust_mass_2 = sum_col_M_kpc2 * pix_area_kpc2
    # Not related
    mask_area_pc2 = pix_area_deg2 * (np.pi**2) / (180**2) * (distance_pc)**2 * len(selected_col)
    #-----------------------------------------------------------
    # Print the answer
    if len(selected_col) == 0:
        print("No data available under this threshold.")
        return
    print("max selected_col: {0}".format(np.max(selected_col)))
    print("num of pixel: {0}".format(len(selected_col)))
    print("sum_col_M_kpc2: {0}".format(sum_col_M_kpc2))
    print("pix_area_deg2: {0}".format(pix_area_deg2))
    print("mask_area_deg2: {0}".format(pix_area_deg2 * len(selected_col)))
    print("mask_area_pc2: {0}".format(mask_area_pc2))
    print("dust mass: {0} M_sun".format(cloud_dust_mass))
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: cloud_mass.py [column density] [extinction map]" )
        exit()
    col_den_name = argv[1]
    Av_name = argv[2]
    print("Arguments:\n{0}".format(argv))
    #--------------------------------------------
    # Load image
    hdu_col = fits.open(col_den_name)
    col = hdu_col[1].data 
    h_col = hdu_col[1].header 
    w_col = WCS(h_col)
    hdu_Av = fits.open(Av_name)
    Av = hdu_Av[1].data 
    h_Av = hdu_Av[1].header 
    w_Av = WCS(h_Av)
    #--------------------------------------------
    # Initialize the parameters
    pix_area_in_deg2_col = abs(h_col['CDELT1'] * h_col['CDELT2']) 
    pix_area_in_deg2_Av = abs(h_Av['CDELT1'] * h_Av['CDELT2'])
    #--------------------------------------------
    # Given cloud distance
    #--------------
    # c2d provides:
    perseus_distance = 250
    # For Aquila, Serpens
    serpens_distance = 260
    chamaeleon_2_distance = 178
    ophiuchus_distance = 125
    lupus_distance = 150
    lupus_3_distance = 200
    #--------------
    # Gould belt provides:
    chamaeleon_13_distance = 200
    auriga_distance = 300
    cepheus_distance = 300
    corona_australis_distance = 130
    ic5146_distance = 950
    musca_distance = 160
    scorpius_distance = 130
    #--------------
    # Zucker+20 provides:
    ara_distance = 1055
    cb28_distance = 398
    cb29_distance = 374
    cb34_distance = 1322
    cma_ob1_distance = 1169
    california_distance = 436
    cam_distance = 235 # Camelopardalis
    carina_distance = 2500
    gem_ob1_distance = 1865
    hercules_3_distance = 230
    ic1396_distance = 916
    ic2118_distance = 328
    # Take one of above.
    distance = ic2118_distance 
    # Estimate the cloud mass
    print("distance (pc): {0}".format(distance))
    levels = [2, 4, 9, 12, 18] 
    linewidths = [2, 1.5, 1.5, 1.5, 1.5]
    colors = ['k', 'r', 'k', 'b', 'k']
    print("Av levels: \n{0}".format(levels))
    for level in levels:
        Av_mask = np.where(Av > level)
        calc_cloud_mass(col, Av_mask, pix_area_in_deg2_col, distance)
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
    plt.savefig("{0}_Av_contour.png".format(col_den_name[:-5]))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
