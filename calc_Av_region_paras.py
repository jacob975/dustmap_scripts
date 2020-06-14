#!/usr/bin/python3
'''
Abstract:
    Calculate the Star Formation parameters from given data for certain extinction regions.
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
from uncertainties import ufloat, umath
from input_lib import option_calc_SF_paras
from chiu20_mysql_lib import save2sql_mq_av_region, mq_av_region_format, mq_av_region_name
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
    l_deg = data_list[1] # deg
    b_deg = data_list[2] # deg
    num_yso = int(data_list[3]) # number
    num_i = int(data_list[4]) # number
    num_f = int(data_list[5]) # number
    #avg_yso_lt = float(data_list[6])   # Myr
    u_avg_yso_lt = ufloat(
        float(data_list[6]), 
        float(data_list[7])
    ) # Myr
    #avg_class_i_yso_lt = float(data_list[8])   # Myr
    u_avg_class_i_yso_lt = ufloat(
        float(data_list[8]),
        float(data_list[9])
    )   # Myr
    #avg_class_f_yso_lt = float(data_list[10])   # Myr
    u_avg_class_f_yso_lt = ufloat(
        float(data_list[10]),
        float(data_list[11])
    )   # Myr
    #avg_yso_mass = float(data_list[12])  # Msun
    u_avg_yso_mass = ufloat(
        float(data_list[12]),
        float(data_list[13])
    )   # Msun
    #cloud_mass = float(data_list[14])    # Msun
    u_cloud_mass = ufloat(
        float(data_list[14]),
        float(data_list[15])
    )   # Msun
    cloud_area_deg2 = float(data_list[16])   # deg^2
    #avg_cloud_distance = float(data_list[17])    # kpc
    u_avg_cloud_distance = ufloat(
        float(data_list[17]),
        float(data_list[18])
    )   # kpc
    Av_threshold = data_list[19] # mag
    comments = data_list[20]
    flag_sfr = 'A'
    flag_i_sfr = 'A'
    flag_f_sfr = 'A'
    #--------------------------------------------
    # Exceptions
    # All YSO number
    if num_yso <= 0:
        assumed_num_yso = 1
        flag_sfr = 'U'
    else:
        assumed_num_yso = num_yso
    # Class I YSO number
    if num_i <= 0:
        assumed_num_i = 1
        flag_i_sfr = 'U'
    else:
        assumed_num_i = num_i
    # Class F YSO number
    if num_f <= 0:
        assumed_num_f = 1
        flag_f_sfr = 'U'
    else:
        assumed_num_f = num_f
    #--------------------------------------------
    # Calculate the Star Formation parameters.
    # Side results, required to obtain main results.
    cloud_area_sr = cloud_area_deg2 * (np.pi**2) / (180**2) # sr
    u_cloud_area_pc2 = cloud_area_sr * u_avg_cloud_distance**2 # pc^2
    u_total_yso_mass = assumed_num_yso * u_avg_yso_mass # Msun
    u_total_class_i_yso_mass = assumed_num_i * u_avg_yso_mass # Msun
    u_total_class_f_yso_mass = assumed_num_f * u_avg_yso_mass # Msun
    # Main results
    u_cloud_surface_density = u_cloud_mass/u_cloud_area_pc2 # Msun / pc^2
    num_yso_per_area_deg2 = assumed_num_yso / cloud_area_deg2   # number / deg^2
    u_num_yso_per_area_pc2  = assumed_num_yso / u_cloud_area_pc2     # number / pc^2
    num_i_per_area_deg2 = assumed_num_i / cloud_area_deg2     # number / deg^2
    u_num_i_per_area_pc2  = assumed_num_i / u_cloud_area_pc2       # number / pc^2
    num_f_per_area_deg2 = assumed_num_f / cloud_area_deg2    # number / deg^2
    u_num_f_per_area_pc2  = assumed_num_f / u_cloud_area_pc2       # number / pc^2
    # "sfr" stands for star formation rate
    u_sfr = u_total_yso_mass / u_avg_yso_lt  # Msun / Myr
    u_sfr_i = u_total_class_i_yso_mass / u_avg_class_i_yso_lt  # Msun / Myr
    u_sfr_f = u_total_class_f_yso_mass / u_avg_class_f_yso_lt  # Msun / Myr
    u_sfr_per_area_pc2 = u_sfr / u_cloud_area_pc2 # Msun / (Myr * pc^2)
    u_sfr_i_per_area_pc2 = u_sfr_i / u_cloud_area_pc2 # Msun / (Myr * pc^2)
    u_sfr_f_per_area_pc2 = u_sfr_f / u_cloud_area_pc2 # Msun / (Myr * pc^2)
    # "sfe stands for star formation efficiency"
    u_sfe = u_total_yso_mass / (u_cloud_mass + u_total_yso_mass) # ratio
    # dep stand for depletion time
    u_cloud_t_dep = u_cloud_mass / u_sfr # (Myr)
    # Free-fall time defined in Evans+09
    # t_ff = 34Myr / √ n
    #   where n is density of all particle species
    #   by assuming the cloud being "spherical" and their area is "circle".
    u_total_particles = (u_cloud_mass*solar_mass_in_g) / (mu_H2 * m_H)
    u_cloud_radius_in_spherical_cm = umath.sqrt(u_cloud_area_pc2/np.pi) * pc_in_cm # cm
    u_cloud_volume_in_spherical_cm3 = u_cloud_radius_in_spherical_cm**3 * 4 * np.pi / 3    # cm^3
    u_particle_density = u_total_particles/u_cloud_volume_in_spherical_cm3 # cm^-3
    u_cloud_t_ff = 34 / umath.sqrt(u_particle_density) # Myr
    u_sfr_per_t_ff = u_cloud_t_ff / u_cloud_t_dep # ratio
    #-----------------------------------
    # Print the results
    print("#------ Main results --------")
    print("Cloud: {0}".format(data_name))
    print("All YSO number: {0}".format(num_yso))
    print("Class I YSO number: {0}".format(num_i))
    print("Class Flat YSO number: {0}".format(num_f))
    print("All YSO mass: {0}".format(u_total_yso_mass))
    print("Class I YSO mass: {0}".format(u_total_class_i_yso_mass))
    print("Class Flat YSO mass: {0}".format(u_total_class_f_yso_mass))
    # Location and morphology of clouds
    print("Galactic longtitude, l (deg): {0}".format(l_deg))
    print("Galactic latitude, b (deg): {0}".format(b_deg))
    print("Distance (pc): {0}".format(u_avg_cloud_distance))
    print("Area (deg^2): {0}".format(cloud_area_deg2))
    print("Area (pc^2): {0}".format(u_cloud_area_pc2))
    print("All YSO number per area (deg^2): {0}".format(num_yso_per_area_deg2))
    print("All YSO number per area (pc^2): {0}".format(u_num_yso_per_area_pc2))
    print("Class I YSO number per area (deg^2): {0}".format(num_i_per_area_deg2))
    print("Class I YSO number per area (pc^2): {0}".format(u_num_i_per_area_pc2))
    print("Class Flat YSO number per area (deg^2): {0}".format(num_f_per_area_deg2))
    print("Class Flat YSO number per area (pc^2): {0}".format(u_num_f_per_area_pc2))
    print("Av threshold (mag): {0}".format(Av_threshold))
    print("Cloud Mass (Msun): {0}".format(u_cloud_mass))
    print("cloud_surface_density (Msun/pc^2): {0}".format(u_cloud_surface_density))
    # All YSO
    print("Star formation rate (Msun/Myr): {0}".format(u_sfr))
    print("Star formation rate per area (Msun/Myr/pc^2): {0}".format(u_sfr_per_area_pc2))
    print("Star formation rate flag: {0}".format(flag_sfr))
    # Class I YSO
    print("Star formation rate (Msun/Myr): {0}".format(u_sfr_i))
    print("Star formation rate per area (Msun/Myr/pc^2): {0}".format(u_sfr_i_per_area_pc2))
    print("Star formation rate flag: {0}".format(flag_i_sfr))
    # Class Flat YSO
    print("Star formation rate (Msun/Myr): {0}".format(u_sfr_f))
    print("Star formation rate per area (Msun/Myr/pc^2): {0}".format(u_sfr_f_per_area_pc2))
    print("Star formation rate flag: {0}".format(flag_f_sfr))
    
    print("cloud depletion time (Myr): {0}".format(u_cloud_t_dep))
    print("cloud free-fall time (Myr): {0}".format(u_cloud_t_ff))
    print("Star formation rate in a unit of free-fall time (ratio): {0}".format(u_sfr_per_t_ff))
    print("Star formation efficiency (ratio): {0}".format(u_sfe))
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
    data = list(-999*np.ones(len(mq_av_region_format)))
    mq_av_region_format_keys = list(mq_av_region_format[:,0])
    data[mq_av_region_format_keys.index('`cloud`')] = region_name
    # Location and morphology of clouds
    data[mq_av_region_format_keys.index('`l_deg`')] = l_deg
    data[mq_av_region_format_keys.index('`b_deg`')] = b_deg
    # Number of YSO
    data[mq_av_region_format_keys.index('`yso_number`')] = num_yso
    data[mq_av_region_format_keys.index('`class_i_yso_number`')] = num_i
    data[mq_av_region_format_keys.index('`class_f_yso_number`')] = num_f
    # YSO lifetime
    data[mq_av_region_format_keys.index('`yso_lifetime_Myr`')] = u_avg_yso_lt.n
    data[mq_av_region_format_keys.index('`e_yso_lifetime_Myr`')] = u_avg_yso_lt.s
    data[mq_av_region_format_keys.index('`class_i_yso_lifetime_Myr`')] = u_avg_class_i_yso_lt.n
    data[mq_av_region_format_keys.index('`e_class_i_yso_lifetime_Myr`')] = u_avg_class_i_yso_lt.s
    data[mq_av_region_format_keys.index('`class_f_yso_lifetime_Myr`')] = u_avg_class_f_yso_lt.n
    data[mq_av_region_format_keys.index('`e_class_f_yso_lifetime_Myr`')] = u_avg_class_f_yso_lt.s
    # YSO mass
    data[mq_av_region_format_keys.index('`avg_yso_mass_Msun`')] = u_avg_yso_mass.n
    data[mq_av_region_format_keys.index('`e_avg_yso_mass_Msun`')] = u_avg_yso_mass.s
    data[mq_av_region_format_keys.index('`total_yso_mass_Msun`')] = u_total_yso_mass.n
    data[mq_av_region_format_keys.index('`e_total_yso_mass_Msun`')] = u_total_yso_mass.s
    data[mq_av_region_format_keys.index('`total_class_i_yso_mass_Msun`')] = u_total_class_i_yso_mass.n
    data[mq_av_region_format_keys.index('`e_total_class_i_yso_mass_Msun`')] = u_total_class_i_yso_mass.s
    data[mq_av_region_format_keys.index('`total_class_f_yso_mass_Msun`')] = u_total_class_f_yso_mass.n
    data[mq_av_region_format_keys.index('`e_total_class_f_yso_mass_Msun`')] = u_total_class_f_yso_mass.s
    # Distance to the cloud
    data[mq_av_region_format_keys.index('`distance_pc`')] = u_avg_cloud_distance.n
    data[mq_av_region_format_keys.index('`e_distance_pc`')] = u_avg_cloud_distance.s
    # Surface area of the cloud
    data[mq_av_region_format_keys.index('`area_deg2`')] = cloud_area_deg2
    data[mq_av_region_format_keys.index('`area_pc2`')] = u_cloud_area_pc2.n
    data[mq_av_region_format_keys.index('`e_area_pc2`')] = u_cloud_area_pc2.s
    data[mq_av_region_format_keys.index('`yso_number_per_deg2`')] = num_yso_per_area_deg2
    data[mq_av_region_format_keys.index('`yso_number_per_pc2`')] = u_num_yso_per_area_pc2.n
    data[mq_av_region_format_keys.index('`e_yso_number_per_pc2`')] = u_num_yso_per_area_pc2.n
    data[mq_av_region_format_keys.index('`class_i_yso_number_per_deg2`')] = num_yso_per_area_deg2
    data[mq_av_region_format_keys.index('`class_i_yso_number_per_pc2`')] = u_num_yso_per_area_pc2.n
    data[mq_av_region_format_keys.index('`e_class_i_yso_number_per_pc2`')] = u_num_yso_per_area_pc2.n
    data[mq_av_region_format_keys.index('`class_f_yso_number_per_deg2`')] = num_yso_per_area_deg2
    data[mq_av_region_format_keys.index('`class_f_yso_number_per_pc2`')] = u_num_yso_per_area_pc2.n
    data[mq_av_region_format_keys.index('`e_class_f_yso_number_per_pc2`')] = u_num_yso_per_area_pc2.n
    data[mq_av_region_format_keys.index('`Av_threshold`')] = Av_threshold 
    # Cloud mass derived from extinctions or dust emission
    data[mq_av_region_format_keys.index('`cloud_mass_Msun`')] = u_cloud_mass.n
    data[mq_av_region_format_keys.index('`e_cloud_mass_Msun`')] = u_cloud_mass.s
    data[mq_av_region_format_keys.index('`cloud_surface_density_Msun_per_pc2`')] = \
        u_cloud_surface_density.n 
    data[mq_av_region_format_keys.index('`e_cloud_surface_density_Msun_per_pc2`')] = \
        u_cloud_surface_density.s 
    # Star Formation Rate (SFR)
    data[mq_av_region_format_keys.index('`sfr_Msun_per_Myr`')] = u_sfr.n
    data[mq_av_region_format_keys.index('`e_sfr_Msun_per_Myr`')] = u_sfr.s
    data[mq_av_region_format_keys.index('`sfr_I_Msun_per_Myr`')] = u_sfr_i.n
    data[mq_av_region_format_keys.index('`e_sfr_I_Msun_per_Myr`')] = u_sfr_i.s
    data[mq_av_region_format_keys.index('`sfr_F_Msun_per_Myr`')] = u_sfr_f.n
    data[mq_av_region_format_keys.index('`e_sfr_F_Msun_per_Myr`')] = u_sfr_f.s
    # Star Formation Rate Density
    data[mq_av_region_format_keys.index('`sfr_surface_density_Msun_per_Myr_pc2`')] = u_sfr_per_area_pc2.n
    data[mq_av_region_format_keys.index('`e_sfr_surface_density_Msun_per_Myr_pc2`')] = u_sfr_per_area_pc2.s
    data[mq_av_region_format_keys.index('`flag_sfr_surface_density_Msun_per_Myr_pc2`')] = flag_sfr  
    data[mq_av_region_format_keys.index('`sfr_I_surface_density_Msun_per_Myr_pc2`')] = \
        u_sfr_i_per_area_pc2.n
    data[mq_av_region_format_keys.index('`e_sfr_I_surface_density_Msun_per_Myr_pc2`')] = \
        u_sfr_i_per_area_pc2.s
    data[mq_av_region_format_keys.index('`flag_sfr_I_surface_density_Msun_per_Myr_pc2`')] = flag_i_sfr 
    data[mq_av_region_format_keys.index('`sfr_F_surface_density_Msun_per_Myr_pc2`')] = \
        u_sfr_f_per_area_pc2.n
    data[mq_av_region_format_keys.index('`e_sfr_F_surface_density_Msun_per_Myr_pc2`')] = \
        u_sfr_f_per_area_pc2.s
    data[mq_av_region_format_keys.index('`flag_sfr_F_surface_density_Msun_per_Myr_pc2`')] = flag_f_sfr 
    # Depletion time
    data[mq_av_region_format_keys.index('`cloud_depletion_time_Myr`')] = u_cloud_t_dep.n
    data[mq_av_region_format_keys.index('`e_cloud_depletion_time_Myr`')] = u_cloud_t_dep.s
    data[mq_av_region_format_keys.index('`cloud_free_fall_time_Myr`')] = u_cloud_t_ff.n
    data[mq_av_region_format_keys.index('`e_cloud_free_fall_time_Myr`')] = u_cloud_t_ff.s
    data[mq_av_region_format_keys.index('`sfr_per_t_ff`')] = u_sfr_per_t_ff.n
    data[mq_av_region_format_keys.index('`e_sfr_per_t_ff`')] = u_sfr_per_t_ff.s
    # Star Formation Efficiency (SFE)
    data[mq_av_region_format_keys.index('`sfe`')] = u_sfe.n
    data[mq_av_region_format_keys.index('`e_sfe`')] = u_sfe.s
    # Inut files and Assumptions
    data[mq_av_region_format_keys.index('`input_file`')] = data_name 
    data[mq_av_region_format_keys.index('`reference`')] = 'Chiu, Yi-Lung' 
    data[mq_av_region_format_keys.index('`comments`')] = comments
    save2sql_mq_av_region(data)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
