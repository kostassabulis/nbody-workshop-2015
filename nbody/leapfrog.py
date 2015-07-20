# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 21:49:28 2015

@author: eimantas
"""

import numpy as np

def calc_vel_update(positions, mass, G, dt):
    r_ik3 = np.power(np.sum((positions[0] - positions[1])**2), 1.5)
    updates = G * mass * dt * (positions[1] - positions[0]) / r_ik3

    return updates

def simulate_step(bodies, dt, G=1.0, dt_output=None):
    current_t = 0
    current_step = 0
    N_bodies = bodies.r.shape[0]
    if not dt_output:
        dt_output = dt

    for i in range(N_bodies):
        for k in range(N_bodies):
            if k == i:
                continue
            bodies.v[i, :] += 0.5 * calc_vel_update((bodies.r[i, :], bodies.r[k, :]), bodies.m[k], G, dt)

    while True:
        for i in range(N_bodies):
            bodies.r[i, :] += bodies.v[i, :] * dt
        
        for i in range(N_bodies):        
            for k in range(N_bodies):
                if k == i:
                    continue

                bodies.v[i, :] += calc_vel_update((bodies.r[i, :], bodies.r[k, :]), bodies.m[k], G, dt)

        if current_step * dt_output <= current_t:
            current_step += 1
            yield current_t
            
        current_t += dt   
        