#!/usr/bin/python3
'''
Abstract:
    Plot the SFR-gas relation in different Av contour regions (Without error consideration).
Usage:
    plot_sfr_vs_gas.py.
Output:
    1. The figure of SFR surface density and gas surface density.
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200522
####################################
update log
20200522 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from chiu20_mysql_lib import load2py_mq_av_region, load2py_mq_cloud
from Heiderman10_lib import Heiderman_cloud, Heiderman_Av_regions_class_f, Heiderman_Av_regions_class_i

def reduce_chi_square(x, y, yerr, func, paras):
    chi_square = 0
    dof = len(x) - len(paras)
    for i, xi in enumerate(x):
        chi_square_i = np.power(y[i] - func(xi, *paras), 2)/np.power(yerr[i], 2)
        chi_square = chi_square + chi_square_i
    reduce_chi_square = chi_square / dof
    return reduce_chi_square

#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 1:
        print ("The number of arguments is wrong.")
        print ("Usage: plot_sfr_vs_gas.py")
        exit()
    #--------------------------------------------
    # Initialization
    class_I_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_I_surface_density_Msun_per_Myr_pc2`',
    ]
    class_F_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_F_surface_density_Msun_per_Myr_pc2`',
    ]
    # Obtain data from SQL
    # Class I
    class_I_data = load2py_mq_av_region(class_I_list)
    class_I_data = np.array(class_I_data, dtype=object)
    gas_sigma_class_I =       np.array(class_I_data[:,0], dtype = float)
    e_gas_sigma_class_I =     np.array(class_I_data[:,1], dtype = float)
    sfr_sigma_class_I =       np.array(class_I_data[:,2], dtype = float)
    e_sfr_sigma_class_I =     np.array(class_I_data[:,3], dtype = float)
    flag_sfr_sigma_class_I =  np.array(class_I_data[:,4], dtype = str)
    index_U_class_I = flag_sfr_sigma_class_I == 'U'
    # Class Flat
    class_F_data = load2py_mq_av_region(class_F_list)
    class_F_data = np.array(class_F_data, dtype=object)
    gas_sigma_class_F =      np.array(class_F_data[:,0], dtype = float)
    e_gas_sigma_class_F =    np.array(class_F_data[:,1], dtype = float)
    sfr_sigma_class_F =      np.array(class_F_data[:,2], dtype = float)
    e_sfr_sigma_class_F =    np.array(class_F_data[:,3], dtype = float)
    flag_sfr_sigma_class_F = np.array(class_F_data[:,4], dtype = str)
    index_U_class_F = flag_sfr_sigma_class_F == 'U'
    #--------------------------------------------
    # Plot the figure
    fig, ax = plt.subplots(figsize = (6,6))
    #----------
    # Class_I 
    detected_gas_sigma_I = gas_sigma_class_I[~index_U_class_I]
    e_detected_gas_sigma_I = e_gas_sigma_class_I[~index_U_class_I]
    detected_sfr_sigma_I = sfr_sigma_class_I[~index_U_class_I]
    e_detected_sfr_sigma_I = e_sfr_sigma_class_I[~index_U_class_I]
    ax.errorbar(
        x = detected_gas_sigma_I,
        xerr = e_detected_gas_sigma_I,
        y = detected_sfr_sigma_I,
        yerr = e_detected_sfr_sigma_I,
        label= 'Class I YSO',
        color = 'b',
        fmt = 'o',
        markersize = 3,
        linewidth = 1,
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_class_I[index_U_class_I],
        y = sfr_sigma_class_I[index_U_class_I],
        label='Class I YSO upper limit', 
        marker = 'v',
        color = 'b',
        alpha = 0.5,
        s = 5,
    )
    #----------
    # Class_F
    detected_gas_sigma_F = gas_sigma_class_F[~index_U_class_F]
    e_detected_gas_sigma_F = e_gas_sigma_class_F[~index_U_class_F]
    detected_sfr_sigma_F = sfr_sigma_class_F[~index_U_class_F]
    e_detected_sfr_sigma_F = e_sfr_sigma_class_F[~index_U_class_F]
    ax.errorbar(
        x = detected_gas_sigma_F,
        xerr = e_detected_gas_sigma_F,
        y = detected_sfr_sigma_F,
        yerr = e_detected_sfr_sigma_F,
        label='Class Flat YSO',
        color = 'm',
        fmt = 'o',
        markersize = 3,
        linewidth = 1,
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_class_F[index_U_class_F],
        y = sfr_sigma_class_F[index_U_class_F],
        label='Class Flat YSO upper limit', 
        marker = 'v',
        color = 'm',
        alpha = 0.5,
        s = 5,
    )
        
    #--------------------------------------------
    # Additional data
    #-------------
    # Heiderman+10
    Heiderman_gas_sigma_class_i = np.array(Heiderman_Av_regions_class_i[:,1], dtype = float)
    Heiderman_sfr_sigma_class_i = np.array(Heiderman_Av_regions_class_i[:,2], dtype = float)
    Heiderman_gas_sigma_class_f = np.array(Heiderman_Av_regions_class_f[:,1], dtype = float)
    Heiderman_sfr_sigma_class_f = np.array(Heiderman_Av_regions_class_f[:,2], dtype = float)
    #ax.scatter(
    #    Heiderman_gas_sigma_class_i, 
    #    Heiderman_sfr_sigma_class_i, 
    #    label = 'Heiderman+10 (c2d class I)', 
    #    color = 'g',
    #)
    #ax.scatter(
    #    Heiderman_gas_sigma_class_f, 
    #    Heiderman_sfr_sigma_class_f, 
    #    label = 'Heiderman+10 (c2d class F)', 
    #    color = 'c',
    #)
    #-------------
    # Kennicutt+98
    # K-S relation
    def Kennicut98_sfr_sigma(gas_sigma):
        # gas_sigma in Msun / pc^2
        # sfr_sigma in Msun / Myr pc^2
        sfr_sigma = 2.5e-4 * np.power(gas_sigma, 1.4)
        return sfr_sigma
    KS_gas_sigma = np.logspace(1, 5, 100)
    KS_sfr_sigma = Kennicut98_sfr_sigma(KS_gas_sigma)
    ax.plot(
        KS_gas_sigma, 
        KS_sfr_sigma, 
        color = 'k', 
        label = 'Kennicut+98 ( KS relation)'
    )
    #-----------------------------------
    # Adjust and Save the figure
    ax.set_xscale('log')
    ax.set_yscale('log')
    # Set the second x tick for Av,RC
    x_lower = 1e1
    x_upper = 2e4
    # A_v,DL = 0.74*(dust_sigma/ (10^5 * M_sun / kpc^-2))
    def get_AvDL(cloud_sigma):
        nominator = 0.74 * cloud_sigma # M_sun pc-2
        denominator = 10 # M_sun pc-2
        return nominator/denominator
    # A_v,RC = (0.38*U_min + 0.27) * A_v,DL
    # by Assuming U_min = 0.5
    def get_AvRC(AvDL):
        return (0.38*0.5 + 0.27) * AvDL
    ax2 = ax.twiny()
    ax2.set_xscale('log')
    ax2.set_xlim(
        get_AvRC(get_AvDL(x_lower)),
        get_AvRC(get_AvDL(x_upper)),
    )
    ax2.set_xlabel(r'A$_{V,RQ}$')
    #--------------------------------------------------
    # Fit data using a power law
    inp_x = np.hstack((
        np.log10(detected_gas_sigma_I), 
        np.log10(detected_gas_sigma_F),
    ))
    inp_xerr = np.hstack((
        np.log10((e_detected_gas_sigma_I+detected_gas_sigma_I)/detected_gas_sigma_I),
        np.log10((e_detected_gas_sigma_F+detected_gas_sigma_F)/detected_gas_sigma_F),
    ))
    inp_y = np.hstack((
        np.log10(detected_sfr_sigma_I), 
        np.log10(detected_sfr_sigma_F),
    ))
    inp_yerr = np.hstack((
        np.log10((e_detected_sfr_sigma_I+detected_sfr_sigma_I)/detected_sfr_sigma_I),
        np.log10((e_detected_sfr_sigma_F+detected_sfr_sigma_F)/detected_sfr_sigma_F),
    ))
    def linear(x, m, b):
        return m*x + b
    # Initialize
    target_func = linear
    p0 = np.array([1.6, -6.0])
    popt, pcov = curve_fit(
        target_func,
        inp_x, inp_y,
        sigma = inp_yerr,
        absolute_sigma=True,
        maxfev = 2000,
        p0=p0,
    )
    print(popt)
    print(pcov)
    out_x = np.linspace(1, 5, 100)
    ax.plot(np.power(10, out_x), np.power(10, target_func(out_x, *popt)), 'r--')
    m = popt[0]
    dm = np.sqrt(pcov[0,0])
    b = popt[1]
    db = np.sqrt(pcov[1,1])
    rchisq = reduce_chi_square(inp_x, inp_y, inp_yerr, linear, popt)
    print(rchisq)
    ax.text(
        x = 0.05,
        y = 0.95,
        s = "$N$ = %.2f$\pm$%.2f \nb = %.2f$\pm$%.2f\n$\chi^{2}_{r}$=%.2f" % (
            m, dm,
            b, db,
            rchisq,
        ),
        transform = ax.transAxes,
        horizontalalignment='left',
        verticalalignment='top',
        bbox=dict(facecolor='white', edgecolor='black', pad=5.0)
    )

    # Fine tune the panel
    ax.set_xlim(x_lower, x_upper)
    ax.set_ylim(1e-3, 1e3)
    ax.grid(True)
    ax.set_xlabel(r'gas surface density ($M_{sun} / pc^{2}$)')
    ax.set_ylabel(r'SFR surface density ($M_{sun} / Myr pc^{2}$)')
    ax.tick_params(
        axis = 'x',
        which='both',
        direction='in',
    )
    ax.tick_params(
        axis = 'y',
        which='both',
        direction='in',
    )
    ax2.tick_params(
        axis='x',
        which='both',
        direction='in',
    )
    #ax.legend()
    fig.savefig(
        "chiu20_sfr_vs_gas_Av_regions_fitting.png",
        dpi = 200)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
