# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 21:49:28 2015

@author: eimantas
"""

import numpy as np


G = 6.67384e-11
AU = 149597870700
M_Solar = 1.9891e30
yr = 31556926

N_bodies = 2
L = 0.1*AU
t_f = 5*yr
dt = 0.001*yr
dt_output = 0.01*yr
fileFolderPath = "d:/n_body/"

xs = np.zeros(N_bodies)
ys = np.zeros(N_bodies)
zs = np.zeros(N_bodies)
vs_x = np.zeros(N_bodies)
vs_y = np.zeros(N_bodies)
vs_z = np.zeros(N_bodies)
ms = np.zeros(N_bodies)

'''PRADINES SALYGOS'''
xs[0] = 0
ys[0] = 0
zs[0] = 0
vs_x[0] = 0
vs_y[0] = 0
vs_z[0] = 0
ms[0] = M_Solar

xs[1] = 0.723327*AU
ys[1] = 0
zs[1] = 0
vs_x[1] = 0
vs_y[1] = 35020
vs_z[1] = 0
ms[1] = 4.867e24

t = 0
t_output = 0
n = 0

alpha = 0.01

'''PRADINIS GREICIO POSLINKIS'''
for j in range(N_bodies):
    for k in range(N_bodies):
        if k == j:
            continue
        r_jk32 = 2*np.power(np.power(xs[k]-xs[j],2) + np.power(ys[k]-ys[j],2) + np.power(zs[k]-zs[j],2),1.5)
        vs_x[j] += G*ms[k] * dt * (xs[k] - xs[j])/r_jk32
        vs_y[j] += G*ms[k] * dt * (ys[k] - ys[j])/r_jk32
        vs_z[j] += G*ms[k] * dt * (zs[k] - zs[j])/r_jk32

while (t < t_f):
    for j in range(N_bodies):
        xs[j] += vs_x[j] * dt
        ys[j] += vs_y[j] * dt
        zs[j] += vs_z[j] * dt
    
    for j in range(N_bodies):        
        for k in range(N_bodies):
            if k == j:
                continue
            r_jk32 = np.power(np.power(xs[k]-xs[j],2) + np.power(ys[k]-ys[j],2) + np.power(zs[k]-zs[j],2),1.5)
            vs_x[j] += G*ms[k] * dt * (xs[k] - xs[j])/r_jk32
            vs_y[j] += G*ms[k] * dt * (ys[k] - ys[j])/r_jk32
            vs_z[j] += G*ms[k] * dt * (zs[k] - zs[j])/r_jk32
    t += dt
    if (t >= t_output):
        f = open(fileFolderPath + "n_body_py.csv." + str(n), 'w')
        f.write("x,y,z\n")
        for k in range(N_bodies):
            f.write("%e,%e,%e\n" % (xs[k], ys[k], zs[k]))
        f.close()
        t_output += dt_output
        n += 1

print "Program finished successfuly!"      
        