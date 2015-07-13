import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()
plt.show()

directory_name = "snapshot/"
base_name = "n_body_py.csv."
colors = ['r', 'g', 'b', 'w']
for i in range(999):
    print(i)
    file_name = directory_name + base_name + str(i)
    bodies = np.loadtxt(file_name, delimiter=",", skiprows=1)
    for i, (x, y, z) in enumerate(bodies):
        ax.scatter(x, y, z, s=20, c=colors[i])

    plt.pause(0.1)
    #for body in bodies:
    #    print body
