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
from chiu20_mysql_lib import save2sql_mq_cloud, mq_cloud_format, mq_cloud_name
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
    avg_yso_mass = float(data_list[3])  # Msun
    cloud_mass = float(data_list[4])    # Msun
    cloud_area_deg2 = float(data_list[5])   # deg^2
    avg_cloud_distance = float(data_list[6])    # kpc
    avg_cloud_age = float(data_list[7]) # Myr
    Av_threshold = float(data_list[8]) # mag
    comments = data_list[9]
    #--------------------------------------------
    # Calculate the Star Formation parameters.
    # Side results, required to obtain main results.
    cloud_area_sr = cloud_area_deg2 * (np.pi**2) / (180**2) # sr
    cloud_area_pc2 = cloud_area_sr * avg_cloud_distance**2 # pc^2
    total_yso_mass = num_yso * avg_yso_mass # Msun
    # Main results
    cloud_surface_density = cloud_mass/cloud_area_pc2 # Msun / pc^2
    num_yso_per_area_deg2 = num_yso / cloud_area_deg2 # number / deg^2
    num_yso_per_area_pc2 = num_yso / cloud_area_pc2    # number / pc^2
    # "sfr" stands for star formation rate
    sfr = total_yso_mass / avg_yso_age  # Msun / Myr
    sfr_per_area_pc2 = sfr / cloud_area_pc2 # Msun / (Myr * pc^2)
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
    # Print the results
    print("#------ Main results --------")
    print("Cloud: {0}".format(data_name))
    print("YSO number: {0}".format(num_yso))
    print("Distance (pc): {0}".format(avg_cloud_distance))
    print("Area (deg^2): {0}".format(cloud_area_deg2))
    print("Area (pc^2): {0}".format(cloud_area_pc2))
    print("YSO number per area (deg^2): {0}".format(num_yso_per_area_deg2))
    print("YSO number per area (pc^2): {0}".format(num_yso_per_area_pc2))
    print("Av threshold (mag): {0}".format(Av_threshold))
    print("Cloud Mass (Msun): {0}".format(cloud_mass))
    print("cloud_surface_density (Msun/pc^2): {0}".format(cloud_surface_density))
    print("Star formation rate (Msun/Myr): {0}".format(sfr))
    print("Star formation rate per area (Msun/Myr/pc^2): {0}".format(sfr_per_area_pc2))
    print("cloud depletion time (Myr): {0}".format(cloud_t_dep))
    print("cloud free-fall time (Myr): {0}".format(cloud_t_ff))
    print("Star formation rate in a unit of free-fall time (ratio): {0}".format(sfr_per_t_ff))
    print("Star formation efficiency (ratio): {0}".format(sfe))
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
    # Save to sql
    # Initialize two lists for outputs and keys.
    data = list(-999*np.ones(len(mq_cloud_format)))
    mq_cloud_format_keys = list(mq_cloud_format[:,0])
    data[mq_cloud_format_keys.index('`cloud`')] = region_name
    data[mq_cloud_format_keys.index('`yso_number`')] = num_yso
    data[mq_cloud_format_keys.index('`distance_pc`')] = avg_cloud_distance
    data[mq_cloud_format_keys.index('`area_deg2`')] = cloud_area_deg2
    data[mq_cloud_format_keys.index('`area_pc2`')] = cloud_area_pc2
    data[mq_cloud_format_keys.index('`yso_number_per_deg2`')] = num_yso_per_area_deg2
    data[mq_cloud_format_keys.index('`yso_number_per_pc2`')] = num_yso_per_area_pc2
    data[mq_cloud_format_keys.index('`Av_threshold`')] = Av_threshold 
    data[mq_cloud_format_keys.index('`cloud_mass_Msun`')] = cloud_mass
    data[mq_cloud_format_keys.index('`cloud_surface_density_Msun_per_pc2`')] = cloud_surface_density 
    data[mq_cloud_format_keys.index('`sfr_Msun_per_Myr`')] = sfr 
    data[mq_cloud_format_keys.index('`sfr_surface_density_Msun_per_Myr_pc2`')] = sfr_per_area_pc2
    data[mq_cloud_format_keys.index('`cloud_depletion_time_Myr`')] = cloud_t_dep 
    data[mq_cloud_format_keys.index('`cloud_free_fall_time_Myr`')] = cloud_t_ff
    data[mq_cloud_format_keys.index('`sfr_per_t_ff`')] = sfr_per_t_ff
    data[mq_cloud_format_keys.index('`sfe`')] = sfe 
    data[mq_cloud_format_keys.index('`input_file`')] = data_name 
    data[mq_cloud_format_keys.index('`reference`')] = 'Chiu, Yi-Lung' 
    data[mq_cloud_format_keys.index('`comments`')] = comments
    save2sql_mq_cloud(data)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
