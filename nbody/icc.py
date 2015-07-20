'''
__author__ = 'Tomas'


'''

## plummer(N, r_pl)  N - number of stars; r_pl - cluster scale radius
## plummer(N, r_pl) grazina x,y,z koordinates ir zvaigzdiu mases(isvardyta tvarka)
## zvaigzdziu mases grazinamos saules masemis
## koordinates grazinamos r_pl vienetais

from collections import namedtuple

import numpy as np

def plummer(N, r_pl): 
    M_min = 0.08 # min zvaigzdes mase
    M_max = 100 # max zvaigzdes mase
    mStars = IMF(N, M_min, M_max)
    rStars = distance(N, r_pl)
    xStars, yStars, zStars = coordinates(N, rStars)

    bodies = namedtuple("Bodies", ["r", "v", "m"])
    bodies.r = np.transpose(np.array([xStars, yStars, zStars]))
    bodies.m = np.array(mStars)
    bodies.v = np.zeros(bodies.r.shape)

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

def coordinates(N, rStars):
    zStars = 2*rStars*np.random.sample(N) - rStars
    tetaStars = 2* np.pi * np.random.sample(N)
    xStars = (rStars*rStars - zStars*zStars)**0.5 * np.cos(tetaStars)
    yStars = (rStars*rStars - zStars*zStars)**0.5 * np.sin(tetaStars)
    return xStars, yStars, zStars

