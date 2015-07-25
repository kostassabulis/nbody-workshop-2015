#from collections import namedtuple

#import numpy as np
#import matplotlib.cm as cm

#import euler
#import leapfrog
import leapfrog_adaptive
import icc 
import constants
from snapshots.display import SnapshotRenderer
from snapshots.storage import SnapshotStorage

total_time = 1000 * constants.YR
dt_min = 0.01 * constants.YR
dt_output = 10 * constants.YR

epsilon = 0.2 #Smoothing parameter
d= 1.0e14
alpha = 0.0001 #adaptive time step parameter
bodies = icc.uniform_distribution(500, d)
#bodies.m *= constants.SOLAR_MASS # tai jau daroma icc

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies.r)

#snapshot_renderer = SnapshotRenderer.for_clusters(snapshot_storage, bounds=[-d, d])
#snapshot_renderer.display_step()

for i, current_t in enumerate(leapfrog_adaptive.simulate_step(bodies, dt_min, constants.G, epsilon, dt_output=dt_output, alpha=alpha)):
    if current_t >= total_time:
        break

    print "%e/%e" %(current_t, total_time)

    snapshot_storage.append(bodies.r)
#    snapshot_renderer.display_step()

snapshot_storage.save("snapshot.pkl")


