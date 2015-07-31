import nbody as nb
from nbody.snapshots.display import SnapshotRenderer
from nbody.snapshots.storage import SnapshotStorage
import sys

total_time = 1000 * nb.constants.YR
dt_min = 1 * nb.constants.YR
dt_output = 10 * nb.constants.YR

epsilon = 0.2 #Smoothing parameter
d = 1.0e14
alpha = 0.0001 #adaptive time step parameter
bodies = nb.icc.uniform_sphere(500, d)

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies)
#sys.exit()

snapshot_renderer = SnapshotRenderer.for_clusters(snapshot_storage, bounds=[-d, d])
#snapshot_renderer.display_step()

for i, current_t in enumerate(nb.leapfrog_adaptive.simulate_step(bodies, dt_min, nb.constants.G, epsilon, dt_output=dt_output, alpha=alpha)):
    if current_t >= total_time:
        break

    print "%e/%e" %(current_t, total_time)

    snapshot_storage.append(bodies)
#    snapshot_renderer.display_step()
#snapshot_renderer.run()
snapshot_storage.save("snapshot.pkl")
