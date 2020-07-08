#!/usr/bin/python3
import numpy as np
from uncertainties import ufloat

index_HC = [
    'cloud', 
    'gas_sigma',
    'e_gas_sigma',
    'sfr_sigma',
    'e_sfr_sigma',
]

Heiderman_cloud = np.array([
# Cloud, gas_sigma, e_gas_sigma, sfr_sigma, e_sfr_sigma
    [ 'Cha II  ', 64.3, 27, 0.605 , 0.35],
    [ 'Lup I   ', 57.9, 31, 0.367 , 0.22],
    [ 'Lup III ', 59.2, 31, 1.10  , 0.63],
    [ 'Lup IV  ', 75.0, 32, 1.19  , 0.72],
    [ 'Oph     ', 105 , 42, 2.45  , 1.6],
    [ 'Per     ', 90.0, 33, 1.31  , 0.88],
    [ 'Ser     ', 138 , 36, 3.29  , 1.8],
    [ 'AurN    ', 92.9, 11, 0.207 , 0.12],
    [ 'Aur     ', 92.4, 11, 0.854 , 0.49],
    [ 'Cep     ', 68.7, 17, 0.776 , 0.45], # multiple regions
    [ 'Cha III ', 47.5, 10, 0.0357, 0.021],
    [ 'Cha I   ', 91.1, 12, 2.36  , 1.4],
    [ 'CrA     ', 92.1, 13, 3.37  , 2.2],
    [ 'IC5146E ', 54.9, 11, 0.378 , 0.21],
    [ 'IC5146NW', 59.1, 10, 0.108 , 0.061],
    [ 'Lup VI  ', 67.5, 11, 1.66  , 1.0],
    [ 'Lup V   ', 60.3, 10, 0.915 , 0.55],
    [ 'Mus     ', 49.1, 10, 0.440 , 0.26],
    [ 'Sco     ', 85.2, 23, 0.343 , 0.20], # multiple regions
    [ 'Ser-Aqu ', 136 , 13, 2.01  , 1.1], # multiple regions
], dtype = object)
Heiderman_Av_regions_class_f = np.array([
# Cloud, gas_sigma, sfr_sigma
    ['Cha II 1' , 53.6, 0.18],
    ['Cha II 2' , 92.6, 0.795],
    ['Cha II 3' , 147 , 4.68],
    ['Cha II 4' , 193 , 19.3],
    ['Lup I 1'  , 51.9, 0.174],
    ['Lup I 2'  , 109 , 1.97],
    ['Lup I 3'  , 185 , 15.0],
    ['Lup III 1', 54.8, 0.188],
    ['Lup III 2', 153 , 3.29],
    ['Lup III 3', 248 , 11.1],
    ['Lup IV 1' , 61.5, 0.619],
    ['Lup IV 2' , 157 , 8.43],
    ['Lup IV 3' , 267 , 15.4],
    ['Oph 1'    , 87.2, 0.105],
    ['Oph 2'    , 198 , 2.26],
    ['Oph 3'    , 319 , 12.1],
    ['Oph 4'    , 435 , 57.4],
    ['Oph 5'    , 542 , 96.0],
    ['Per 1'    , 66.9, 0.0268],
    ['Per 2'    , 122 , 0.364],
    ['Per 3'    , 194 , 5.12],
    ['Per 4'    , 261 , 10.3],
    ['Per 5'    , 317 , 6.36],
    ['Per 6'    , 404 , 78.7],
    ['Ser 1'    , 120 , 0.105],
    ['Ser 2'    , 180 , 1.10],
    ['Ser 3'    , 243 , 7.57],
    ['Ser 4'    , 307 , 54.8],
], dtype = object)
Heiderman_Av_regions_class_i = np.array([
# Cloud, gas_sigma, sfr_sigma
    ['Cha II 1' , 53.6, 0.116], 
    ['Cha II 2' , 92.6, 0.511],
    ['Cha II 3' , 147 , 3.01],
    ['Cha II 4' , 193 , 12.4],
    ['Lup I 1'  , 51.9, 0.112],
    ['Lup I 2'  , 109 , 1.26],
    ['Lup I 3'  , 185 , 9.66],
    ['Lup III 1', 54.8, 0.0604],
    ['Lup III 2', 153 , 2.12],
    ['Lup III 3', 248 , 7.14],
    ['Lup IV 1' , 61.5, 0.398],
    ['Lup IV 2' , 157 , 5.42],
    ['Lup IV 3' , 267 , 9.89],
    ['Oph 1'    , 87.2, 0.0338],
    ['Oph 2'    , 198 , 0.484],
    ['Oph 3'    , 319 , 7.89],
    ['Oph 4'    , 435 , 24.3],
    ['Oph 5'    , 542 , 52.3],
    ['Per 1'    , 66.9, 0.0516],
    ['Per 2'    , 122 , 0.883],
    ['Per 3'    , 194 , 4.33],
    ['Per 4'    , 261 , 17.1],
    ['Per 5'    , 317 , 33.2],
    ['Per 6'    , 404 , 50.6],
    ['Ser 1'    , 120 , 0.135],
    ['Ser 2'    , 180 , 0.709],
    ['Ser 3'    , 243 , 7.03],
    ['Ser 4'    , 307 , 79.8],
], dtype = object)

index_WC = [
    'cloud', 
    'gas_sigma',
    'e_gas_sigma',
    'sfr_sigma',
    'e_sfr_sigma',
]

# Ratio means our data/ other data
ratio_gas = ufloat(2.63, 0.42)
ratio_sfr = ufloat(0.38, 0.31)

Wu_cloud = np.array([
# Cloud, gas_sigma, e_gas_sigma, sfr_sigma, e_sfr_sigma
    ['W3(OH)     ', 3.39, 0.13, 1.35, 0.12,],
    ['RCW142     ', 3.40, 0.14, 1.08, 0.13,],
    ['W28A2(1)   ', 3.66, 0.14, 2.12, 0.13,],
    ['G9.62+0.10 ', 3.28, 0.13, 1.45, 0.14,],
    ['G10.60-0.40', 3.32, 0.12, 1.83, 0.12,],
    ['G12.21-0.10', 2.63, 0.24, 0.28, 0.23,],
    ['G13.87+0.28', 2.28, 0.15, 0.61, 0.13,],
    ['G23.95+0.16', 2.28, 0.25, 0.79, 0.21,],
    ['W43S       ', 2.63, 0.14, 1.51, 0.14,],
    ['W44        ', 2.79, 0.18, 1.00, 0.16,],
    ['G35.58-0.03', 3.41, 0.24, 0.89, 0.22,],
    ['G48.61+0.02', 1.98, 0.14, 0.75, 0.13,],
    ['W51M       ', 3.14, 0.17, 1.53, 0.17,],
    ['S87        ', 2.76, 0.16, 0.97, 0.12,],
    ['S88B       ', 2.68, 0.19, 1.31, 0.15,],
    ['K3-50      ', 3.26, 0.12, 1.75, 0.13,],
    ['ON1        ', 2.83, 0.14, 0.73, 0.13,],
    ['ON2S       ', 2.76, 0.16, 1.44, 0.14,],
    ['W75N       ', 3.13, 0.13, 1.50, 0.12,],
    ['DR21S      ', 3.20, 0.13, 1.75, 0.12,],
    ['W75(OH)    ', 3.21, 0.13, 0.62, 0.13,],
    ['CEPA       ', 3.44, 0.17, 2.00, 0.13,],
    ['IRAS20126  ', 2.98, 0.18, 1.22, 0.13,],
    ['IRAS20220  ', 2.63, 0.21, 0.29, 0.18,],
    ['IRAS23385  ', 2.79, 0.19, 0.43, 0.15,],
])
