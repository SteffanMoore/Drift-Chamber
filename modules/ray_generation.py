import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse import linalg
import matplotlib.animation as animate

def main():
    plot_angle_distributions(1000001, (10, 10, 10))


def Zenith_angle():
    """
    Creates a random zenith angle of an incoming cosmic ray with a cos^2 distribution using the accept/reject method
    """

    # Only returns a value once accepted (the distribution random number being higher than a uniform random number)
    while True:
        zenith  = (np.pi)*np.random.random() - (np.pi)/2
        p = np.random.random()
        if p < (np.cos(zenith))**2:
            return zenith


def Azimuth_angle():
    """
    Creates a random azimuth angle of an incoming cosmic ray with a uniform distribution
    """

    azimuth = (2*np.pi)*np.random.random()
    return azimuth


def Starting_position(x_size, y_size, z_size):
    """
    Returns random start position values for the cosmic ray inside the box
    """

    x_start = x_size*np.random.random()
    y_start = y_size*np.random.random()
    z_start = z_size*np.random.random()
    return x_start, y_start, z_start
    

def Generate_muon(x_size, y_size, z_size):
    """
    Benerates a cosmic ray based on the size of the detector box
    """

    return Zenith_angle(), Azimuth_angle(), Starting_position(x_size, y_size, z_size)


def plot_angle_distributions(particle_number, container_size):
    """
    Returns two figures to demonstrate the angle distributions of a number of generated particles
    """

    cosmic_rays = [Generate_muon(container_size[0], container_size[1], container_size[2]) for i in range(particle_number)]
    ray_zeniths = [ray[0] for ray in cosmic_rays]
    ray_azimuths = [ray[1] for ray in cosmic_rays]
        
    # For the zeniths, a cos^2 line is also plotted to compare to the distribution
    x = np.linspace(-np.pi/2, np.pi/2, 1000)
    y = ((np.cos(x))**2)*20000

    # Plots the two distributions
    plt.figure(1)
    plt.hist(ray_zeniths, bins=99)
    plt.plot(x,y)

    plt.figure(2)
    plt.hist(ray_azimuths, bins=99)
    
    plt.show()


if __name__ == "__main__":
    main()