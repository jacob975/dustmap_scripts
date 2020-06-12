#!/usr/bin/python3
'''
Abstract:
    This is a program to calculate the cloud mass based on column density map and extintion map.
Usage:
    Av_region_mass.py [contour config] [column density map] [extinction map]
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

20200608
####################################
update log
20200608 version alpha 1:
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

from input_lib import option_Av_region_paras
import dist_lib 

class cloud_mass_set():
    def __init__(self):
        self.distance_pc = 0.0 
        self.mask_area_deg2 = 0.0 
        self.mask_area_pc2 = 0.0 
        self.dust_mass_Msun = 0.0

def calc_cloud_mass(col, mask, pix_area_deg2, distance_pc):
    # distance in pc
    selected_col = col[mask]
    sum_col_M_kpc2 = np.sum(selected_col)
    # Trial 1
    sum_col_M_sr = sum_col_M_kpc2 * (distance_pc/1000)**2
    sum_col_M_deg2 = sum_col_M_sr * (np.pi**2) / (180**2)
    dust_mass_Msun = sum_col_M_deg2 * pix_area_deg2
    # Trial 2
    pix_area_sr = pix_area_deg2 * (np.pi**2) / (180**2)
    pix_area_kpc2 = pix_area_sr * (distance_pc/1000)**2
    cloud_dust_mass_2 = sum_col_M_kpc2 * pix_area_kpc2
    # Not related
    mask_area_pc2 = pix_area_deg2 * (np.pi**2) / (180**2) * (distance_pc)**2 * len(selected_col)
    #-----------------------------------------------------------
    # Save the answer
    if len(selected_col) == 0:
        print("No data available under this threshold.")
        return True, None 
    max_selected_col = np.max(selected_col)
    num_of_pixel = len(selected_col)
    mask_area_deg2 = pix_area_deg2 * len(selected_col)
    
    ans = cloud_mass_set()
    ans.distance_pc = distance_pc,
    ans.mask_area_deg2 = mask_area_deg2,
    ans.mask_area_pc2 = mask_area_pc2,
    ans.dust_mass_Msun = dust_mass_Msun,
    return False, ans

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
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage:  Av_region_mass.py [contour config] [column density map] [extinction map]") 
        aa.create()
        exit()
    contour_config_name = argv[1]
    col_den_name = argv[2]
    Av_name = argv[3]
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
    # Initialize parameters
    # Contours
    contour_config = aa.load(contour_config_name)
    levels = np.array(contour_config[0], dtype = float)[::-1]
    linewidths = np.array(contour_config[1], dtype = float)[::-1]
    colors = contour_config[2, ::-1]
    print("Av levels: \n{0}".format(levels))
    print("linewidth: \n{0}".format(linewidths))
    print("colors: \n{0}".format(colors))
    # Pixel Size
    pix_area_in_deg2_col = abs(h_col['CDELT1'] * h_col['CDELT2']) 
    pix_area_in_deg2_Av = abs(h_Av['CDELT1'] * h_Av['CDELT2'])
    # Result hosts
    # Av_range, mask_area_deg2, mask_area_pc2, dust_mass_Msun
    result_table = np.zeros((len(levels), 5), dtype = object)
    #--------------------------------------------
    # Given cloud distance
    distance = dist_lib.chamaeleon_13_distance
    # Estimate the cloud mass
    print("distance (pc): {0}".format(distance))
    prev_level = None
    prev_result_set = cloud_mass_set()
    the_first = True
    Av_range = None
    mask_area_deg2 = None
    mask_area_pc2 = None
    dust_mass_Msun = None
    for i, level in enumerate(levels):
        # Renew the results
        new_result_set = None 
        Av_mask = np.where(Av > level)
        Failure, new_result_set = calc_cloud_mass(col, Av_mask, pix_area_in_deg2_col, distance)
        if Failure:
            continue
        elif the_first:
            the_first = False
            print("-------------------------------")
            Av_range = "Av > {0}".format(level)
            mask_area_deg2 = new_result_set.mask_area_deg2[0]
            mask_area_pc2 = new_result_set.mask_area_pc2[0]
            dust_mass_Msun = new_result_set.dust_mass_Msun[0]
        else:
            print("-------------------------------")
            Av_range = "{0} < Av <= {1} ".format(level, prev_level) 
            mask_area_deg2 = new_result_set.mask_area_deg2[0] - prev_result_set.mask_area_deg2[0]
            mask_area_pc2 =  new_result_set.mask_area_pc2[0] - prev_result_set.mask_area_pc2[0]
            dust_mass_Msun = new_result_set.dust_mass_Msun[0] - prev_result_set.dust_mass_Msun[0]
        result_table[i, 0] = Av_range
        result_table[i, 1] = mask_area_deg2
        result_table[i, 2] = mask_area_pc2
        result_table[i, 3] = dust_mass_Msun
        result_table[i, 4] = distance
        print(Av_range)
        print("mask_area_deg2: {0}".format(mask_area_deg2))
        print("mask_area_pc2: {0}".format(mask_area_pc2))
        print("dust_mass_Msun: {0}".format(dust_mass_Msun))
            
        # Update the last result by this result
        prev_level = level
        prev_result_set = new_result_set 
            
    #--------------------------------------------
    # Save the result
    print(result_table)
    np.save("Av_region_mass", result_table) 
    #--------------------------------------------
    # Plot the contour
    levels = levels[::-1]
    linewidths = linewidths[::-1]
    colors = colors[::-1]
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
