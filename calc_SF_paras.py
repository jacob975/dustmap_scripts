#!/usr/bin/python3
'''
Abstract:
    Calculate the Star Formation parameters from given data.
Usage:
    calc_SF_paras.py [Given data]
Output:
    print the parameters on screen
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200506
####################################
update log
20200506 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
import numpy as np
from sys import argv
from os import system
from input_lib import option_calc_SF_paras
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #--------------------------------------------
    # Initialization
    # Argument Assistant
    default_input_name = 'input_for_calc_SF_paras.txt'
    aa = option_calc_SF_paras(default_input_name)
    # Constants
    mu_H2 = 2.8
    m_H = 1.674e-24
    pc_in_cm  = 3.086e18
    solar_mass_in_g = 1.989e33
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: calc_SF_paras.py [Given data]") 
        aa.create()
        exit()
    data_name = argv[1]
    # Load detail options from option file.
    data_list = aa.load(data_name)
    region_name = data_list[0]
    num_yso = int(data_list[1]) # number
    avg_yso_age = float(data_list[2])   # Myr
    avg_yso_mass = float(data_list[3])  # M_sun
    cloud_mass = float(data_list[4])    # M_sun
    cloud_area_deg2 = float(data_list[5])   # deg^2
    avg_cloud_distance = float(data_list[6])    # kpc
    avg_cloud_age = float(data_list[7]) # Myr
    Av_threshold = float(data_list[8]) # mag
    #--------------------------------------------
    # Calculate the Star Formation parameters.
    # Side results, required to obtain main results.
    cloud_area_sr = cloud_area_deg2 * (np.pi**2) / (180**2) # sr
    cloud_area_pc2 = cloud_area_sr * avg_cloud_distance**2 # pc^2
    total_yso_mass = num_yso * avg_yso_mass # M_sun
    # Main results
    num_yso_per_area_deg2 = num_yso / cloud_area_deg2 # number / deg^2
    num_yso_per_area_pc2 = num_yso / cloud_area_pc2    # number / pc^2
    # "sfr" stands for star formation rate
    sfr = total_yso_mass / avg_yso_age  # M_sun / Myr
    sfr_per_area_pc2 = sfr / cloud_area_pc2 # M_sun / (Myr * pc^2)
    # "sfe stands for star formation efficiency"
    sfe = np.divide(total_yso_mass, cloud_mass + total_yso_mass) # ratio
    # dep stand for depletion time
    cloud_t_dep = cloud_mass / sfr # (Myr)
    # Free-fall time defined in Evans+09
    # t_ff = 34Myr / √ n
    #   where n is density of all particle species
    #   by assuming the cloud being "spherical" and their area is "circle".
    total_particles = np.divide(
        cloud_mass*solar_mass_in_g,
        mu_H2 * m_H
    )
    cloud_radius_in_spherical_cm = np.sqrt(cloud_area_pc2/np.pi) * pc_in_cm # cm
    cloud_volume_in_spherical_cm3 = cloud_radius_in_spherical_cm**3 * 4 * np.pi / 3    # cm^3
    particle_density = np.divide(
        total_particles,
        cloud_volume_in_spherical_cm3
    ) # cm^-3
    cloud_t_ff = 34 / np.sqrt(particle_density) # Myr
    sfr_per_t_ff = cloud_t_ff / cloud_t_dep # ratio
    #-----------------------------------
    # TODO result
    # dense_and_star_mass_ratio
    # dense_depletion_time
    #-----------------------------------
    # Print the results
    print("#------ Main results --------")
    print("YSO number per area (deg^2): {0}".format(num_yso_per_area_deg2))
    print("YSO number per area (pc^2): {0}".format(num_yso_per_area_pc2))
    print("Star formation rate (M_sun/Myr): {0}".format(sfr))
    print("Star formation rate per area (M_sun/Myr/pc^2): {0}".format(sfr_per_area_pc2))
    print("Star formation efficiency (ratio): {0}".format(sfe))
    print("cloud depletion time (Myr): {0}".format(cloud_t_dep))
    print("cloud free-fall time (Myr): {0}".format(cloud_t_ff))
    print("Star formation rate in a unit of free-fall time (ratio): {0}".format(sfr_per_t_ff))
    print("#------ end of results ------")
    #-----------------------------------
    # Rename the option file
    data_new_name = 'input_for_calc_SF_paras_{0}.txt'.format(
        region_name
    )
    cmd_line = 'cp {0} {1}'.format(
        data_name,
        data_new_name
    )
    system(cmd_line)
    print("The input data has been renamed from '{0}' to '{1}'".format(
        data_name,
        data_new_name))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
