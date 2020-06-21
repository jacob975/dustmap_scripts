#!/usr/bin/python3
from uncertainties import ufloat

# 20200619
# I calculate the distance from 
# 1. For c2d and Gould belt regions, I use the distance mentioned in Heiderman+10
# 2. For other regions, I use the average distance in Zucker+10.
# And if the region is composed of several parts and their distance are measured individually, we estimate the overall distance by average the distance of these parts.
# In addition, we define the uncertainty of the overall distance to be the sqare root of the largest distance uncertainty and the longest distance difference in these parts.

#--------------------------------------------
# Given cloud distance
distance_dict = {
    #--------------
    # c2d provides:
    "perseus": ufloat(250, 50),
    # For Aquila, Serpens
    "serpens": ufloat(260, 10),
    "chamaeleon_2": ufloat(178, 18),
    "ophiuchus": ufloat(125, 25),
    "lupus": ufloat(150, 20),
    "lupus_3": ufloat(200, 20),
    #--------------
    # Gould belt provides:
    "chamaeleon_13": ufloat(200, 20),
    "auriga": ufloat(300, 30),
    "cepheus": ufloat(300, 30),
    "corona_australis": ufloat(130, 25),
    "ic5146": ufloat(950, 80),
    "musca": ufloat(160, 20),
    "scorpius": ufloat(130, 15),
    #--------------
    # Zucker+20 provides:
    "ara": ufloat(1050, 56),
    #"cb28": 398,
    #"cb29": 374,
    "cb34": ufloat(1322, 66),
    #"cma_ob1": 1169,
    "california": ufloat(452, 37),
    #"cam": 235, # Camelopardalis
    #"carina": ufloat(2500, 120),
    "carina_13": ufloat(2530, 261),
    "gem_ob1_south": ufloat(1848, 314),
    #"hercules_3": 230,
    "ic1396_1": ufloat(916, 45),
    "ic2118": ufloat(294, 57),
    "l1228": ufloat(366, 18),
    #"l1228d": 491,
    "l1251": ufloat(351, 17),
    #"l1293": 1083,
    #"l1306_2": 941,
    "l1307_2": ufloat(902, 45),
    #"l1333": 283,
    #"l1335": 647,
    "l1340": ufloat(858, 42),
    #"l1355": 948,
    #"l1617": 414,
    "l1622": ufloat(418, 20),
    "l291": ufloat(1439, 71),
    #"l977": 660,
    "l988": ufloat(619, 34),
    #"lbn906": 287,
    "lagoon": ufloat(1272, 124),
    #"m17": 1488,
    #"m20": 1253,
    "maddalena": ufloat(2110, 211),
    "ngc2264_e": ufloat(770, 44),
    #"ngc2264_w": 715, 
    "mon_r2_136": ufloat(784, 50),
    "ngc2362_2": ufloat(1173, 58),
    #"ngc6604": 1352,
    "north_america_w": ufloat(807, 153),
    #"orion": 433,
    "orion_a": ufloat(426, 82),
    "orion_ngc2071": ufloat(426, 30),
    "orion_ngc2024": ufloat(432, 46),
    #"orion_lam": 406,
    "orion_lam_i": ufloat(409, 37),
    #"pegasus_234": 238,
    "pipe": ufloat(180, 9),
    #"rcw38": 1595,
    "rosette": ufloat(1337, 167),
    #"s106": 1091,
    "sh2_232": ufloat(1713, 171),
    "taurus": ufloat(147, 42),
    #"w3": 1873,
    "w3_ii": ufloat(2184, 218),
    "w3_iii": ufloat(1659, 165),
    #"w5": 2026,
    "cygnus_x": ufloat(1164, 22),
}
