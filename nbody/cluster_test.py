from collections import namedtuple

import numpy as np
import matplotlib.cm as cm

import euler
import leapfrog
import icc
import display

M_solar = 1.98e30
AU = 1.5e11
yr = 3.15569e7

total_time = 10000 * yr
dt = 10 * yr
dt_output = 100 * yr

bodies = icc.plummer(100, 1.0e14)
bodies.m *= M_solar

body_history = np.zeros((total_time / dt_output + 1, bodies.r.shape[0], bodies.r.shape[1]))
body_history[0, :, :] = bodies.r
for i, current_t in enumerate(leapfrog.simulate_step(bodies, dt, G=6.67e-11, dt_output=dt_output)):
    if current_t >= total_time:
        break

    print "{}/{}".format(current_t, total_time)
    
    body_history[i + 1, :, :] = bodies.r

snapshot_renderer = display.SnapshotRenderer(body_history, line_style="", marker_style=".", 
                                             history_length=0, fade=False, verbose=2)
snapshot_renderer.run()
