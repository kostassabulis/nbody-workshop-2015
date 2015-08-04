"""Base body storage class used in simulations
"""

import numpy as np


class Bodies(object):
    def __init__(self, r=None, v=None, m=None, t=None):
        self.r = r
        self.v = v
        self.m = m
        self.t = t

    def to_array(self):
        return np.concatenate([self.r, self.v, self.m[:, np.newaxis]], axis=1)

    def from_array(self, arr):
        self.r = arr[:, :3]
        self.v = arr[:, 3:6]
        self.m = arr[:, 6:]

    def from_pickle(self, arr):
        self.r = arr[:, :, :3]
        self.v = arr[:, :, 3:6]
        self.m = arr[:, :, 6]

    def copy(self, arr):
        self.r = np.copy(arr.r)
        self.v = np.copy(arr.v)
        self.m = np.copy(arr.m)
        self.t = np.copy(arr.t)

    def shape(self):
        return self.r.shape, self.v.shape, self.m.shape #, self.t.shape

    def time_arr(self, total, out_step):
        self.t = np.zeros(int(total/out_step)+1)
