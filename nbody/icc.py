'''
__author__ = 'Tomas'


'''

## plummer(N, r_pl)  N - number of stars; r_pl - cluster scale radius
## zvaigzdziu mases grazinamos kilogramais. koordinates grazinamos r_pl vienetais. Greiciai grazinami metrais per sekunde

## uniform_distribution(N, R) N - number of stars; R - zvaigzdiu sferos spindulys
## zvaigzdziu mases grazinamos kilogramais. koordinates grazinamos R vienetais. Greiciai = 0

import numpy as np
from bodies import Bodies
import constants

def plummer(N, r_pl): 
    M_min = 0.08 # min zvaigzdes mase
    M_max = 100 # max zvaigzdes mase
    mStars = IMF_salpeter(N, M_min, M_max) * constants.SOLAR_MASS
    rStars = np.sort(distance_plummer(N, r_pl))
    xStars, yStars, zStars = vector_projection(N, rStars)
    vStars = velocity_kepler(N, mStars, rStars)
    v_xStars, v_yStars, v_zStars = vector_projection(N, vStars)
    bodies = Bodies()
    bodies.r = np.transpose(np.array([xStars, yStars, zStars]))
    bodies.m = np.array(mStars)
    bodies.v = np.transpose(np.array([v_xStars, v_yStars, v_zStars]))

    return bodies

def uniform_sphere(N, R):
    phi = np.random.random((N)) * 2.0 * np.pi
    costheta = (np.random.random((N)) - 0.5) * 2.0
    u = np.random.random((N))

    theta = np.arccos(costheta)
    r = R * u**(1.0/3.0)

    x_stars = r * np.sin(theta) * np.cos(phi) 
    y_stars = r * np.sin(theta) * np.sin(phi)
    z_stars = r * np.cos(theta)
   
    bodies = Bodies()
    bodies.r = np.transpose(np.array([x_stars, y_stars, z_stars]))
    bodies.m = np.ones(N) * constants.SOLAR_MASS
    bodies.v = np.zeros(bodies.r.shape)
    
    M = np.sum(bodies.m)
    ro = M/(4./3.*np.pi*R**3)
    print "Expected collapse time : {:e}".format(np.sqrt(3*np.pi/32./constants.G/ro))
    return bodies

def uniform_distribution(N, R, koeff=1./3.):
    #koeff nulemia pasiskirstyma.
    x_stars, y_stars, z_stars = vector_projection(N, np.power(np.random.sample(N), koeff) * R)

    bodies = Bodies()
    bodies.r = np.transpose(np.array([x_stars, y_stars, z_stars]))
    bodies.m = np.ones(N) * constants.SOLAR_MASS
    bodies.v = np.zeros(bodies.r.shape)

    M = np.sum(bodies.m)
    ro = M/(4./3.*np.pi*R**3)
    print "Expected collapse time : {:e}".format(np.sqrt(3*np.pi/32./constants.G/ro))
    return bodies

def IMF_salpeter(N, M_min, M_max):
    p = -2.35 +1 # Salpeter funkcijos koff. +1. nes suintegravus taip
    a = np.power(M_min, p)
    b = np.power(M_max, p)
    c = np.random.sample(N) * (b - a) + a
    return np.power(c, 1. / p)

def distance_plummer(N, r_pl):
    rStars = r_pl / np.sqrt(np.random.sample(N)**(-2./3) - 1) #Aarseth et al. 1974
    return rStars

def vector_projection(N, vector):
    zProjection = 2*vector*np.random.sample(N) - vector
    teta = 2* np.pi * np.random.sample(N)
    xProjection = (vector*vector - zProjection*zProjection)**0.5 * np.cos(teta)
    yProjection = (vector*vector - zProjection*zProjection)**0.5 * np.sin(teta)
    return xProjection, yProjection, zProjection

def velocity_kepler(N, mStars, rStars):
    vStars = np.zeros(N)
    M = 0
    for i,r in enumerate(rStars):
        M += mStars[i]
        vStars[i] = np.sqrt(constants.G * M / rStars[i])
    return vStars
