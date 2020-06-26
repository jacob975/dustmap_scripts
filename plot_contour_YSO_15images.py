#!/usr/bin/python3
'''
Abstract:
    This is a program to plot the contours and YSOs on a dustmap 
Usage:
    Av_region_mass.py [contour config] [cloud_name] [column density map] [extinction map] [coord table] [cls pred table] [yso class table]
    column density map unit: M_sun / kpc^2
    extinction map unit: Av in mag
Output:
    2. The PNG image of selected regions with Av contour and YSO in different classes.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200622
####################################
update log
20200622 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from  matplotlib.colors import LogNorm
import numpy as np

from astropy.io import fits
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_area
from astropy.coordinates import SkyCoord
from astropy import units as u

from uncertainties import ufloat, unumpy

from input_lib import option_Av_region_paras
import dist_lib 

def is_insided_the_image(pixel_array, class_array, image_shape):
    # if no points, nothing to do
    if pixel_array.size == 0:
        return pixel_array, class_array
    # Take the points inside the image.
    pixel_insided_index = np.where(
        (pixel_array[:,0] >= 0) &
        (pixel_array[:,0] < image_shape[1]) &
        (pixel_array[:,1] >= 0) &
        (pixel_array[:,1] < image_shape[0])
    )
    pixel_insided_array = pixel_array[pixel_insided_index]
    class_insided_array = class_array[pixel_insided_index]
    return pixel_insided_array, class_insided_array

def plot_star_forming_region(fig, gs_iterator, arguments):
    # Load arguments
    contour_config_name = arguments[1]
    cloud_name = arguments[2]
    col_den_name = arguments[3]
    Av_name = arguments[4]
    coord_name = arguments[5]
    cls_pred_name = arguments[6]
    yso_class_name = arguments[7]
    print("Arguments:\n{0}".format(np.array(arguments)))
    #--------------------------------------------
    # Load images and data
    hdu_col = fits.open(col_den_name)
    col = hdu_col[1].data 
    e_col = hdu_col[2].data
    h_col = hdu_col[1].header 
    w_col = WCS(h_col)
    hdu_Av = fits.open(Av_name)
    Av = hdu_Av[1].data 
    Av_shape = Av.shape
    h_Av = hdu_Av[1].header 
    w_Av = WCS(h_Av)
     # Load YSO coordinates and classes
    no_yso = False
    no_cls_pred = False
    no_class = False
    coord_array = np.loadtxt(coord_name, dtype= float)
    try:
        cls_pred_array = np.loadtxt(cls_pred_name, dtype = int)
    except:
        no_cls_pred = True
    try:
        class_array = np.loadtxt(yso_class_name, dtype = object)
    except:
        no_class = True
    if no_cls_pred or no_class:
        no_yso = True
    # Initialize the contours
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
    if no_cls_pred or no_class:
        no_yso = True
    #--------------------------------------------
    # Plot the contour
    ax = plt.subplot(gs_iterator, projection = w_col)
    # Dust map
    aximage = plt.imshow(
        col, 
        cmap = 'gist_yarg',
        norm = LogNorm(
            vmax = np.max(col),
            vmin = np.min(col)
        ),
        zorder = 1,
    )
    #cbar = plt.colorbar(aximage)
    #cbar.set_label(r"$M_{sun}/kpc^{2}$", rotation = 270, labelpad = 15)
    # Define a routine for finding YSO on this map
    def plot_routine(ax, coord_array, cls_pred_array, class_array, class_flag, color_scheme):
        # Find the index
        yso_index = None
        if class_flag == 'all':
            yso_index = np.where(cls_pred_array == 2)[0]
        else:
            yso_index = np.where((cls_pred_array == 2) & (class_array == class_flag))
        # Confirm the coordinate    
        if h_Av['CTYPE1'][:4] == 'GLON':
            yso_coord_array = icrs2galactic(coord_array[yso_index]) 
        else:
            yso_coord_array = coord_array[yso_index]           
        # Convert the world coordinate the pixel coordinate    
        yso_pixel_array = np.array(np.round(
            w_Av.wcs_world2pix(yso_coord_array, 0)), 
            dtype = int
        )
        yso_class_array = class_array[yso_index]
        # Take the YSO on the image only.
        on_image_yso_pixel_array, on_image_yso_class_array = is_insided_the_image(
            yso_pixel_array, 
            yso_class_array,
            Av_shape,
        )
        if on_image_yso_pixel_array.size == 0:
            return
        # Plot the YSO on the dustmap
        ax.scatter(
            on_image_yso_pixel_array[:,0],
            on_image_yso_pixel_array[:,1],
            color = color_scheme,
            s = 3,
            marker = 'x',
            zorder = 100,
        )
        return 
    
    #plot_routine(ax, coord_array, cls_pred_array, class_array, 'all', 'r')
    if not no_yso:
        plot_routine(ax, coord_array, cls_pred_array, class_array, 'I', 'r')
        plot_routine(ax, coord_array, cls_pred_array, class_array, 'Flat', 'm')
        plot_routine(ax, coord_array, cls_pred_array, class_array, 'II','c')
        plot_routine(ax, coord_array, cls_pred_array, class_array, 'III', 'b')
    
    # Av contours
    plt.contour(
        Av, 
        levels = levels,
        linewidths = linewidths,
        colors = 'w',
        #colors = colors,   
        zorder = 2,
    )
    plt.text(
        x = 0.05,
        y = 0.9,
        s = cloud_name,
        transform=ax.transAxes,
    )
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    return 

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
    if len(argv) != 8:
        print ("The number of arguments is wrong.")
        print ("Usage: Av_region_mass.py [contour config] [cloud_name] [column density map] [extinction map] [coord table] [cls pred table] [yso class table]") 
        exit()
    contour_config_name_list_name = argv[1]
    cloud_name_list_name = argv[2]
    col_den_name_list_name = argv[3]
    Av_name_list_name = argv[4]
    coord_name_list_name = argv[5]
    cls_pred_name_list_name = argv[6]
    yso_class_name_list_name = argv[7]
    print("Arguments:\n{0}".format(np.array(argv)))
    # Load argv
    contour_config_name_list = np.loadtxt(contour_config_name_list_name, dtype = str)
    cloud_name_list = np.loadtxt(cloud_name_list_name, dtype = str, delimiter = '\n')
    col_den_name_list = np.loadtxt(col_den_name_list_name, dtype = str)
    Av_name_list = np.loadtxt(Av_name_list_name, dtype = str)
    coord_name_list = np.loadtxt(coord_name_list_name, dtype = str)
    cls_pred_name_list = np.loadtxt(cls_pred_name_list_name, dtype = str)
    yso_class_name_list = np.loadtxt(yso_class_name_list_name, dtype = str)
    #--------------------------------------------
    num_v = 5
    num_h = 3
    num_images_1page = num_v*num_h
    num_images = 62
    fig = plt.figure(0, figsize=(10,15))
    gs1 = gridspec.GridSpec(num_v, num_h)
    gs1.update(
        wspace = 0.05, # the amount of width reserved for space between subplots,
                      # expressed as a fraction of the average axis width
        hspace = 0.08, # the amount of height reserved for space between subplots,
        left = 0.05,  # the left side of the subplots of the figure
        right = 1.0,   # the right side of the subplots of the figure
        bottom = 0.05,  # the bottom of the subplots of the figure
        top = 0.95,
    )
    for i in range(num_images):
        # Change the figure every 15 panels
        if i%num_images_1page == 0 and i != 0:
            # Save the last figure 
            fig.savefig(
                "dustmap_Avcontour_YSO_15images_{0}.png".format(i//num_images_1page -1),
                dpi = 300,
            )
            plt.close()
            # Create a new figure
            fig = plt.figure(i//num_images_1page, figsize=(10,15))
            gs1 = gridspec.GridSpec(num_v, num_h)
            gs1.update(
                wspace = 0.05, # the amount of width reserved for space between subplots,
                              # expressed as a fraction of the average axis width
                hspace = 0.08, # the amount of height reserved for space between subplots,
                left = 0.05,  # the left side of the subplots of the figure
                right = 1.0,   # the right side of the subplots of the figure
                bottom = 0.05,  # the bottom of the subplots of the figure
                top = 0.95,
            )
        arguments = [
            argv[0],
            contour_config_name_list[i],
            cloud_name_list[i],
            col_den_name_list[i],
            Av_name_list[i],
            coord_name_list[i],
            cls_pred_name_list[i],
            yso_class_name_list[i]
        ]
        plot_star_forming_region(fig, gs1[i%15], arguments) 
    # Save the last figure 
    fig.savefig(
        "dustmap_Avcontour_YSO_15images_{0}.png".format(num_images//num_images_1page),
        dpi = 300,
    )
    plt.close()
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
