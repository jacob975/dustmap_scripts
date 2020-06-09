#!/usr/bin/python3
'''
Abstract:
    This is a program to calculate the cloud mass based on column density map and extintion map.
Usage:
    Av_region_YSO.py [contour config] [YSO coord] [extinction map] 
    extinction map unit: Av in mag
Output:
    1. Show the YSO number in different Av region.
    2. The Av contour map.
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

class cloud_yso_set():
    def __init__(self):
        self.mask_area_deg2 = 0.0 
        self.yso_number = 0

def calc_yso_number(yso_pixel_array, Av_threshold, Av_map, pix_area_deg2):
    selected_Av = Av_map[Av_map > Av_threshold]
    ans = cloud_yso_set()
    #print(Av_map[yso_pixel_array[:,1], yso_pixel_array[:,0]])
    index_selected_yso = np.where(Av_map[yso_pixel_array[:,1], yso_pixel_array[:,0]] > Av_threshold)[0]
    num_yso = len(index_selected_yso)
    ans.mask_area_deg2 = pix_area_deg2*len(selected_Av) 
    ans.yso_number = num_yso
    #print(ans.mask_area_deg2, ans.yso_number)
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
    if len(argv) != 5:
        print ("The number of arguments is wrong.")
        print ("Usage: Av_region_YSO.py [contour config] [coord] [cls_pred] [extinction map]") 
        aa.create()
        exit()
    contour_config_name = argv[1]
    coord_name = argv[2]
    cls_pred_name = argv[3]
    Av_name = argv[4]
    print("Arguments:\n{0}".format(argv))
    #--------------------------------------------
    # Load data and image
    coord_array = np.loadtxt(coord_name, dtype = float)
    cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    yso_index = np.where(cls_pred == 2)[0]
    yso_coord = coord_array[yso_index]
    hdu_Av = fits.open(Av_name)
    Av = hdu_Av[1].data 
    h_Av = hdu_Av[1].header 
    w_Av = WCS(h_Av)
    #--------------------------------------------
    # Initialize the image parameters
    pix_area_in_deg2_Av = abs(h_Av['CDELT1'] * h_Av['CDELT2'])
    # Contours
    contour_config = aa.load(contour_config_name)
    levels = np.array(contour_config[0], dtype = float)[::-1]
    linewidths = np.array(contour_config[1], dtype = float)[::-1]
    colors = contour_config[2, ::-1]
    print("Av levels: \n{0}".format(levels))
    print("linewidth: \n{0}".format(linewidths))
    print("colors: \n{0}".format(colors))
    # Result hosts
    # Av_range, yso_num_range
    result_table = np.zeros((len(levels), 2), dtype = object)
    #--------------------------------------------
    # Calculate the number of YSO in certain Av range 
    prev_level = None
    prev_result_set = cloud_yso_set()
    the_first = True
    for i, level in enumerate(levels):
        print("-------------------------------")
        # Initialize the results
        new_result_set = None 
        Av_range = None
        mask_area_deg2 = None
        yso_num_range = None
        # Renew the results
        yso_pixel = np.array(np.round(w_Av.wcs_world2pix(yso_coord, 0)), dtype = int)
        Failure, new_result_set = calc_yso_number(yso_pixel, level, Av, pix_area_in_deg2_Av)
        if Failure:
            continue
        elif the_first:
            the_first = False
            Av_range = "Av > {0}".format(level)
            mask_area_deg2 = new_result_set.mask_area_deg2
            yso_num_range = new_result_set.yso_number
        else:
            Av_range = "{0} < Av <= {1}".format(level, prev_level) 
            mask_area_deg2 = new_result_set.mask_area_deg2 - prev_result_set.mask_area_deg2
            yso_num_range = new_result_set.yso_number - prev_result_set.yso_number
        result_table[i, 0] = Av_range
        result_table[i, 1] = yso_num_range 
        print(Av_range)
        print("mask_area_deg2: {0}".format(mask_area_deg2))
        print("YSO number: {0}".format(yso_num_range))
            
        # Update the last result by this result
        prev_level = level
        prev_result_set = new_result_set 
    #--------------------------------------------
    # Save the result
    print(result_table)
    np.save("Av_region_YSO", result_table) 
    #--------------------------------------------
    # Plot the contour
    levels = levels[::-1]
    linewidths = linewidths[::-1]
    colors = colors[::-1]
    plt.figure(figsize=(10,8))
    axes = plt.subplot(111, projection = w_Av)
    ax = plt.imshow(
        Av, 
        norm = LogNorm(
            vmax = np.max(Av),
            vmin = np.min(Av)
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
    plt.savefig("{0}_Av_contour.png".format(Av_name[:-5]))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
