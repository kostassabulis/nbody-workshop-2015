'''
__author__ = 'Tomas'


'''

## plummer(N, r_pl)  N - number of stars; r_pl - cluster scale radius
## plummer(N, r_pl) grazina x,y,z koordinates ir zvaigzdiu mases(isvardyta tvarka)
## zvaigzdziu mases grazinamos saules masemis
## koordinates grazinamos r_pl vienetais

from collections import namedtuple
import numpy as np
import constants

def plummer(N, r_pl): 
    M_min = 0.08 # min zvaigzdes mase
    M_max = 100 # max zvaigzdes mase
    mStars = IMF(N, M_min, M_max) * constants.SOLAR_MASS
    rStars = distance(N, r_pl)
    xStars, yStars, zStars = vector_projection(N, rStars)
    vStars = velocity(N, mStars, rStars)
    v_xStars, v_yStars, v_zStars = vector_projection(N, vStars)
    bodies = namedtuple("Bodies", ["r", "v", "m"])
    bodies.r = np.transpose(np.array([xStars, yStars, zStars]))
    bodies.m = np.array(mStars)
    bodies.v = np.transpose(np.array([v_xStars, v_yStars, v_zStars]))

    return bodies

def IMF(N, M_min, M_max):
    p = -2.35 +1 # Salpeter funkcijos koff. +1. nes suintegravus taip
    a = np.power(M_min, p)
    b = np.power(M_max, p)
    c = np.random.sample(N) * (b - a) + a
    return np.power(c, 1. / p)

def distance(N, r_pl):
    rStars = (np.random.sample(N)**(-2./3)-1)**(-0.5) * r_pl
    return rStars

def vector_projection(N, vector):
    zProjection = 2*vector*np.random.sample(N) - vector
    teta = 2* np.pi * np.random.sample(N)
    xProjection = (vector*vector - zProjection*zProjection)**0.5 * np.cos(teta)
    yProjection = (vector*vector - zProjection*zProjection)**0.5 * np.sin(teta)
    return xProjection, yProjection, zProjection

def velocity(N, mStars, rStars):
    vStars = np.zeros(N)
    rStars_sorted = np.sort(rStars)
    M = 0
    for i,r in enumerate(rStars_sorted):
        M += mStars[i]
        vStars[i] = np.sqrt(constants.G * M / rStars_sorted[i])
    return vStars