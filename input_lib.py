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
        # Create the option file if it doesn't exist.
        try:
            np.loadtxt(self.default_name, dtype = str)
        except:
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
            return
        else:
            return

class option_hp_cloud_pointer(inp_option):
    def create(self):
        # Create cloud coordinate table.
        try:
            np.loadtxt(self.default_name, dtype = str)
        except:
            s = [
                '# Cloud coordinates, in icrs or galactic.',
                '# Please list the cloud center below.',
                '# Usage: [alpha] [beta] [frame]',
                '# ex. 98.9 4.0 galactic',
                '# It indicating a cloud located at (98.9, 4.0) using galactic coordinate',
                '45.1 8.9 galactic',
                '44.1 8.6 galactic',
                '42.8 7.9 galactic',
            ]
            np.savetxt(self.default_name, s, fmt = '%s')
            return
        else:
            return
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        self.opts = np.reshape(self.opts, (-1, 3))
        return self.opts

class option_calc_SF_paras(inp_option):
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str, delimiter = '\n')
        self.opts = list(self.opts)
        return self.opts
    def show_string(self):
        self.s = [
            "# Region name, take Perseus as example",
            "Perseus",
            "# Central Galactic Longtitude, l (deg.)",
            "160",
            "# Central Galactic Latitude, b (deg.)",
            "-20",
            "#----------------------------------------",
            "# YSO part",
            "#----------------------------------------",
            "# Number of YSOs",
            "118",
            "# Number of Class I YSOs",
            "113",
            "# Number of Class Flat YSOs",
            "4",
            "# Average YSO lifetime (Myr)",
            "2",
            "1",
            "# Average Class I YSO lifetime (Myr), and the corresponding error",
            "0.55",
            "0.28",
            "# Average Class Flat YSO lifetime (Myr), and the corresponding error",
            "0.36",
            "0.18",
            "# Average YSO mass (Msun), and the corresponding error",
            "0.5",
            "0.1",
            "#----------------------------------------",
            "# Cloud part",
            "#----------------------------------------",
            "# Cloud mass (gas+dust in Msun), and the corresponding error",
            "18000",
            "7000",
            "# Cloud size (solid angle in deg^2), and the corresponding error",
            "3.97",
            "# Distance to the cloud (pc), and the corresponding error",
            "250",
            "50",
            "# Av threshold used to defined the cloud region (mag)",
            "Av >= 4",
            "#----------------------------------------",
            "# Comments",
            "#----------------------------------------",
            "# Write note below but ONE line only.",
            "NULL",
        ]
    def create(self):
        # Create the option file if it doesn't exist.
        try:
            np.loadtxt(self.default_name, dtype = str)
        except:
            self.show_string()
            np.savetxt(self.default_name, self.s, fmt = '%s')
            return
        else:
            return

class option_Av_region_paras(inp_option):
    def create(self):
        # Create the option file if it doesn't exist.
        try:
            np.loadtxt(self.default_name, dtype = str)
        except:
            s = [
                "# The Av list used to define contours from little to large."
                "# ex. : 2 4 6 12 22",
                "2   4   6   9  12  22",
                "# The contour linewidth",
                "2 1.5 1.5 1.5 1.5 1.5",
                "# The contour colors",
                "k   r   k   k   b   k",
            ]
            np.savetxt(self.default_name, s, fmt = '%s')
            return
        else:
            return
    def load(self, file_name):
        self.opts = np.loadtxt(file_name, dtype = str)
        return self.opts
