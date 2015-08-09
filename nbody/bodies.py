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
        return self.r.shape, self.v.shape, self.m.shape, self.t.shape

    def time_arr(self, total, out_step):
        self.t = np.zeros(int(total/out_step)+1)

    def sort_by_radius(self, center=(0, 0, 0)):
        radius = np.sqrt(np.sum(self.r**2 - center, axis=1))
        sorted_indexes = np.argsort(radius)
        self.r = self.r[sorted_indexes]
        self.v = self.v[sorted_indexes]
        self.m = self.m[sorted_indexes]
        return self

    def __getitem__(self, item):
        if len(self.r.shape) == 3:
            k = Bodies()
            k.r = self.r[item]
            k.v = self.v[item]
            k.m = self.m[item]
            return k
        else:
            return self.r[item], self.v[item], self.m[item]

    def __repr__(self):
        return '{}'.format(self.to_array())
