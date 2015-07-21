'''
__author__ = 'Tomas'


'''

## plummer(N, r_pl)  N - number of stars; r_pl - cluster scale radius
## zvaigzdziu mases grazinamos kilogramais. koordinates grazinamos r_pl vienetais. Greiciai grazinami metrais per sekunde

## uniform_distribution(N, R) N - number of stars; R - zvaigzdiu sferos spindulys
## zvaigzdziu mases grazinamos kilogramais. koordinates grazinamos R vienetais. Greiciai = 0

from collections import namedtuple
import numpy as np
import constants

def plummer(N, r_pl): 
    M_min = 0.08 # min zvaigzdes mase
    M_max = 100 # max zvaigzdes mase
    mStars = IMF_salpeter(N, M_min, M_max) * constants.SOLAR_MASS
    rStars = np.sort(distance_plummer(N, r_pl))
    xStars, yStars, zStars = vector_projection(N, rStars)
    vStars = velocity_kepler(N, mStars, rStars)
    v_xStars, v_yStars, v_zStars = vector_projection(N, vStars)
    bodies = namedtuple("Bodies", ["r", "v", "m"])
    bodies.r = np.transpose(np.array([xStars, yStars, zStars]))
    bodies.m = np.array(mStars)
    bodies.v = np.transpose(np.array([v_xStars, v_yStars, v_zStars]))

    return bodies

def uniform_distribution(N, R):
    mStars = np.ones(N) * constants.SOLAR_MASS
    xStars, yStars, zStars = vector_projection(N, np.random.sample(N) * R)
    bodies = namedtuple("Bodies", ["r", "v", "m"])
    bodies.r = np.transpose(np.array([xStars, yStars, zStars]))
    bodies.m = np.array(mStars)
    bodies.v = np.zeros(bodies.r.shape)
    M = np.sum(mStars)
    ro = M/(4./3.*np.pi*R**3)
    print "Expected collapse time :" + str(np.sqrt(3*np.pi/32./constants.G/ro))
    return bodies

def IMF_salpeter(N, M_min, M_max):
    p = -2.35 +1 # Salpeter funkcijos koff. +1. nes suintegravus taip
    a = np.power(M_min, p)
    b = np.power(M_max, p)
    c = np.random.sample(N) * (b - a) + a
    return np.power(c, 1. / p)

def distance_plummer(N, r_pl):
    rStars = (np.random.sample(N)**(-2./3)-1)**(-0.5) * r_pl
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