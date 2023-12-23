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
    intersection_list = []

    # Iterates through points on the x grid
    for i in range(x_cells + 1):
        x = i * grid_spacing
        z = z_centre - ((x - x_centre) / (np.sin(azimuth) * np.tan(zenith)))

        # Moves to next iteration if not within z boundary
        if z < 0 or z > z_length:
            continue

        intersection_list.append((x, z))

        # After an x gridline intersection, all z gridline intersections before the next x intersection are added
        while len(intersection_list) > 1:

            z_line = next_z_line(intersection_list[-2][1], intersection_list[-1][1])
            x_of_line_intersect = x_position(z_line, z_centre, x_centre, azimuth, zenith)

            # Z gridline intersections are added until the next z intersection exceeds the next x intersection
            if x_position(intersection_list[-1][1], z_centre, x_centre, azimuth, zenith) > x_of_line_intersect:
                intersection_list.insert(-1, (x_of_line_intersect, z_line))
            else:
                break

    return intersection_list


def hypotenuse(x, z):
    """
    Returns the distance between two points given the x and z displacement between them.
    """

    hyp = np.sqrt((x)**2 + (z)**2)

    return hyp


def electrons_emitted(muon):
    """
    Accepts a generated cosmic ray as an argument and returns a populated charge distribution from the resulting ionisation
    from the ray. From the ray information, path intersections with the grid are found and which allows a calculation of charge
    for each length of path between intersections (in this simulation we assume a constant ionisation rate). This is then mapped
    as a projection of a 3D model onto a 2D array and returned.
    """

    intersections = grid_intersections(muon)
    x_total= intersections[0][0] - intersections[-1][0]
    z_total = intersections[0][1] - intersections[-1][1]
    azimuth = muon[1]
    
    # Full 3D length is calculated from the x-z plane projection and used to produce a constant
    projected_length = hypotenuse(x_total, z_total)
    real_length = hypotenuse((x_total / np.tan(azimuth)), projected_length)
    increase_factor = real_length / projected_length

    # Creates 2D matrix for charge values
    charge_distribution = np.zeros((z_cells, x_cells))

    # Iterates through intersections to find the charge to be attributed along the paths between
    for i, coordinates in enumerate(intersections[:-1]):
        length = hypotenuse(coordinates[0] - intersections[i + 1][0], coordinates[1] - intersections[i + 1][1]) * increase_factor
        electron_number = length * 94 / 0.01    # 94 electrons per cm was provided as an assumption for this problem

        midpoint_x = ((intersections[i + 1][0] - coordinates[0]) / 2) + coordinates[0]
        midpoint_z = ((intersections[i + 1][1] - coordinates[1]) / 2) + coordinates[1]

        x_gridline = int(math.floor(midpoint_x / grid_spacing))
        z_gridline = int(math.floor(midpoint_z / grid_spacing))

        charge_distribution[z_gridline][x_gridline] = electron_number * 1.602E-19
        
    return charge_distribution


plt.imshow(electrons_emitted(Generate_muon(x_length, y_length, z_length)))
plt.show()

if __name__ == "__main__":
    main()