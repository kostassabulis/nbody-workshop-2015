"""Various astronomical constants in SI units"""

import scipy.constants as sc
import numpy as np

SOLAR_MASS = 1.98e30            #[kg]
AU = sc.astronomical_unit       #1.5e11 [m]
YR = sc.Julian_year             #~3.15569e7 [s]
G = sc.G                        #6.67e-11  [m^3 kg^-1 s^-2]
PC = sc.parsec                  #3.086e+16 [m]

TU = np.sqrt(PC**3/SOLAR_MASS/G) #Time Unit [s]
TUcoef = YR/TU

def unitstocode():
    G = 1.
    YR = TUcoef
    SOLAR_MASS = 1.
    return G, SOLAR_MASS, YR
    
def codetounits():
    G = sc.G
    YR = TUcoef
    SOLAR_MASS = 1.98e30 
    return G, SOLAR_MASS, YR
