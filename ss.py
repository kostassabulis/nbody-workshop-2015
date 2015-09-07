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
dt_output = 1.0 * nb.constants.YR

bodies_phys = bodies.clone()
conversion_params = nb.constants.convert_to_sim_units(bodies)

space_coeff = nb.constants.space_coeff(*conversion_params)
time_coeff = nb.constants.time_coeff(*conversion_params)

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies_phys)

snapshot_renderer = SnapshotRenderer.for_orbits(snapshot_storage, 
                                                bounds=(-nb.constants.AU, nb.constants.AU))
snapshot_renderer.display_step()

for i, current_t in enumerate(nb.leapfrog_adaptive.simulate_step(bodies, 
        epsilon=epsilon / space_coeff, dt_output=dt_output / space_coeff, alpha=alpha, max_dt_bins=5)):
    if current_t >= total_time / time_coeff:
        break

    print "{}/{}".format(current_t * time_coeff / nb.constants.YR, total_time / nb.constants.YR)
    
    bodies_phys = bodies.clone()
    nb.constants.convert_from_sim_units(bodies_phys, *conversion_params)
    snapshot_storage.append(bodies_phys)
    snapshot_renderer.display_step()
