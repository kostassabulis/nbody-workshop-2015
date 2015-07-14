"""Various utility functions, mostly dealing with input/output"""

import os

import numpy as np

def load_bodies(directory_name, stack_coords=False):
    """Loads files by traversing a directory and reading in a filename sorted order"""
    data = []
    for root, dirs, files in os.walk(directory_name):
        for file_name in sorted(files, key=lambda x: int(x.split(".")[-1])):
            #This needs fixing, but I'll leave it like this until we unify our formats
            if "csv" in file_name.split("."):
                bodies = np.loadtxt(os.path.join(root, file_name), delimiter=",", skiprows=1, unpack=stack_coords)
                data.append(bodies)

    return np.array(data)
