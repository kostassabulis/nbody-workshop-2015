"""Various utility functions, mostly dealing with input/output"""

import os

import numpy as np

def load_snapshots(directory_name, stack_coords=False):
    """Loads files by traversing a directory and reading in a filename sorted order"""
    data = []
    for root, dirs, files in os.walk(directory_name):
        for file_name in sorted(files, key=lambda x: int(x.split(".")[-1])):
            #This needs fixing, but I'll leave it like this until we unify our formats
            if "csv" in file_name.split("."):
                bodies = np.loadtxt(os.path.join(root, file_name), delimiter=",", skiprows=1, unpack=stack_coords)
                data.append(bodies)

    return np.array(data)
    
def save_snapshot(snapshot, file_name):
    f = open(file_name, 'w')
    f.write("x,y,z\n")
    for i in range(snapshot.shape[0]):
        f.write("%e,%e,%e\n" % (snapshot[i, 0], snapshot[i, 1], snapshot[i, 2]))
    f.close()