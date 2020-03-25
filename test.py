#!/usr/bin/python3
from astropy.coordinates import SkyCoord
from dustmaps.bayestar import BayestarQuery

coords = SkyCoord('00h30m25.3s', '15d15m58.1s', frame='icrs')
bayestar = BayestarQuery(max_samples=2)
# ebv stands for E(B-V)
ebv = bayestar(coords)
print(ebv)
print(bayestar.distances)
