import nbody as nb
from nbody.bodies import Bodies
from nbody.snapshots.display import SnapshotRenderer
from nbody.snapshots.storage import SnapshotStorage
import numpy as np
import matplotlib.cm as cm

#nb.constants.G, nb.constants.SOLAR_MASS, nb.constants.YR = nb.constants.unitstocode() #conversion to code units [PC], [SOLAR_MASS] and G = 1
total_time = 1000 * nb.constants.YR
dt_min = 0.1 * nb.constants.YR
dt_output = 10 * nb.constants.YR

epsilon = nb.constants.AU#/nb.constants.PC #Smoothing parameter
d = 1.0e14 #/nb.constants.PC
alpha = 0.0001 #adaptive time step parameter
N = 500

bodies, distribution = nb.icc.plummer(N, d)
bodies_phys = bodies.clone()
conversion_params = nb.constants.convert_to_sim_units(bodies)

def mass_colors(snapshots, time_step):
    curr_masses = snapshots[time_step, :, 6]
    norm_mass = (curr_masses - curr_masses.min()) / (curr_masses.max() - curr_masses.min())

    cmap = cm.get_cmap("RdBu")
    return [cmap(abs(1.0 - norm_mass[i])) for i in range(norm_mass.shape[0])] 

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies_phys)

space_coeff = nb.constants.space_coeff(*conversion_params)
snapshot_renderer = SnapshotRenderer.for_clusters(snapshot_storage, 
        recoloring_func=mass_colors, 
        bounds=[-2e14, 2e14], 
        verbose=1, 
        angle=[45, 45])
#snapshot_renderer.display_step()

time_coeff = nb.constants.time_coeff(*conversion_params)
for i, current_t in enumerate(nb.leapfrog_adaptive.simulate_step(bodies, 
        epsilon=epsilon / space_coeff, alpha=alpha, dt_output=dt_output / time_coeff, max_dt_bins=5)):
    if current_t >= total_time / time_coeff:
        break

    print "{}/{}".format(current_t * time_coeff / nb.constants.YR, total_time / nb.constants.YR)

    bodies_phys = bodies.clone()
    nb.constants.convert_from_sim_units(bodies_phys, *conversion_params)
    snapshot_storage.append(bodies_phys)
    #snapshot_renderer.display_step()

name = "{:s}_N{:d}_T{:d}_E{:.0e}_d{:.0e}_color00".format(distribution, N, int(total_time / nb.constants.YR), epsilon, d)
snapshot_renderer.run(name + ".mp4")
snapshot_storage.save(name + ".pkl")
