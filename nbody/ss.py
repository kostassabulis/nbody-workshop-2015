from collections import namedtuple

import numpy as np
import matplotlib.cm as cm

import euler
import leapfrog
import display

import constants

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

body_history = np.zeros((total_time / dt_output + 1, bodies.r.shape[0], bodies.r.shape[1]))
body_history[0, :, :] = bodies.r


snapshot_renderer = display.SnapshotRenderer(body_history, blocking=True, line_style="-", marker_style=".", 
                                             history_length=0, fade=False, color=cm.get_cmap(), verbose=0,
                                             bounds=(-constants.AU, constants.AU))

for i, current_t in enumerate(euler.simulate_step(bodies, dt, G=constants.G, dt_output=dt_output)):
    if current_t >= total_time:
        break

    print "{}/{}".format(current_t, total_time)
    
    body_history[i + 1, :, :] = bodies.r
    snapshot_renderer.run(updated_data=body_history[:i + 1, :, :])
