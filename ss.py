import numpy as np

import nbody as nb
from nbody.bodies import Bodies
from nbody.snapshots.display import SnapshotRenderer
from nbody.snapshots.storage import SnapshotStorage

bodies = Bodies()
bodies.r = np.array([
        [0.0, 0.0, 0.0],
        [0.387 * nb.constants.AU, 0.0, 0.0],
        [-0.728 * nb.constants.AU, 0.0, 0.0],
        [1 * nb.constants.AU, 0.0, 0.0]])

bodies.m = np.array([nb.constants.SOLAR_MASS, 3.3e23, 4.86e24, 5.97e24])
bodies.v = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 47362, 0.0],
        [0.0, -35020, 0.0],
        [0.0, 29780, 0.0]])

total_time = 10 * nb.constants.YR
dt_min = 0.000001 * nb.constants.YR
epsilon = 0.2
alpha = 0.001 #adaptive time step parameter
dt_output = 0.01 * nb.constants.YR

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies.r)

snapshot_renderer = SnapshotRenderer.for_orbits(snapshot_storage, 
                                                bounds=(-nb.constants.AU, nb.constants.AU))
snapshot_renderer.display_step()

for i, current_t in enumerate(leapfrog_adaptive.simulate_step(bodies, dt_min, G=nb.constants.G, epsilon=epsilon, dt_output=dt_output, alpha=alpha)):
    if current_t >= total_time:
        break

    print "{}/{}".format(current_t, total_time)
    
    snapshot_storage.append(bodies.r)
    snapshot_renderer.display_step()
