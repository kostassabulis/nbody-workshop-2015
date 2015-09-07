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

def get_conversion_params(bodies):
    # TODO(ZadrraS, Kostas): Replace this with proper potential energy calculation when it's done.
    potential_energy = 0.0
    for i in range(bodies.m.shape[0]):
        for j in range(bodies.m.shape[0]):
            if i != j:
                potential_energy += bodies.m[i] * bodies.m[j] / np.sqrt(np.sum((bodies.r[i, :] - bodies.r[j, :])**2))

    potential_energy *= -0.5 * G

    sum_mass = np.sum(bodies.m)
    virial_radius = -G * sum_mass**2 / (2 * potential_energy)

    return virial_radius, sum_mass

def convert_to_sim_units(bodies):
    virial_radius, sum_mass = get_conversion_params(bodies)

    bodies.r /= virial_radius
    bodies.m /= sum_mass

    vel_coef = np.sqrt(G * sum_mass / virial_radius)
    bodies.v /= vel_coef
    bodies.t /= virial_radius / vel_coef

    return virial_radius, sum_mass

def convert_from_sim_units(bodies, virial_radius, sum_mass):
    bodies.r *= virial_radius
    bodies.m *= sum_mass
    vel_coef = np.sqrt(G * sum_mass / virial_radius)
    bodies.v *= vel_coef
    bodies.t *= virial_radius / vel_coef
  
def space_coeff(virial_radius, sum_mass):
    return virial_radius

def mass_coeff(virial_radius, sum_mass):
    return sum_mass

def velocity_coeff(virial_radius, sum_mass):
    return np.sqrt(G * sum_mass / virial_radius)

def time_coeff(virial_radius, sum_mass):
    return virial_radius / velocity_coeff(virial_radius, sum_mass)

