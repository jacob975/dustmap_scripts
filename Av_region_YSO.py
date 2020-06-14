#!/usr/bin/python3
'''
Abstract:
    This is a program to calculate the cloud mass based on column density map and extintion map.
Usage:
    Av_region_YSO.py [contour config] [YSO coord] [YSO cls_pred] [YSO class] [extinction map] 
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
        self.class_i_yso_number = 0
        self.class_f_yso_number = 0

def calc_yso_number(
        yso_pixel_array, 
        class_i_pixel_array, 
        class_f_pixel_array, 
        Av_threshold, 
        Av_map, 
        pix_area_deg2
    ):
    selected_Av = Av_map[Av_map > Av_threshold]
    ans = cloud_yso_set()
    try:
        index_selected_yso = np.where(Av_map[yso_pixel_array[:,1], yso_pixel_array[:,0]] > Av_threshold)[0]   
    except:
        index_selected_yso = []
    try:
        index_selected_class_i = np.where(Av_map[class_i_pixel_array[:,1], class_i_pixel_array[:,0]] > Av_threshold)[0]
    except:
        index_selected_class_i = []
    try:
        index_selected_class_f = np.where(Av_map[class_f_pixel_array[:,1], class_f_pixel_array[:,0]] > Av_threshold)[0]
    except:
        index_selected_class_f = []
    num_yso = len(index_selected_yso)
    num_i = len(index_selected_class_i)
    num_f = len(index_selected_class_f)
    ans.mask_area_deg2 = pix_area_deg2*len(selected_Av) 
    ans.yso_number = num_yso
    ans.class_i_yso_number = num_i
    ans.class_f_yso_number = num_f
    #print(ans.mask_area_deg2, ans.yso_number)
    return False, ans

def icrs2galactic(icrs_coords):
    ans = []
    for coord in icrs_coords:
        temp = SkyCoord(coord[0], coord[1], frame = 'icrs', unit = 'deg')
        ans.append([temp.galactic.l.deg, temp.galactic.b.deg])
    ans_array = np.array(ans)
    return ans_array
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
    if len(argv) != 6:
        print ("The number of arguments is wrong.")
        print ("Usage: Av_region_YSO.py [contour config] [coord] [cls_pred] [yso_class] [extinction map]") 
        aa.create()
        exit()
    contour_config_name = argv[1]
    coord_name = argv[2]
    cls_pred_name = argv[3]
    yso_class_name = argv[4]
    Av_name = argv[5]
    print("Arguments:\n{0}".format(argv))
    #--------------------------------------------
    # Load data and image
    coord_array = np.loadtxt(coord_name, dtype = float)
    cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    yso_class = np.loadtxt(yso_class_name, dtype = object)
    hdu_Av = fits.open(Av_name)
    Av = hdu_Av[1].data 
    h_Av = hdu_Av[1].header 
    w_Av = WCS(h_Av)
    # Obtain the index of YSO
    yso_index = np.where(cls_pred == 2)[0]
    class_i_yso_index = np.where((cls_pred == 2) & (yso_class == 'I'))
    class_f_yso_index = np.where((cls_pred == 2) & (yso_class == 'Flat'))
    if h_Av['CTYPE1'][:4] == 'GLON':
        yso_coord = icrs2galactic(coord_array[yso_index])
        class_i_yso_coord = icrs2galactic(coord_array[class_i_yso_index])
        class_f_yso_coord = icrs2galactic(coord_array[class_f_yso_index])
    else:
        yso_coord = coord_array[yso_index]
        class_i_yso_coord = coord_array[class_i_yso_index]
        class_f_yso_coord = coord_array[class_f_yso_index]
        
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
    # Av_range, YSO_num, Class_I_YSO_num, Class_F_YSO_num
    result_table = np.zeros((len(levels), 4), dtype = object)
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
        num_yso = None
        num_i = None
        num_f = None
        # Renew the results
        yso_pixel = np.array(np.round(w_Av.wcs_world2pix(yso_coord, 0)), dtype = int)
        class_i_yso_pixel = np.array(np.round(w_Av.wcs_world2pix(class_i_yso_coord, 0)), dtype = int)
        class_f_yso_pixel = np.array(np.round(w_Av.wcs_world2pix(class_f_yso_coord, 0)), dtype = int)
        Failure, new_result_set = calc_yso_number(
            yso_pixel, 
            class_i_yso_pixel, 
            class_f_yso_pixel, 
            level, 
            Av, 
            pix_area_in_deg2_Av
        )
        if Failure:
            continue
        elif the_first:
            the_first = False
            Av_range = "Av > {0}".format(level)
            mask_area_deg2 = new_result_set.mask_area_deg2
            num_yso = new_result_set.yso_number
            num_i = new_result_set.class_i_yso_number
            num_f = new_result_set.class_f_yso_number
        else:
            Av_range = "{0} < Av <= {1}".format(level, prev_level) 
            mask_area_deg2 = new_result_set.mask_area_deg2 - prev_result_set.mask_area_deg2
            num_yso = new_result_set.yso_number - prev_result_set.yso_number
            num_i = new_result_set.class_i_yso_number - prev_result_set.class_i_yso_number
            num_f = new_result_set.class_f_yso_number - prev_result_set.class_f_yso_number
        result_table[i, 0] = Av_range
        result_table[i, 1] = num_yso 
        result_table[i, 2] = num_i
        result_table[i, 3] = num_f
        print(Av_range)
        print("mask_area_deg2: {0}".format(mask_area_deg2))
        print("YSO number: {0}".format(num_yso))
        print("Class I YSO number: {0}".format(num_i))
        print("Class F YSO number: {0}".format(num_f))
            
        # Update the last result by this result
        prev_level = level
        prev_result_set = new_result_set 
    #--------------------------------------------
    # Print the summary
    print("-----------------------------------")
    print("Summary")
    print("YSO number: {0}".format(np.sum(result_table[:,1])))
    print("Class I YSO number: {0}".format(np.sum(result_table[:,2])))
    print("Class F YSO number: {0}".format(np.sum(result_table[:,3])))
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
