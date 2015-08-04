"""Leapfrog integrator"""

import numpy as np

def calculate_dt(v, delta_v, N_bodies, alpha):
    a_max = 0.
    for i in range(N_bodies):
        a = np.sum(delta_v[i,:]**2)
        if a > a_max:
            a_max = a
            a_max_index = i
            
    v_mag = np.sqrt(np.sum(v[a_max_index,:]**2))
    return alpha*v_mag/np.sqrt(a_max)

def simulate_step(bodies, dt_min, G, epsilon, dt_output, alpha):
    current_t = 0
    current_step = 0
    n_bodies = bodies.r.shape[0]
    delta_v = np.zeros_like(bodies.v)
    for i in range(n_bodies):
        coord_diff = bodies.r - bodies.r[i, :]
        r_ik3 = (np.sum(coord_diff**2, axis=1) + epsilon**2)**1.5
        delta_v[i,:] = G*np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)
        
    dt = max(calculate_dt(bodies.v, delta_v, n_bodies, alpha), dt_min)
    bodies.v += 0.5 * dt * delta_v

    while True:
        bodies.r += dt * bodies.v      
        for i in range(n_bodies):        
            coord_diff = bodies.r - bodies.r[i, :]
            r_ik3 = (np.sum(coord_diff**2, axis=1) + epsilon**2)**1.5
            delta_v[i,:] = G*np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)
        
        dt = max(calculate_dt(bodies.v, delta_v, n_bodies, alpha), dt_min)
        bodies.v += dt * delta_v
        if current_step * dt_output <= current_t:
            bodies.t[current_step] = current_t
            current_step += 1
            yield current_t
            
        current_t += dt   
        