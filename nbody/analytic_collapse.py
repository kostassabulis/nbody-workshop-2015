__author__ = 'Eimantas'

import numpy as np
from scipy.optimize import fsolve
import constants

def radius_at_t(t, r_0, rho_0):
    t_ff = np.sqrt(3*np.pi/(32*constants.G*rho_0))
    tau = t/t_ff
    f = lambda x: np.arccos(np.sqrt(x)) - np.sqrt(x*(1-x)) - 0.5*np.pi*tau
    x_guess = tau*r_0
    x_at_tau, infodict, ier, mesg = fsolve(f, x_guess)
    if ier == 1:
        return x_at_tau*r_0
    else:
        print 'Solution not found: ' + mesg
        return x_guess*r_0
