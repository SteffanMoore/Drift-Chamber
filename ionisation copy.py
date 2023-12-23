import math
import numpy as np
import matplotlib.pyplot as plt
from ray_generation import Generate_muon


def main():
    pass

x_length, y_length, z_length = 0.5, 1, 0.3
grid_spacing = 0.001
x_cells, z_cells = round(x_length/grid_spacing), round(z_length/grid_spacing)


def next_z_line(z_1, z_2):
    """
    Accepts two previous z positions and returns the z position of the next z grid line intersection, using the previous
    positions to check positive or negative line gradient.
    """

    order_of_spacing = 10**math.floor(math.log10(grid_spacing))
    if z_1 < z_2:
        next_z = int(z_1/order_of_spacing) * order_of_spacing + grid_spacing
    elif z_1 > z_2:
        next_z = int(z_1 / order_of_spacing) * order_of_spacing - grid_spacing

    return next_z
        

def x_position(z_position, z_centre, x_centre, azimuth, zenith):
    """
    Returns the x position of the ray path given the z position and starting conditions.
    """

    x_pos = (z_centre - z_position) * np.sin(azimuth) * np.tan(zenith) + x_centre

    return x_pos


def grid_intersections(muon):
    """
    Finds the coordinates where the ray path crosses the grid lines.
    Given a generated ray, returns the an x list and a z list of ray path intersections 
    """

    x_centre, z_centre, azimuth, zenith = muon[2][0], muon[2][2], muon[1], muon[0]
    x_list, z_list = [], []

    # Iterates through points on the x grid
    for i in range(x_cells + 1):
        x = i * grid_spacing
        z = z_centre - ((x - x_centre) / (np.sin(azimuth) * np.tan(zenith)))

        # Moves to next iteration if not within z boundary
        if z < 0 or z > z_length:
            continue

        x_list.append(x), z_list.append(z)

        # After an x gridline intersection, all z gridline intersections before the next x intersection are added
        while len(x_list) > 1:

            z_line = next_z_line(z_list[-2], z_list[-1])
            x_of_line_intersect = x_position(z_line, z_centre, x_centre, azimuth, zenith)

            # Z gridline intersections are added until the next z intersection exceeds the next x intersection
            if x_position(z_list[-1], z_centre, x_centre, azimuth, zenith) > x_of_line_intersect:
                z_list.insert(-1, z_line), x_list.insert(-1, x_of_line_intersect)
            else:
                break

    return x_list, z_list


def hypotenuse(x, z):
    """
    Returns the distance between two points given the x and z displacement between them.
    """

    hyp = np.sqrt((x)**2 + (z)**2)
    
    return hyp


def electrons_emitted(muon):
    """
    Finds how many electrons are emitted between each grid intersection
    """

    x_list, z_list = grid_intersections(muon)
    x_total, z_total = x_list[0] - x_list[len(x_list) - 1], z_list[0] - z_list[len(z_list) - 1]
    azimuth = muon[1]
    
    projected_length = hypotenuse(x_total, z_total)                              #track length in x-z plane
    real_length = hypotenuse((x_total/np.tan(azimuth)), projected_length)       #track length in 3D
    increase_factor = real_length/projected_length
    charge_distribution = np.zeros((z_cells, x_cells))                       #creates 2D matrix for charge values
    
    for i in range(len(x_list) - 1):
        length = hypotenuse(x_list[i] - x_list[i + 1], z_list[i] - z_list[i + 1])*increase_factor
        number_of_electrons = length*94/0.01            #number of electrons between each point
       
        midpoint_x = (x_list[i + 1]  - x_list[i])/2 + x_list[i]
        midpoint_z = (z_list[i + 1]  - z_list[i])/2 + z_list[i]
        x_gridline = int(math.floor(midpoint_x/grid_spacing))
        z_gridline = int(math.floor(midpoint_z/grid_spacing))
        charge_distribution[z_gridline][x_gridline] = number_of_electrons*1.602E-19
        
    return charge_distribution


plt.imshow(electrons_emitted(Generate_muon(x_length, y_length, z_length)))
plt.show()

if __name__ == "__main__":
    main()