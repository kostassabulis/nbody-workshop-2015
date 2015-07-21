from collections import namedtuple

import numpy as np
import matplotlib.cm as cm

import euler
import leapfrog
import icc
import display
import constants

total_time = 10000 * constants.YR
dt = 10 * constants.YR
dt_output = 50 * constants.YR

d= 1.0e14
bodies = icc.plummer(100, d)
#bodies.m *= constants.SOLAR_MASS # tai jau daroma icc

body_history = np.zeros((total_time / dt_output + 1, bodies.r.shape[0], bodies.r.shape[1]))
body_history[0, :, :] = bodies.r


snapshot_renderer = display.SnapshotRenderer(body_history, blocking=True, line_style="", marker_style=".", 
                                             history_length=0, fade=False, verbose=0, bounds=[-2*d, 2*d])
for i, current_t in enumerate(leapfrog.simulate_step(bodies, dt, G=constants.G, dt_output=dt_output)):
    if current_t >= total_time:
        break

    print "%e/%e" %(current_t, total_time)

    
    body_history[i + 1, :, :] = bodies.r
    snapshot_renderer.run(updated_data=body_history[:i + 1, :, :])


