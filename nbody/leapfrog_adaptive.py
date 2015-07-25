"""Leapfrog integrator"""

import numpy as np

def calculate_dt(V, A, N_bodies, alpha):
    a_max = 0.
    for i in range(N_bodies):
        a = np.sum(A[i,:]**2)
        if a > a_max:
            a_max = a
            a_max_index = i
            
    v = np.sqrt(np.sum(V[a_max_index,:]**2))
    return alpha*v/a_max

def simulate_step(bodies, dt_min, G, epsilon, dt_output, alpha):
    current_t = 0
    current_step = 0
    N_bodies = bodies.r.shape[0]
    A = np.zeros_like(bodies.v)
    for i in range(N_bodies):
        coord_diff = bodies.r - bodies.r[i, :]
        r_ik3 = (np.sum(coord_diff**2, axis=1) + epsilon**2)**1.5 #+ 1e-16
        A[i,:] = G*np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)
        
    dt = max(calculate_dt(bodies.v, A, N_bodies, alpha), dt_min)
    bodies.v += 0.5 * dt * A

    while True:
        bodies.r += dt * bodies.v      
        for i in range(N_bodies):        
            coord_diff = bodies.r - bodies.r[i, :]
            r_ik3 = (np.sum(coord_diff**2, axis=1) + epsilon**2)**1.5 #+ 1e-16
            A[i,:] = G*np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)
        
        dt = max(calculate_dt(bodies.v, A, N_bodies, alpha), dt_min)
        bodies.v += dt * A
        if current_step * dt_output <= current_t:
            current_step += 1
            yield current_t
            
        current_t += dt   
        