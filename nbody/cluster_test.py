from collections import namedtuple

import numpy as np
import matplotlib.cm as cm

import euler
import leapfrog
import icc 
import constants
from snapshots.display import SnapshotRenderer
from snapshots.storage import SnapshotStorage

total_time = 10000 * constants.YR
dt = 1 * constants.YR
dt_output = 5 * constants.YR

epsilon = 0.2 #Smoothing parameter
d= 1.0e14
bodies = icc.uniform_distribution(500, d)
#bodies.m *= constants.SOLAR_MASS # tai jau daroma icc

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies.r)

snapshot_renderer = SnapshotRenderer.for_clusters(snapshot_storage, bounds=[-d, d])
snapshot_renderer.display_step()

for i, current_t in enumerate(leapfrog.simulate_step(bodies, dt, constants.G, epsilon, dt_output=dt_output)):
    if current_t >= total_time:
        break

    print "%e/%e" %(current_t, total_time)

    snapshot_storage.append(bodies.r)
    snapshot_renderer.display_step()

snapshot_storage.save("snapshot.pkl")
