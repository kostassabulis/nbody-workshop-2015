"""Base body storage class used in simulations
"""

import numpy as np

class Bodies(object):
    def __init__(self, r=None, v=None, m=None, t=0, tags=None):
        self.r = r
        self.v = v
        self.m = m
        self.t = t
        self.tags = tags

    def to_array(self):
        array = np.concatenate(
            [self.r, self.v, self.m[:, np.newaxis], np.tile(np.asarray(self.t), self.m.shape)[:, np.newaxis]], 
            axis=1)

        if self.tags:
            array = np.concatenate([array, self.tags[:, np.newaxis]], axis=1)
        else:
            array = np.concatenate([array, np.zeros_like(self.m)[:, np.newaxis]], axis=1)

        return array

    def from_array(self, arr, t=None):
        self.r = arr[:, :3]
        self.v = arr[:, 3:6]
        self.m = arr[:, 6]
        self.t = arr[0, 7]
        self.tags = arr[:, 8]

    def copy(self, arr):
        self.r = np.copy(arr.r)
        self.v = np.copy(arr.v)
        self.m = np.copy(arr.m)
        self.tags = np.copy(arr.tags)
        self.t = np.copy(arr.t)

    def sort_by_radius(self, center=(0, 0, 0)):
        radius = np.sqrt(np.sum((self.r - center)**2, axis=1))
        sorted_indexes = np.argsort(radius)
        self.r = self.r[sorted_indexes]
        self.v = self.v[sorted_indexes]
        self.m = self.m[sorted_indexes]
        self.tags = self.tags[sorted_indexes]
        radius = radius[sorted_indexes]
        return radius

    def __getitem__(self, item):
        if self.r.ndim == 3:
            k = Bodies()
            k.r = self.r[item]
            k.v = self.v[item]
            k.m = self.m[item]
            k.tags = self.tags[item]
            return k
        if self.r.ndim == 2:
            return self.r[item], self.v[item], self.m[item], self.tags[item]

    def __repr__(self):
        return '{}'.format(self.to_array())
