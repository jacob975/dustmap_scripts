#!/usr/bin/python3
'''
Abstract:
    This is a program for reading and loading input files. 
Usage:
    print_input_lib.py
Editor:
    Jacob975

##################################
#   Python3                      #
#   This code is made in python3 #
##################################

20181113
####################################
update log
20181113 version alpha 1
    1. The code works.
'''
import numpy as np
import time

class inp_option():
    def __init__(self, default_name):
        self.opts = None
        self.default_name = default_name
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        self.opts = list(self.opts)
        return self.opts

class option_hp_map_project(inp_option):
    def create(self):
        s = [   
            '# Coordinate system (icrs or galactic)',
            'icrs',
            '# Right Ascension (deg. in float)',
            '# Example: 277',
            '277',
            '# Declination (deg. in float)',
            '# Example: 0.5',
            '0.5',
            '# ds9 width (pixel in integer)',
            '768',
            '# ds9 height (pixel in integer)', 
            '768',
        ]
        np.savetxt(self.default_name, s, fmt = '%s')

class option_calc_SF_paras(inp_option):
    def create(self):
        s = [
            "# Region name, take Perseus as example",
            "Perseus",
            "#----------------------------------------",
            "# YSO part",
            "#----------------------------------------",
            "# Number of YSOs",
            "118",
            "# Average YSO age (Myr)",
            "2",
            "# Average YSO mass (Msun)",
            "0.5",
            "#----------------------------------------",
            "# Cloud part",
            "#----------------------------------------",
            "# Cloud mass (gas+dust in Msun)",
            "17793",
            "# Cloud size (solid angle in deg^2)",
            "3.97",
            "# Distance to the cloud (pc)",
            "250",
            "# Average cloud age (Myr) (not used)",
            "2",
            "# Av threshold used to defined the cloud region (mag)",
            "4",
        ]
        np.savetxt(self.default_name, s, fmt = '%s')
