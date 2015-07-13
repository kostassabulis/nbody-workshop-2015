__author__ = 'Collaboration'

import numpy as np

G = 6.67e-11
M_solar = 1.98e30
AU = 1.5e11
yr = 3.15569e7

XS = [0, 0.387*AU, -0.728*AU, 1*AU]
YS = [0, 0, 0, 0]
ZS = [0, 0, 0, 0]

MS = [M_solar, 3.3e23, 4.86e24, 5.97e24]
N_bodies = len(XS)

VS_x = [0, 0, 0, 0]
VS_y = [0, 47362, -35020, 29780]
VS_z = [0, 0, 0, 0]

n = 0
t = 0
t_f = 10 * yr
dt = 0.001 * yr
dt_output = 0.01 * yr

while t < t_f:
    for i in range(N_bodies):
        g_x = 0
        g_y = 0
        g_z = 0
        for k in range(N_bodies):
            if i == k:
                continue
            r_ik3 = np.power((XS[k]-XS[i])**2 + (YS[k]-YS[i])**2 + (ZS[k]-ZS[i])**2), 1.5)
            g_x += G*MS[k]*(XS[k]-XS[i])/r_ik3
            g_y += G*MS[k]*(YS[k]-YS[i])/r_ik3
            g_z += G*MS[k]*(ZS[k]-ZS[i])/r_ik3
        XS[i] += VS_x[i]*dt
        YS[i] += VS_y[i]*dt
        ZS[i] += VS_z[i]*dt
        VS_x[i] += g_x*dt
        VS_y[i] += g_y*dt
        VS_z[i] += g_z*dt
    if n*dt_output <= t:
        f = open("../snapshot/n_body_py.csv."+str(n), 'w')
        f.write("x,y,z\n")
        for i in range(N_bodies):
            f.write("%e,%e,%e\n" % (XS[i], YS[i], ZS[i]))
        f.close()
        n += 1
    t += dt

