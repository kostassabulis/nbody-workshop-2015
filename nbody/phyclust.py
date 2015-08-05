"""
__author__ = 'Tomas'


"""

from bodies import Bodies
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import constants


def center_of_mass(cordinates, mass):
    all_mass = np.sum(mass)
    x = np.sum(cordinates[:, 0] * mass) / all_mass
    y = np.sum(cordinates[:, 1] * mass) / all_mass
    z = np.sum(cordinates[:, 2] * mass) / all_mass
    center = (x, y, z)
    return center


def center_of_mass_plot(data, out_file=None, show=True, retrieve=False, color='k'):
    nbody = Bodies()
    nbody.copy(data)
    centers_of_mass = np.zeros((nbody.m.shape[0], 3))
    for i in range(nbody.m.shape[0]):
        centers_of_mass[i] = center_of_mass(nbody.r[i], nbody.m[i])

    print centers_of_mass[:].shape
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(centers_of_mass[:, 0], centers_of_mass[:, 1], zs=centers_of_mass[:, 2], c=color, depthshade=False)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return center_of_mass


def distance_plot(data, out_file=None, show=True, retrieve=False, color='k'):
    nbody = Bodies()
    nbody.copy(data)
    mean_distance = np.zeros(nbody.m.shape[0])
    for i in range(nbody.m.shape[0]):
        center = center_of_mass(nbody.r[i], nbody.m[i])
        mean_distance[i] = np.mean(np.sqrt(np.sum((nbody.r[i, :, :] - center) ** 2, axis=1)), axis=0)

    plt.plot(nbody.t, mean_distance, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Mean distance, m')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return mean_distance


def distance_center_off_plot(data, out_file=None, show=True, retrieve=False, color='k'):
    nbody = Bodies()
    nbody.copy(data)
    mean_distance = np.zeros(nbody.m.shape[0])
    for i in range(nbody.m.shape[0]):
        mean_distance[i] = np.mean(np.sqrt(np.sum(nbody.r[i, :, :] ** 2, axis=1)), axis=0)

    plt.plot(nbody.t, mean_distance, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Mean distance, m')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return mean_distance


def half_mass_radius_plot(data, out_file=None, show=True, retrieve=False, color='k'):
    nbody = Bodies()
    nbody.copy(data)
    half_mass_radius = np.zeros(nbody.m.shape[0])
    distances = np.zeros(nbody.m.shape)
    for i in range(nbody.m.shape[0]):
        total_mass = np.sum(nbody.m[i])
        center = center_of_mass(nbody.r[i], nbody.m[i])
        distances[i] = np.sqrt(np.sum((nbody.r[i, :, :] - center) ** 2, axis=1))
        # Turiu zvaigzdziu atstumus iki centro
        link_sort = np.asarray(sorted(zip(distances[i], nbody.m[i])))
        distances[i] = [point[0] for point in link_sort]
        nbody.m[i] = [point[1] for point in link_sort]
        confined_mass = 0
        j = 0
        while confined_mass <= total_mass * 0.5:
            confined_mass += nbody.m[i, j]
            j += 1
        half_mass_radius[i] = distances[i, j]

    plt.plot(nbody.t, half_mass_radius, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Half mass radius, m')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return half_mass_radius


def half_mass_radius_center_off_plot(data, out_file=None, show=True, retrieve=False, color='k'):
    nbody = Bodies()
    nbody.copy(data)
    half_mass_radius = np.zeros(nbody.m.shape[0])
    distances = np.zeros(nbody.m.shape)
    for i in range(nbody.m.shape[0]):
        total_mass = np.sum(nbody.m[i])
        distances[i] = np.sqrt(np.sum(nbody.r[i, :, :] ** 2, axis=1))
        # Turiu zvaigzdziu atstumus iki centro
        link_sort = np.asarray(sorted(zip(distances[i], nbody.m[i])))
        distances[i] = [point[0] for point in link_sort]
        nbody.m[i] = [point[1] for point in link_sort]
        confined_mass = 0
        j = 0
        while confined_mass <= total_mass * 0.5:
            confined_mass += nbody.m[i, j]
            j += 1
        half_mass_radius[i] = distances[i, j]

    plt.plot(nbody.t, half_mass_radius, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Half mass radius, m')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return half_mass_radius


def kinetic_energy_plot(data, out_file=None, show=True, retrieve=False, color='r'):
    nbody = Bodies()
    nbody.copy(data)
    all_kinetic_energy = np.zeros(nbody.m.shape[0])
    for i in range(nbody.m.shape[0]):
        all_kinetic_energy[i] = np.sum(np.sum(nbody.v[i] ** 2, axis=1) * nbody.m[i] / 2.)

    plt.plot(nbody.t, all_kinetic_energy, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Kinetic energy')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return all_kinetic_energy


def potential_energy_plot(data, out_file=None, show=True, retrieve=False, color='b'):
    nbody = Bodies()
    nbody.copy(data)
    all_potential_energy = np.zeros(nbody.m.shape[0])
    potential_energy = np.zeros(nbody.m.shape[1])
    distances = np.zeros(nbody.m.shape)
    for i in range(nbody.m.shape[0]):
        center = center_of_mass(nbody.r[i], nbody.m[i])
        distances[i] = np.sqrt(np.sum((nbody.r[i] - center) ** 2, axis=1))
        # Turiu zvaigzdziu atstumus iki centro
        link_sort = np.asarray(sorted(zip(distances[i], nbody.m[i])))
        distances[i] = [point[0] for point in link_sort]
        nbody.m[i] = [point[1] for point in link_sort]
        confined_mass = 0
        for j in range(nbody.m.shape[1]):
            potential_energy[j] = -constants.G * confined_mass * nbody.m[i, j] / distances[i, j]
            confined_mass += nbody.m[i, j]
        all_potential_energy[i] = np.sum(potential_energy)

    plt.plot(nbody.t, all_potential_energy, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Potential energy')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return all_potential_energy


def potential_energy_center_off_plot(data, out_file=None, show=True, retrieve=False, color='b'):
    nbody = Bodies()
    nbody.copy(data)
    all_potential_energy = np.zeros(nbody.m.shape[0])
    potential_energy = np.zeros(nbody.m.shape[1])
    distances = np.zeros(nbody.m.shape)
    for i in range(nbody.m.shape[0]):
        distances[i] = np.sqrt(np.sum(nbody.r[i, :, :] ** 2, axis=1))
        # Turiu zvaigzdziu atstumus iki centro
        link_sort = np.asarray(sorted(zip(distances[i], nbody.m[i])))
        distances[i] = [point[0] for point in link_sort]
        nbody.m[i] = [point[1] for point in link_sort]
        confined_mass = 0
        for j in range(nbody.m.shape[1]):
            potential_energy[j] = -constants.G * confined_mass * nbody.m[i, j] / distances[i, j]
            confined_mass += nbody.m[i, j]
        all_potential_energy[i] = np.sum(potential_energy)

    plt.plot(nbody.t, all_potential_energy, color=color)
    plt.xlabel('Time')
    plt.ylabel('Potential energy')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return all_potential_energy


def potential_energy_plot_other(data, out_file=None, show=True, retrieve=False, color='b'):
    nbody = Bodies()
    nbody.copy(data)
    all_potential_energy = np.zeros(nbody.m.shape[0])
    for i in range(0, nbody.m.shape[0], 50):
        # print i
        for j in range(nbody.m.shape[1]):
            for k in range(j):
                distance = np.sqrt(np.sum(np.power(nbody.r[i, j, :] - nbody.r[i, k, :], 2)))
                all_potential_energy[i] -= constants.G * nbody.m[i, j] * nbody.m[i, k] / distance

    plt.plot(nbody.t, all_potential_energy, color=color)
    plt.xlabel('Time, s')
    plt.ylabel('Potential energy')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return all_potential_energy


def total_energy_plot(data, out_file=None, show=True, color='0.5'):
    nbody = Bodies()
    nbody.copy(data)
    all_kinetic_energy = kinetic_energy_plot(data, out_file=None, show=False, retrieve=True)
    all_potential_energy = potential_energy_plot(data, out_file=None, show=False, retrieve=True)
    plt.plot(nbody.t, all_kinetic_energy + all_potential_energy, color=color)
    # plt.plot(range(data.m.shape[0]), all_kinetic_energy / all_potential_energy, color='k')
    plt.ylabel('Energy')
    plt.xlim((0, nbody.t[-1]))
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()


if __name__ == "__main__":
    bodies = Bodies()
    bodies.from_pickle(np.load("dist0.333_N500_T500_E1e+11_d1e+14.pkl"))
    bodies.t = np.load('dist0.333_N500_T500_E1e+11_d1e+14_time.npy')


    # galima pasidaryti kaukes, kad pvz tam paciam plote paziureti skirtigu masiu grupiu zvaigzdziu atstumus iki centro
    # mask = [bodies.m[0, :] > 3*constants.SOLAR_MASS]
    #print bodies.m[0, 0], bodies.m[0, 1]

    #center_of_mass_plot(bodies)
    #distance_center_off_plot(bodies, color='r', show=False)
    #distance_plot(bodies)
    #half_mass_radius_center_off_plot(bodies, color='r', show=False)
    #half_mass_radius_plot(bodies)
    #kinetic_energy_plot(bodies)
    #potential_energy_center_off_plot(bodies, color='r', show=False)
    #potential_energy_plot(bodies)
    #total_energy_plot(bodies)
