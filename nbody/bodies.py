"""Base body storage class used in simulations
"""

import numpy as np

class Bodies(object):
    def __init__(self, r=None, v=None, m=None):
        self.r = r
        self.v = v
        self.m = m

    def to_array(self):
        return np.concatenate([self.r, self.v, self.m[:, np.newaxis]], axis=1)

    def from_array(self, arr):
        self.r = arr[:, :, :3]
        self.v = arr[:, :, 3:6]
        self.m = arr[:, :, 6]