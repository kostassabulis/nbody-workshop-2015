"""Leapfrog integrator"""

import numpy as np


def calculate_dts(v, delta_v, alpha, dt_output, max_dt_bins, n_bodies):
    v_mag = np.sqrt(np.sum(np.power(v, 2), axis=1))
    a_mag = np.sqrt(np.sum(np.power(delta_v, 2), axis=1))
    dts = alpha * v_mag / a_mag
    dts_2 = np.zeros(n_bodies)
    for i in range(n_bodies):
        if dts[i] == 0:
            n = max_dt_bins
        else:
            n = min(int(1 + np.log2(dt_output / dts[i])), max_dt_bins)
        dts_2[i] = dt_output / 2**n
    return dts_2


def simulate_step(bodies, G, epsilon, dt_output, alpha, max_dt_bins):
    current_t = 0
    current_step = 0
    n_bodies = bodies.r.shape[0]
    delta_v = np.zeros_like(bodies.v)
    for i in range(n_bodies):
        coord_diff = bodies.r - bodies.r[i, :]
        r_ik3 = (np.sum(np.power(coord_diff, 2), axis=1) + epsilon ** 2) ** 1.5
        delta_v[i, :] = G * np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)

    dts = calculate_dts(bodies.v, delta_v, alpha, dt_output, max_dt_bins, n_bodies)
    dt_min = np.min(dts)
    times_update = np.ones(n_bodies) * current_t + dts

    for i in range(n_bodies):
        bodies.v[i, :] += 0.5 * dts[i] * delta_v[i, :]

    while True:
        bodies.t = current_t
        bodies.r += bodies.v * dt_min
        current_t += dt_min

        if current_step * dt_output <= current_t:
            current_step += 1
            yield current_t

        for i in range(n_bodies):
            if times_update[i] <= current_t:
                coord_diff = bodies.r - bodies.r[i, :]
                r_ik3 = (np.sum(np.power(coord_diff, 2), axis=1) + epsilon ** 2) ** 1.5
                delta_v[i, :] = G * np.sum(bodies.m[:, np.newaxis] * coord_diff / r_ik3[:, np.newaxis], axis=0)
                bodies.v[i, :] += dts[i] * delta_v[i, :]
                times_update[i] += dts[i]
