import nbody as nb
from nbody.snapshots.display import SnapshotRenderer
from nbody.snapshots.storage import SnapshotStorage
import numpy as np

#nb.constants.G, nb.constants.SOLAR_MASS, nb.constants.YR = nb.constants.unitstocode() #conversion to code units [PC], [SOLAR_MASS] and G = 1
total_time = 10000 * nb.constants.YR
dt_min = 0.1 * nb.constants.YR
dt_output = 10 * nb.constants.YR

epsilon = nb.constants.AU#/nb.constants.PC #Smoothing parameter
d = 1.0e14 #/nb.constants.PC
alpha = 0.0001 #adaptive time step parameter
N = 500

bodies, distribution = nb.icc.plummer(N, d)
bodies.time_arr(total_time, dt_output)
#bodies = nb.icc.super_massive_black_hole(bodies)
bodies = nb.icc.test_galaxy(bodies, d=1e16)


snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies)

snapshot_renderer = SnapshotRenderer.for_clusters(snapshot_storage, bounds=[-d, d])
#snapshot_renderer.display_step()

for i, current_t in enumerate(nb.leapfrog_adaptive.simulate_step(bodies, G=nb.constants.G, epsilon=epsilon, dt_output=dt_output, alpha=alpha, max_dt_bins=5)):
    if current_t >= total_time:
        break

    print "%e/%e" %(current_t, total_time)

    snapshot_storage.append(bodies)
#   snapshot_renderer.display_step()

#nb.constants.G, nb.constants.SOLAR_MASS, nb.constants.YR = nb.constants.codetounits() #Back to SI units
name = '{:s}_N{:d}_T{:d}_E{:.0e}_d{:.0e}_galaxy04'.format(distribution, N, int(total_time / nb.constants.YR), epsilon, d)
snapshot_renderer.run(name + ".mp4")
snapshot_storage.save("nbody/" + name + ".pkl")
np.save('nbody/{}_time.npy'.format(name), bodies.t)
