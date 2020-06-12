#!/usr/bin/python3
'''
Abstract:
    A function calculating infrared flux slope, alpha, and giving YSO class to sources.
    The class we use:
    Quoted from Evans+09, these classifications were based on the slope between 2 and 10 um.
    In our case, we obtain alpha using flux from IRAC 1-4 and MIPS 1
        I: 0.3 <= alpha
        Flat: -0.3 <= alpha < 0.3
        II: -1.6 <= alpha < -0.3
        III: alpha < -1.6
Usage:
    calc_alpha.py [SED table] [Q table]
Output:
    1. A table of alpha.
    2. A table of YSO classes.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200612
####################################
update log
20200612 version alpha 1:

'''
# First, we’ll import the necessary modules:
import time
from sys import argv
import numpy as np
import convert_lib
from matplotlib import pyplot as plt

# Skip band-filled value to prevent artifacts.
def sed_to_alpha(sed, Q):
    # Initialize
    alpha = 0.0
    spitzer_system = convert_lib.set_spitzer()
    band_name_list = [
        'IR1',
        'IR2',
        'IR3',
        'IR4',
        'MP1',
    ]
    log_l_F = []
    e_log_l_F = []
    log_l = []
    yso_class = ''
    # Make lambda and flux*lambda list
    for i, band_name in enumerate(band_name_list):    
        # Choose the band that detected.
        if Q[i] != 'A':
            continue
        # Index start at 3 because we skip band J, H, and K.
        band_flux = sed[3+i]
        e_band_flux = sed[8+3+i]
        log_l_F.append(np.log10(spitzer_system[band_name][1] * band_flux))
        e_log_l_F.append(np.log10(spitzer_system[band_name][1] * (e_band_flux+band_flux)/band_flux))
        log_l.append(np.log10(spitzer_system[band_name][1])) 
    w_log_l_F = np.divide(1, np.array(e_log_l_F))
    paras = np.polyfit(log_l, log_l_F, 1, w = w_log_l_F)
    # Calculate alpha and derive yso class
    alpha = paras[0]
    if alpha >= 0.3:
        yso_class = 'I'
    elif alpha >= -0.3 and alpha < 0.3:
        yso_class = 'Flat'
    elif alpha >= -1.6 and alpha < -0.3:
        yso_class = 'II'
    elif alpha < -1.6:
        yso_class = 'III'
    #--------------------------------------------
    # For debugging
    # Plot the result for debugging
    '''
    p = np.poly1d(paras)
    x_samples = np.logspace(
        np.log10(spitzer_system['IR1'][1]), 
        np.log10(spitzer_system['MP1'][1]), 
        10
    )
    plt.plot(np.log10(x_samples), p(np.log10(x_samples)))
    plt.scatter(
        log_l, 
        log_l_F, 
        c = 'r', 
        label = r'$\alpha$=%f, Class %s' % (alpha, yso_class))
    plt.xlabel(r"log($\lambda$)")
    plt.ylabel(r"log($\lambda F_{\lambda}$)")
    plt.legend()
    plt.show()
    '''
    return alpha, yso_class

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: calc_alpha.py [SED table] [Q table]") 
        exit()
    sed_table_name = argv[1]
    Q_table_name = argv[2]
    #--------------------------------------------
    # Load SED and Q from input arguments 
    sed_table = np.loadtxt(sed_table_name)
    Q_table = np.loadtxt(Q_table_name, dtype = str)
    # Calculate the alpha
    alpha_list = np.zeros(len(Q_table))
    yso_class_list = np.zeros(len(Q_table), dtype=np.dtype('U8'))
    for i, Q in enumerate(Q_table):
        alpha_list[i], yso_class_list[i] = sed_to_alpha(sed_table[i], Q)
    # Print out the number of sources in different YSO class.
    print("Class I, Flat, II, III")
    num_I = len(np.where(yso_class_list == 'I')[0])
    num_F = len(np.where(yso_class_list == 'Flat')[0])
    num_II = len(np.where(yso_class_list == 'II')[0])
    num_III = len(np.where(yso_class_list == 'III')[0])
    print("{0}, {1}, {2}, {3}".format(num_I, num_F, num_II, num_III))
    # Save the alpha and YSO class
    np.savetxt("alpha_table.txt", alpha_list)
    np.savetxt("yso_class_table.txt", yso_class_list, fmt = '%s')
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
