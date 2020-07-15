#!/usr/bin/python3
'''
Abstract:
    Show the Bayestar 19 dustmap on a given location, 10x10 deg square.
Usage:
    calc_yso_contamination.py [cls pred] [Model index]
    Available Model index: II, IV
Output:
    print the possible contamination percentage of YSOs.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200715
####################################
update log
20200715 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: calc_yso_contamination.py [cls pred] [Model index]") 
        print ("Available Model index: II, IV")
        exit()
    cls_pred_name = argv[1]
    model_index = argv[2]
    #--------------------------------------------
    # Load data
    cls_pred = np.loadtxt(cls_pred_name, dtype = int)
    # Initialization
    # This is error rate of stars
    error_rate = None
    if model_index == 'II':
        error_rate = 2.2e-4
    elif model_index == 'IV':
        error_rate = 2.87e-5
    else:
        print("The Error rate for this model is not measured.")
        print("Please try 'II' or 'IV'.")
        exit()
    print(error_rate)
    # Obtain class index and also the source counts for each class.
    star_index = np.where(cls_pred == 0)[0]
    gala_index = np.where(cls_pred == 1)[0]
    ysos_index = np.where(cls_pred == 2)[0]
    num_star = len(star_index)
    num_gala = len(gala_index)
    num_ysos = len(ysos_index)
    print(num_star)
    print(num_gala)
    print(num_ysos)
    # Calculate the percentage of possible YSO contamination
    # The error rate of galaxies is larger than stars by a factor of 35
    cyso = (num_star*error_rate + num_gala*35*error_rate)/num_ysos
    print('YSO contamination: {0}%'.format(cyso*100))
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
