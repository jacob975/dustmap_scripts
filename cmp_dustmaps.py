#!/usr/bin/python3
'''
Abstract:
    We’ll finish by plotting a comparison of the SFD, Planck Collaboration and Bayestar Dust maps.
Usage:
    cmp_dustmaps.py [l] [b]
Output:
    The picture that compare different dustmap on a given location.
Editor:
    Jacob975
    People who contribute this website: https://dustmaps.readthedocs.io/en/latest/examples.html#getting-started

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20200325
####################################
update log
20200325 version alpha 1:
    1. The code works.
'''
# First, we’ll import the necessary modules:
import time
from sys import argv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import astropy.units as units
from astropy.coordinates import SkyCoord

from dustmaps.sfd import SFDQuery
from dustmaps.planck import PlanckQuery
from dustmaps.bayestar import BayestarQuery
#--------------------------------------------
# Main code
if __name__ == "__main__":
    # Measure time
    start_time = time.time()
    #-----------------------------------
    # Load argv
    if len(argv) != 3:
        print ("The number of arguments is wrong.")
        print ("Usage: cmp_dustmaps.py [l] [b]")
        exit()
    l0 = float(argv[1])
    b0 = float(argv[2])
    #--------------------------------------------
    # Next, we’ll set up a grid of coordinates to plot, centered on the given location: 
    
    # e.g. Aquila South cloud
    # l0, b0 = (37., -16.)
    l = np.arange(l0 - 5., l0 + 5., 0.05)
    b = np.arange(b0 - 5., b0 + 5., 0.05)
    l, b = np.meshgrid(l, b)
    coords = SkyCoord(
        l*units.deg, 
        b*units.deg,
        distance=1.*units.kpc, 
        frame='galactic'
    )
    
    #--------------------------------------------
    # Then, we’ll load up and query three different dust maps:
    
    sfd = SFDQuery()
    Av_sfd = 2.742 * sfd(coords)
    
    planck = PlanckQuery()
    Av_planck = 3.1 * planck(coords)
    
    bayestar = BayestarQuery(max_samples=1)
    Av_bayestar = 2.742 * bayestar(coords)
    
    #--------------------------------------------
    # We’ve assumed RV=3.1, and used the coefficient from Table 6 of Schlafly & Finkbeiner (2011) 
    # to convert SFD and Bayestar reddenings to magnitudes of AV.
    #
    # Finally, we create the figure using matplotlib:
    
    fig = plt.figure(figsize=(12,4), dpi=150)
    
    for k,(Av,title) in enumerate([(Av_sfd, 'SFD'),
                                   (Av_planck, 'Planck'),
                                   (Av_bayestar, 'Bayestar')]):
        ax = fig.add_subplot(1,3,k+1)
        ax.imshow(
            np.sqrt(Av)[::,::-1],
            vmin=0.,
            vmax=2.,
            origin='lower',
            interpolation='nearest',
            cmap='binary',
            aspect='equal'
        )
        ax.axis('off')
        ax.set_title(title)
    
    fig.subplots_adjust(wspace=0., hspace=0.)
    plt.savefig('comparison.png', dpi=150)
    #-----------------------------------
    # Measure time
    elapsed_time = time.time() - start_time
    print("Exiting Main Program, spending ", elapsed_time, "seconds.")
