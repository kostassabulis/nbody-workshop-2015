"""Base body storage class used in simulations
"""

import numpy as np
from matplotlib.colors import colorConverter
#a = colorConverter.colors

class Bodies(object):
    def __init__(self, r=None, v=None, m=None, t=None, color=None):
        self.r = r
        self.v = v
        self.m = m
        self.t = t
        self.color = color

    def to_array(self):
        return np.concatenate([self.r, self.v, self.m[:, np.newaxis], colorConverter.to_rgba_array(self.color)], axis=1)

    def from_array(self, arr):
        self.r = arr[:, :3]
        self.v = arr[:, 3:6]
        self.m = arr[:, 6]

    def from_pickle(self, arr):
        self.r = arr[:, :, :3]
        self.v = arr[:, :, 3:6]
        self.m = arr[:, :, 6]
        self.color = arr[:, :, 7:]

    def copy(self, arr):
        self.r = np.copy(arr.r)
        self.v = np.copy(arr.v)
        self.m = np.copy(arr.m)
        self.color = np.copy(arr.color)
        self.t = np.copy(arr.t)

    def shape(self):
        return self.r.shape, self.v.shape, self.m.shape, self.color.shape, self.t.shape

    def time_arr(self, total, out_step):
        self.t = np.zeros(int(total/out_step)+1)

    def sort_by_radius(self, center=(0, 0, 0)):
        radius = np.sqrt(np.sum((self.r - center)**2, axis=1))
        sorted_indexes = np.argsort(radius)
        self.r = self.r[sorted_indexes]
        self.v = self.v[sorted_indexes]
        self.m = self.m[sorted_indexes]
        self.color = self.color[sorted_indexes]
        radius = radius[sorted_indexes]
        return radius

    def __getitem__(self, item):
        if self.r.ndim == 3:
            k = Bodies()
            k.r = self.r[item]
            k.v = self.v[item]
            k.m = self.m[item]
            k.color = self.color[item]
            return k
        if self.r.ndim == 2:
            return self.r[item], self.v[item], self.m[item], self.color[item]

    def __repr__(self):
        return '{}'.format(self.to_array())
