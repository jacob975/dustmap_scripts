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
    # TODO
    # I need to update the Av contour above.
    "musca": ufloat(160, 20),
    "scorpius": ufloat(130, 15),
    #--------------
    # Zucker+20 provides:
    "ara": ufloat(1050, 40),
    #"cb28": 398,
    #"cb29": 374,
    "cb34": ufloat(1322, 66),
    #"cma_ob1": 1169,
    "california": ufloat(452, 13),
    #"cam": 235, # Camelopardalis
    "carina": ufloat(2500, 120),
    "carina_north": ufloat(2530, 180),
    # TODO
    # I need to update the uncertainties of distance above.
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
    "l1333": 283,
    "l1335": 647,
    "l1340": 858,
    "l1355": 948,
    "l1617": 414,
    "l1622": 418,
    "l291": 1439,
    "l977": 660,
    "l988": 627,
    "lbn906": 287,
    "lagoon": 1325,
    "m17": 1488,
    "m20": 1253,
    "maddalena": 2110,
    "ngc2264": 771,
    "mon_r2_136": 799,
    "ngc2362": 1173,
    "ngc6604": 1352,
    "north_america": 834,
    "orion": 433,
    "orion_lam": 406,
    "pegasus_234": 238,
    "pipe": 180,
    "rcw38": 1595,
    "rosette": 1356,
    "s106": 1091,
    "sh2_231_232": 1616,
    "taurus": 147,
    "w3": 1873,
    "w5": 2026,
    "cygnus_x": ufloat(1164, 22),
}
