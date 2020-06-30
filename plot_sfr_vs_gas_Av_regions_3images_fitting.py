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

# Condition can be: 'less_500pc', '500_1000pc', 'over_1000pc'
def plot_sfr_gas_relation(ax, condition, panel_order ):
    #--------------------------------------------
    # Initialization
    class_I_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_I_surface_density_Msun_per_Myr_pc2`',
        '`distance_pc`',
    ]
    class_F_list = [
        '`cloud_surface_density_Msun_per_pc2`', 
        '`e_cloud_surface_density_Msun_per_pc2`', 
        '`sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`e_sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`flag_sfr_F_surface_density_Msun_per_Myr_pc2`',
        '`distance_pc`',
    ]
    # Obtain data from SQL
    # Class I, Zucker+20 sources only
    class_I_data = load2py_mq_av_region(class_I_list)
    class_I_data = np.array(class_I_data, dtype=object)
    gas_sigma_class_I =       np.array(class_I_data[:,0], dtype = float)
    e_gas_sigma_class_I =     np.array(class_I_data[:,1], dtype = float)
    sfr_sigma_class_I =       np.array(class_I_data[:,2], dtype = float)
    e_sfr_sigma_class_I =     np.array(class_I_data[:,3], dtype = float)
    flag_sfr_sigma_class_I =  np.array(class_I_data[:,4], dtype = str)
    distance_class_I =        np.array(class_I_data[:,5], dtype = float)
    index_U_class_I = flag_sfr_sigma_class_I == 'U'
    # Take the region inside the defined distance range
    index_distance_condition_class_I = None
    if condition == 'less_500pc':
        index_distance_condition_class_I = distance_class_I <= 500
    elif condition == '500_1000pc':
        index_distance_condition_class_I = np.logical_and(
            distance_class_I > 500,
            distance_class_I <= 1000
        )
    elif condition == 'over_1000pc':
        index_distance_condition_class_I = distance_class_I > 1000
    # Class Flat, Zucker+20 sources only
    class_F_data = load2py_mq_av_region(class_F_list)
    class_F_data = np.array(class_F_data, dtype=object)
    gas_sigma_class_F =      np.array(class_F_data[:,0], dtype = float)
    e_gas_sigma_class_F =    np.array(class_F_data[:,1], dtype = float)
    sfr_sigma_class_F =      np.array(class_F_data[:,2], dtype = float)
    e_sfr_sigma_class_F =    np.array(class_F_data[:,3], dtype = float)
    flag_sfr_sigma_class_F = np.array(class_F_data[:,4], dtype = str)
    distance_class_F =        np.array(class_F_data[:,5], dtype = float)
    index_U_class_F = flag_sfr_sigma_class_F == 'U'
    # Take the region inside the defined distance range
    index_distance_condition_class_F = None
    if condition == 'less_500pc':
        index_distance_condition_class_F = distance_class_F <= 500
    elif condition == '500_1000pc':
        index_distance_condition_class_F = np.logical_and(
            distance_class_F > 500,
            distance_class_F <= 1000
        )
    elif condition == 'over_1000pc':
        index_distance_condition_class_F = distance_class_F > 1000
    #----------
    # Class_I 
    ax.errorbar(
        x = gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        xerr = e_gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        y = sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        yerr = e_sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)],
        label= 'Class I YSO',
        color = 'b',
        fmt = 'o',
        markersize = 2,
        linewidth = 1
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_class_I[(index_U_class_I) & (index_distance_condition_class_I)],
        y = sfr_sigma_class_I[(index_U_class_I) & (index_distance_condition_class_I)],
        label='Class I YSO upper limit', 
        marker = 'v',
        s = 3,
        color = 'b',
        alpha = 0.5,
    )
    #----------
    # Class_F
    ax.errorbar(
        x = gas_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)],
        xerr = e_gas_sigma_class_F[(~index_U_class_F) & index_distance_condition_class_F],
        y = sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)],
        yerr = e_sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)],
        label='Class Flat YSO',
        color = 'm',
        fmt = 'o',
        markersize = 2,
        linewidth = 1
    )
    # SFR Upper limits for Av regions without a YSO.
    ax.scatter(
        x = gas_sigma_class_F[(index_U_class_F) & (index_distance_condition_class_F)],
        y = sfr_sigma_class_F[(index_U_class_F) & (index_distance_condition_class_F)],
        label='Class Flat YSO upper limit', 
        marker = 'v',
        color = 'm',
        alpha = 0.5,
        s = 3,
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
    KS_gas_sigma = np.logspace(1, 4.5, 100)
    KS_sfr_sigma = Kennicut98_sfr_sigma(KS_gas_sigma)
    ax.plot(
        KS_gas_sigma, 
        KS_sfr_sigma, 
        color = 'k', 
        label = 'Kennicut+98 ( KS relation)'
    )
    #-----------------------------------
    # Plot the fitting line of SFR-gas relation, and show the corresponding legend
    def heiderman_broke_powerlaw(x, m1, b, m2, xth):
        r1 = np.log10(0.38)
        r2 = np.log10(2.63)
        ans = np.piecewise(
            x,
            [x < xth+r2, x>= xth+r2],
            [lambda x:m1*x + b +r1-m1*r2, lambda x:m1*xth+b + m2*(x-xth) +r1-m2*r2]
        )
        return ans
    #   m1, b, m2, xth
    heiderman_paras = [4.58, -9.18, 1.12, np.log10(129.2)]
    def linear(x, m, b):
        return m*x + b
    def reduce_chi_square(x, y, yerr, func, paras):
        chi_square = 0
        dof = len(x) - len(paras)
        for i, xi in enumerate(x):
            chi_square_i = np.power(y[i] - func(xi, *paras), 2)/np.power(yerr[i], 2)
            chi_square = chi_square + chi_square_i
        reduce_chi_square = chi_square / dof
        return reduce_chi_square

    inp_x = np.hstack((
        np.log10(gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)]), 
        np.log10(gas_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)])
    ))
    inp_xerr = np.hstack((
        np.log10((
            e_gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)] +\
            gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)]) /\
            gas_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)]),
        np.log10((
            e_gas_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)] +\
            gas_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)]) /\
            gas_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)]),
    )) 
    inp_y = np.hstack((
        np.log10(sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)]),
        np.log10(sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)]),
    ))
    inp_yerr = np.hstack((
        np.log10((
            e_sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)] +\
            sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)]) /\
            sfr_sigma_class_I[(~index_U_class_I) & (index_distance_condition_class_I)]),
        np.log10((
            e_sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)] +\
            sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)]) /\
            sfr_sigma_class_F[(~index_U_class_F) & (index_distance_condition_class_F)]),
    
    ))
    #target_func = func_powerlaw
    target_func = linear
    popt, pcov = curve_fit(
        target_func, 
        inp_x, inp_y, 
        sigma = 1/(inp_xerr**2),
        #absolute_sigma=True,
        maxfev = 2000, 
        #p0=np.array([1.4, 1e-5]), # for powerlaw
        p0=np.array([1.4, -4]), # for linear 
    )
    m = popt[0]
    dm = np.sqrt(pcov[0,0])
    b = popt[1]
    db = np.sqrt(pcov[1,1])
    out_x = np.linspace(1, 5, 100)
    ax.plot(np.power(10, out_x), np.power(10, target_func(out_x, *popt)), 'r--')
    #ax.plot(np.power(10, out_x), np.power(10, heiderman_broke_powerlaw(out_x, *heiderman_paras)), 'c--')
    #-----------------------------------
    # Adjust and Save the figure
    ax.set_xscale('log')
    ax.set_yscale('log')
    x_upper = 1e1
    x_lower = 1e5
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
        get_AvRC(get_AvDL(x_upper)),
        get_AvRC(get_AvDL(x_lower)),
    )
    ax.set_xlim(x_upper, x_lower)
    ax.set_ylim(1e-3, 1e3)
    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    ax.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        direction='in'
    )
    ax2.tick_params(
        axis='x',
        which='both',
        direction='in'
    )
    ax.grid(True)
    rchisq_linear = reduce_chi_square(
        inp_x, 
        inp_y, inp_yerr, 
        linear, 
        popt)
    print(rchisq_linear)
    rchisq_heiderman = reduce_chi_square(
        inp_x, 
        inp_y, inp_yerr,
        heiderman_broke_powerlaw, 
        heiderman_paras
    )
    print(rchisq_heiderman)

    if panel_order == 0:
        ax.set_ylabel(r'SFR surface density ($M_{sun} / Myr \cdot pc^{2}$)')
        present_condition = "d <= 500pc"
    if panel_order == 1:
        ax.set_xlabel(r'gas surface density ($M_{sun} / pc^{2}$)')
        ax2.set_xlabel('A$_{v,RQ}$')
        present_condition = "500pc < d <= 1000pc"
    if panel_order == 2:
        present_condition = "d > 1000pc"
    # Show the text
    ax.text(
        x = 0.05, 
        y = 0.95, 
        s = "%s\nM = %.2f$\pm$%.2f\nb = %.2f$\pm$%.2f\n$\chi_{r}$=%.3g" % (
            present_condition, 
            m, dm,
            b, db,
            rchisq_linear,
        ),
        transform = ax.transAxes,
        horizontalalignment='left',
        verticalalignment='top',
        bbox=dict(facecolor='white', edgecolor='black', pad=5.0)
    )    
        #ax.legend()

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
    # Plot the figure
    fig, axes = plt.subplots(
        1, 3, 
        sharex=True, 
        sharey=True,
        figsize=(12, 4))
    plot_sfr_gas_relation(axes[0], 'less_500pc', 0)
    plot_sfr_gas_relation(axes[1], '500_1000pc', 1)
    plot_sfr_gas_relation(axes[2], 'over_1000pc', 2)
    plt.tight_layout()
    #plt.show()
    fig.savefig("chiu20_sfr_vs_gas_Av_regions_3images_fitting.png", dpi = 150)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
