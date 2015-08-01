import nbody as nb
from nbody.snapshots.display import SnapshotRenderer
from nbody.snapshots.storage import SnapshotStorage

total_time = 500 * nb.constants.YR
dt_min = 0.1 * nb.constants.YR
dt_output = 1 * nb.constants.YR

epsilon = nb.constants.AU #Smoothing parameter
d = 1.0e14
alpha = 0.0001 #adaptive time step parameter
N = 500
bodies = nb.icc.uniform_sphere(N, d)

snapshot_storage = SnapshotStorage()
snapshot_storage.append(bodies)

snapshot_renderer = SnapshotRenderer.for_clusters(snapshot_storage, bounds=[-d, d])
#snapshot_renderer.display_step()

for i, current_t in enumerate(nb.leapfrog_adaptive.simulate_step(bodies, dt_min, nb.constants.G, epsilon, dt_output=dt_output, alpha=alpha)):
    if current_t >= total_time:
        break

    print "%e/%e" %(current_t, total_time)

    snapshot_storage.append(bodies)
#    snapshot_renderer.display_step()

name = 'sphere_N' + str(N) + '_T' + str(int(total_time/nb.constants.YR))
snapshot_renderer.run( name + ".mp4")
snapshot_storage.save("nbody/" + name +".pkl")
