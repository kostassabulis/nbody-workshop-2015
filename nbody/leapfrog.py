"""Leapfrog integrator"""

import numpy as np

def simulate_step(bodies, dt, epsilon, dt_output=None):
    current_t = 0
    current_step = 0
    n_bodies = bodies.r.shape[0]
    if not dt_output:
        dt_output = dt

    for i in range(n_bodies):
        coord_diff = bodies.r - bodies.r[i, :]
        r_ik3 = (np.sum(coord_diff**2, axis=1) + epsilon**2)**1.5 #+ 1e-16
        bodies.v[i, :] += 0.5 * dt * np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)

    while True:
        bodies.r += dt * bodies.v
        
        for i in range(n_bodies):        
            coord_diff = bodies.r - bodies.r[i, :]
            r_ik3 = (np.sum(coord_diff**2, axis=1) + epsilon**2)**1.5 #+ 1e-16
            bodies.v[i, :] += dt * np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)

        if current_step * dt_output <= current_t:
            current_step += 1
            yield current_t
            
        current_t += dt   
        