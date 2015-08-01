"""
__author__ = 'Tomas'


"""

from bodies import Bodies
import numpy as np
import matplotlib.pyplot as plt
import constants


def distance_plot(bodies, out_file=None, show=True, retrieve=False, color='k'):
    mean_distance = np.zeros(bodies.m.shape[0])
    for i in range(bodies.m.shape[0]):
        mean_distance[i] = np.mean(np.sqrt(np.sum(bodies.r[i, :, :]**2, axis=1)), axis=0)

    plt.plot(range(bodies.m.shape[0]), mean_distance, color=color)
    plt.xlabel('Time') #Turi buti
    plt.ylabel('Mean distance, m')
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return mean_distance

def half_mass_radius_plot(bodies, out_file=None, show=True, retrieve=False, color='k'):
    half_mass_radius = np.zeros(bodies.m.shape[0])
    distances = np.zeros(bodies.m.shape)
    for i in range(bodies.m.shape[0]):
        total_mass = np.sum(bodies.m[i])
        distances[i] = np.sqrt(np.sum(bodies.r[i, :, :]**2, axis=1))
        #Turiu zvaigzdziu atstumus iki centro
        link_sort = np.asarray(sorted(zip(distances[i], bodies.m[i])))
        distances[i] = [point[0] for point in link_sort]
        bodies.m[i] = [point[1] for point in link_sort]
        confined_mass = 0
        j = 0
        while confined_mass < total_mass * 0.5:
            confined_mass += bodies.m[i, j]
            j += 1
        half_mass_radius[i] = distances[i, j]

    plt.plot(range(bodies.m.shape[0]), half_mass_radius, color=color)
    plt.xlabel('Time') #Turi buti
    plt.ylabel('Half mass radius, m')
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return half_mass_radius

def kinetic_energy_plot(bodies, out_file=None, show=True, retrieve=False, color='r'):
    all_kinetic_energy = np.zeros(bodies.m.shape[0])
    for i in range(bodies.m.shape[0]):
        all_kinetic_energy[i] = np.sum(np.sqrt(np.sum(bodies.v[i, :, :]**2, axis=1)) * bodies.m[i] / 2.)

    plt.plot(range(bodies.m.shape[0]), all_kinetic_energy, color=color)
    plt.xlabel('Time') #Turetu buti
    plt.ylabel('Kinetic energy')
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return all_kinetic_energy


def potential_energy_plot(bodies, out_file=None, show=True, retrieve=False, color='b'):
    all_potential_energy = np.zeros(bodies.m.shape[0])
    potential_energy = np.zeros(bodies.m.shape[1])
    distances = np.zeros(bodies.m.shape)
    for i in range(bodies.m.shape[0]):
        distances[i] = np.sqrt(np.sum(bodies.r[i, :, :]**2, axis=1))
        #Turiu zvaigzdziu atstumus iki centro
        link_sort = np.asarray(sorted(zip(distances[i], bodies.m[i])))
        distances[i] = [point[0] for point in link_sort]
        bodies.m[i] = [point[1] for point in link_sort]
        confined_mass = 0
        for j in range(bodies.m.shape[1]):
            potential_energy[j] = -constants.G * confined_mass * bodies.m[i, j] / distances[i, j]
            confined_mass += bodies.m[i, j]
        all_potential_energy[i] = np.sum(potential_energy)

    plt.plot(range(bodies.m.shape[0]), all_potential_energy, color=color)
    plt.xlabel('Time') #Turetu buti
    plt.ylabel('Potential energy')
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()
    if retrieve is True:
        return all_potential_energy

def total_energy_plot(bodies, out_file=None, show=True, color='0.5'):
    mean_kinetic_energy = kinetic_energy_plot(bodies, out_file=None, show=False, retrieve=True)
    mean_potential_energy = potential_energy_plot(bodies, out_file=None, show=False, retrieve=True)

    plt.plot(range(bodies.m.shape[0]), mean_kinetic_energy + mean_potential_energy, color=color)
    plt.ylabel('Energy')
    if out_file is not None:
        plt.savefig(out_file)
    if show is True:
        plt.show()


if __name__ == "__main__":
    bodies = Bodies()
    bodies.from_pickle(np.load("snapshot.pkl"))

    #galima pasidaryti kaukes, kad pvz tam paciam plote paziureti skirtigu masiu grupiu zvaigzdziu atstumus iki centro
    #mask = [bodies.m[0, :] > 3*constants.SOLAR_MASS]
    #print bodies.m[0, 0], bodies.m[0, 1]

    #distance_plot(bodies)
    #half_mass_radius_plot(bodies)
    #kinetic_energy_plot(bodies)
    #potential_energy_plot(bodies)
    total_energy_plot(bodies)