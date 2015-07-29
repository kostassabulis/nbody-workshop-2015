"""Test to check if Python can compute on GPU"""

import numpy as np
import gnumpy as gpu
import time

n = 4096

A = np.random.uniform(0, 1, (n, n))
B = np.random.uniform(0, 1, (n, n))

gA = gpu.garray(A)
gB = gpu.garray(B)

gpu_time_0 = time.time()
gA_dot_gB = gpu.dot(gA, gB)
gpu_time_1 = time.time()
print 'gnumpy took: ', gpu_time_1 - gpu_time_0, 's'

cpu_time_0 = time.time()
A_dot_B = np.dot(A, B)
cpu_time_1 = time.time()
print 'numpy took: ', cpu_time_1 - cpu_time_0, 's'

gpu.status()
