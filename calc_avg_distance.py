#!/usr/bin/python3
'''
Abstract:
    A function calculating the average distance of a set of regions.
Usage:
    calc_avg_distance.py [distance table]
Output:
    The average distance and their uncertainties.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200616
####################################
update log
20200616 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import numpy as np

from uncertainties import unumpy
from input_lib import option_avg_distance
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Initialize the arguements
    default_avg_distance_table_name = "distance_table.txt"
    # aa stands or Arguement Assistent
    aa = option_avg_distance(default_avg_distance_table_name)
    #-----------------------------------
    # Load argv
    if len(argv) != 2:
        print ("The number of arguments is wrong.")
        print ("Usage: calc_avg_distance.py [distance table]") 
        aa.create()
        exit()
    distance_table_name = argv[1]
    #--------------------------------------------
    # Load data
    distance_table = aa.load(distance_table_name)
    num_regions = len(distance_table)
    print(distance_table)
    # Calculate the average distance
    max_e_distance = np.max(distance_table[:,1])
    max_diff_distance = np.max(distance_table[:,0]) - np.min(distance_table[:,0])
    print(max_e_distance)
    print(max_diff_distance)
    distance_tot = np.mean(distance_table[:,0])
    e_distance_tot = np.sqrt(max_e_distance**2 + max_diff_distance**2)
    print(r'%f$\pm$%f (pc)' % (distance_tot, e_distance_tot))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
