#!/usr/bin/python3
'''
Abstract:
    Estimate the protostar luminosity based on SED in mid-infrared using method defined in Kryukova et al. (2012).
Usage:
    sed_to_L.py [SED list] [Q flag list] [cloud distance]
Output:
    A list of given protostar luminosity. 
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200416 
####################################
update log
20200416 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv
import numpy as np
from matplotlib import pyplot as plt

import convert_lib

# Input: SED of a protostar, Quality flag of a protostar
# SED in mJy
# d in pc
# Output: Luminosity in mid-infrared
# L_mir in L_solar
def sed_to_L_mir(sed, Q, d):
    # Initialize
    L_mir = 0
    coeffients = np.array([
        19.79,
        16.96,
        10.49,
        5.50,
        4.68,
        4.01,
        4.31,
        0.81
    ])
    # Skip all band-filled values, convert from mJy to Jy, and times the coeffient.
    modified_sed = np.zeros(len(Q))
    modified_sed[np.where(Q != 'U')] = \
        coeffients[np.where(Q != 'U')] * sed[np.where(Q != 'U')]/1000
    L_mir = np.sum(modified_sed)*1e-6*d**2
    return L_mir

# Input: SED of a protostar, Quality flag of a protostar
# Output: The slope of best-fitted line on SED
#------------------------------------------------
# TODO
# Skip band-filled value to prevent artifacts.

def sed_to_alpha(sed, Q):
    # Initialize
    cs = 3e10 # cm s-1
    alpha = 0.0
    spitzer_system = convert_lib.set_SCAO()
    band_name_list = [
        'J',
        'H',
        'K',
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
        if Q[i] != 'A' and Q[i] != 'S':
            continue
        # Index start at 3 because we skip band J, H, and K.
        band_flux = sed[i]
        e_band_flux = sed[8+i]
        wavelength = 10*spitzer_system[band_name][1] # um
        # Specific freq. to specific flux
        cvt = cs / (wavelength**2) # cm-1 s-1
        log_l_F.append(np.log(wavelength * cvt * band_flux))
        e_log_l_F.append(np.log(wavelength * (e_band_flux+band_flux)/band_flux))
        log_l.append(np.log(wavelength)) 
    print(log_l_F)
    print(log_l)
    print(e_log_l_F)
    w_log_l_F = np.divide(1, np.array(e_log_l_F))
    paras = np.polyfit(
        x = log_l_F, 
        y = log_l, 
        deg = 1, 
        w = w_log_l_F
    )
    alpha = paras[0]
    # Plot the result for debugging
    '''
    p = np.poly1d(paras)
    x_samples = np.logspace(
        np.log10(spitzer_system['IR1'][1]), 
        np.log10(spitzer_system['MP1'][1]), 
        10
    )
    plt.plot(np.log10(x_samples), p(np.log10(x_samples)))
    plt.scatter(log_l, log_l_F, c = 'r')
    plt.xlabel(r"log($\lambda$)")
    plt.ylabel(r"log($\lambda F_{\lambda}$)")
    plt.show()
    '''
    return alpha

# Input: The slope of best-fitted SED line (alpha), mid-infrared luminosity.
# Output: Protostar luminosity (0.36um - 1000 um) defined in Evans et al. (2009)
def alpha_L_mir_to_L_bol(alpha, L_mir):
    # Initialzation
    L_bol = 0
    # For flat spectrum
    if alpha <= np.power(10, -0.5):
        L_bol = L_mir / 0.338
    # For rising spectrum
    else:
        denominator = np.power(-0.466*np.log10(alpha) + 0.337, 2)
        L_bol = L_mir/denominator
    return L_bol

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #----------------------------------------
    # Load argv
    if len(argv) != 4:
        print ("The number of arguments is wrong.")
        print ("Usage: sed_to_L.py [SED list] [Q flag list] [cloud distance]") 
        exit()
    sed_name = argv[1]
    Q_name = argv[2]
    distance = float(argv[3])
    #-----------------------------------------
    # Load data
    sed_array = np.loadtxt(sed_name, dtype = float)
    Q_array = np.loadtxt(Q_name, dtype = str)
    # Initialize variables
    num_sed = len(sed_array)
    # alpha_L_array
    # 1 for alpha
    # 2 for L_mir
    # 3 for L_bol
    alpha_L_array = np.zeros((num_sed, 3))
    for i in range(num_sed):
        #--------------------------------------------
        # Calculate \alpha
        alpha = sed_to_alpha(sed_array[i], Q_array[i])
        #--------------------------------------------
        # Calculate L_{MIR}
        L_mir = sed_to_L_mir(sed_array[i], Q_array[i], distance)
        #--------------------------------------------
        # Calculate L_{bol}
        L_bol = alpha_L_mir_to_L_bol(alpha, L_mir)
        '''
        print("---")
        print(r"$\alpha$ = %f" % alpha)
        print(r"$L_{MIR}$ = %f (solar luminosity)" % L_mir)
        print(r"$L_{bol}$ = %f (solar luminosity)" % L_bol)
        '''
        alpha_L_array[i, 0] = alpha
        alpha_L_array[i, 1] = L_mir
        alpha_L_array[i, 2] = L_bol
    #-----------------------------------
    # Save the result
    np.savetxt(
        "paras_of_luminosity_func.txt",
        alpha_L_array,
        header = 'alpha, Lmir, L_bol',
        fmt = '%s',
    )
    '''
    #-----------------------------------
    # Debug: Plot the histogram
    fig, axes = plt.subplots(figsize = (8,8))
    plt.hist(
        alpha_L_array[:, 2],
        bins = np.logspace(-4, 4, num = 20),
    )
    axes.set_xscale("log")
    axes.set_xlabel(r"$L_{bol}$")
    plt.savefig("L_bol_hist.png")
    '''
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
