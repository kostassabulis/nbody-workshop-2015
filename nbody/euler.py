__author__ = 'Collaboration'

import numpy as np
import os.path

def calc_vel_update(positions, mass, dt):
    r_ik3 = np.power(np.sum((positions[0] - positions[1])**2), 1.5)
    updates = mass * (positions[1] - positions[0]) / r_ik3
    
    return updates
    
def simulate_step(bodies, dt, dt_output=None):
    current_t = 0
    current_step = 0
    n_bodies = bodies.r.shape[0]
    if not dt_output:
        dt_output = dt
        
    while True:
        for i in range(n_bodies):
            bodies.r[i, :] += bodies.v[i, :] * dt
			
        for i in range(n_bodies):
            vel_update = np.array([0.0, 0.0, 0.0])
            for k in range(n_bodies):
                if i == k:
                    continue
                    
                vel_update += calc_vel_update((bodies.r[i, :], bodies.r[k, :]), bodies.m[k], dt)
            
            bodies.v[i, :] += vel_update * dt



        if current_step * dt_output <= current_t:
            current_step += 1
            yield current_t
            
        current_t += dt