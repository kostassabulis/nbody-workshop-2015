import numpy as np
import matplotlib.pyplot as plt

def density_distance_hist(bodies):
    distances = np.sqrt(np.sum(bodies.r**2, axis=1))
    distances = np.sort(distances)
    plt.hist(distances, bins=100)
    plt.show()
