from collections import namedtuple

import numpy as np
import matplotlib.cm as cm

import euler
import display

M_solar = 1.98e30
AU = 1.5e11
yr = 3.15569e7

bodies = namedtuple("Bodies", ["r", "v", "m"])
bodies.r = np.array([
        [0.0, 0.0, 0.0],
        [0.387 * AU, 0.0, 0.0],
        [-0.728 * AU, 0.0, 0.0],
        [1 * AU, 0.0, 0.0]])

bodies.m = np.array([M_solar, 3.3e23, 4.86e24, 5.97e24])
bodies.v = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 47362, 0.0],
        [0.0, -35020, 0.0],
        [0.0, 29780, 0.0]])

total_time = 1 * yr
dt = 0.0001 * yr
dt_output = 0.01 * yr

body_history = np.zeros((total_time / dt_output + 1, bodies.r.shape[0], bodies.r.shape[1]))
body_history[0, :, :] = bodies.r
for i, current_t in enumerate(euler.simulate_step(bodies, dt, dt_output)):
    if current_t >= total_time:
        break

    print "{}/{}".format(current_t, total_time)
    
    body_history[i + 1, :, :] = bodies.r

snapshot_renderer = display.SnapshotRenderer(body_history, line_style="-", marker_style=".", 
                                             history_length=100, fade=True, color=cm.get_cmap())
snapshot_renderer.run()
