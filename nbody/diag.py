import numpy as np
import matplotlib.pyplot as plt


def density_distance_hist(bodies, out_file=None):
    distances = np.sqrt(np.sum(bodies.r ** 2, axis=1))
    distances = np.sort(distances)
    plt.hist(distances, bins=100)
    if out_file is not None:
        plt.savefig(out_file)
    plt.show()
