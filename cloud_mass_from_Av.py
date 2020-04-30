#!/usr/bin/python3
'''
Abstract:
    This is a program to calculate the cloud mass based on Av map (Enoch et al. 2006). 
Usage:
    cloud_mass_from_Av.py [extinction map]
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

20200430
####################################
update log
20200430 version alpha 1:
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

# Based on Enoch et al. 2006
def calc_cloud_mass(Av, mask, pix_area_deg2, distance_pc):
    # constants
    mu_H2 = 2.8
    m_H = 1.674e-24
    pc_in_cm  = 3.086e18
    solar_mass_in_g = 1.989e33
    # distance in pc
    print("---")
    selected_Av = Av[mask]
    col_H2num_cm2 = 0.94e21 * selected_Av # unit: cm^-2
    sum_col_H2num_cm2 = np.sum(col_H2num_cm2)
    sum_col_M_cm2 = sum_col_H2num_cm2 * mu_H2 * m_H
    # Trial 1
    sum_col_M_sr = sum_col_M_cm2 * (distance_pc*pc_in_cm)**2
    sum_col_M_deg2 = sum_col_M_sr * (np.pi**2) / (180**2)
    cloud_dust_mass = sum_col_M_deg2 * pix_area_deg2 / solar_mass_in_g
    # Trial 2
    pix_area_sr = pix_area_deg2 * (np.pi**2) / (180**2)
    pix_area_cm2 = pix_area_sr * (distance_pc*pc_in_cm)**2
    cloud_dust_mass_2 = sum_col_M_cm2 * pix_area_cm2 / solar_mass_in_g
    # Not related
    mask_area_pc2 = pix_area_deg2 * (np.pi**2) / (180**2) * (distance_pc)**2 * len(selected_Av)
    #-----------------------------------------------------------
    # Print the answer
    print("max selected_Av: {0}".format(np.max(selected_Av)))
    print("num of pixel: {0}".format(len(selected_Av)))
    print("sum_col_M_cm2: {0}".format(sum_col_M_cm2))
    print("pix_area_deg2: {0}".format(pix_area_deg2))
    print("mask_area_deg2: {0}".format(pix_area_deg2 * len(selected_Av)))
    print("mask_area_pc2: {0}".format(mask_area_pc2))
    print("dust mass: {0} M_sun".format(cloud_dust_mass))
    print("dust mass 2: {0} M_sun".format(cloud_dust_mass_2))
    return

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: cloud_mass_from_Av.py [extinction map]" )
        exit()
    Av_name = argv[1]
    print("Arguments:\n{0}".format(argv))
    #--------------------------------------------
    # Load image
    hdu_Av = fits.open(Av_name)
    Av = hdu_Av[1].data 
    h_Av = hdu_Av[1].header 
    w_Av = WCS(h_Av)
    #--------------------------------------------
    # Initialize the parameters
    pix_area_in_deg2_Av = abs(h_Av['CDELT1'] * h_Av['CDELT2'])
    # for c2d 240arcsec extinction maps
    #pix_area_in_deg2_Av = np.power(np.divide(40, 3600), 2)
    # for Planck extinction maps
    #pix_area_in_deg2_Av = np.power(np.divide(25.7661, 3600), 2)
    #--------------------------------------------
    # Given cloud distance
    # c2d provides:
    perseus_distance = 250
    serpens_distance = 260
    chamaeleon_distance = 178
    ophiuchus_distance = 125
    lupus_distance = 150
    lupus_3_distance = 200
    # Take one of above.
    distance = perseus_distance 
    # Estimate the cloud mass
    print("distance (pc): {0}".format(distance))
    levels = [2, 4, 12] 
    linewidths = [2, 1.5, 1.5]
    colors = ['k', 'r', 'b']
    print("Av levels: \n{0}".format(levels))
    for level in levels:
        Av_mask = np.where(Av > level)
        calc_cloud_mass(Av, Av_mask, pix_area_in_deg2_Av, distance)
    #--------------------------------------------
    # Plot the contour
    plt.figure(figsize=(10,8))
    axes = plt.subplot(111, projection = w_Av)
    ax = plt.imshow(Av)
    cbar = plt.colorbar(ax)
    cbar.set_label("Av (mag)", rotation = 270, labelpad = 15)
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
