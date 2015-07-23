from collections import namedtuple

import numpy as np
import matplotlib.cm as cm

import euler
import leapfrog
import constants
from snapshots.display import SnapshotRenderer
from snapshots.storage import SnapshotStorage

bodies = namedtuple("Bodies", ["r", "v", "m"])
bodies.r = np.array([
        [0.0, 0.0, 0.0],
        [0.387 * constants.AU, 0.0, 0.0],
        [-0.728 * constants.AU, 0.0, 0.0],
        [1 * constants.AU, 0.0, 0.0]])

bodies.m = np.array([constants.SOLAR_MASS, 3.3e23, 4.86e24, 5.97e24])
bodies.v = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 47362, 0.0],
        [0.0, -35020, 0.0],
        [0.0, 29780, 0.0]])

total_time = 100 * constants.YR
dt = 0.001 * constants.YR
dt_output = 0.01 * constants.YR

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies.r)

snapshot_renderer = SnapshotRenderer.for_orbits(snapshot_storage, bounds=(-constants.AU, constants.AU))
snapshot_renderer.display_step()

for i, current_t in enumerate(euler.simulate_step(bodies, dt, G=constants.G, dt_output=dt_output)):
    if current_t >= total_time:
        break

    print "{}/{}".format(current_t, total_time)
    
    snapshot_storage.append(bodies.r)
    snapshot_renderer.display_step()
