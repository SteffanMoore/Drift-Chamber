from scipy import sparse
from scipy.sparse import linalg
import numpy as np
import matplotlib.pyplot as plt

def main():
    plot_point_charge()


def M_matrix(tau, z_cells, x_cells, grid_spacing):
    """
    The charge from the ionisation both drifts towards the anode wires and diffuses into the gas - this can be reprensented by
    a single matrix acting on a vector: q(n) = M * q(n+1). This M matrix is a largely empty matrix (being a diagonal matrix with
    a few offset diagonals). Due to this, it is useful to represent it as a sparse matrix to improve performance.
    """

    D, mu, E, h = 0.1, 50, 10**5, grid_spacing
    alpha, beta, M_dimension = (D * tau) / (h**2), (tau * E) / (2 * mu * h), z_cells * x_cells   #n_i and n_j are number of cells
    diag_centre, diag_alpha_beta, diag_alpha, diagonals = [], [], [], []  #creates lists for diagonal matrices
    
    for i in range(M_dimension):
        diag_centre.append(1 + 4*alpha + beta)
        diag_alpha_beta.append(-alpha - beta)
        diag_alpha.append(-alpha)
            
    diagonals.append(diag_centre), diagonals.append(diag_alpha_beta)
    for i in range(3):
        diagonals.append(diag_alpha)
        
    sparse_matrix = sparse.diags(diagonals, [0, -1, 1, x_cells, -x_cells], format = "csc")
    return sparse_matrix


def solve_matrix(LU_decomp, q_matrix):
    """
    Using the LU decomposition of the sparse M matrix, the charge matrix is solved using the LU factors
    """

    solved = LU_decomp(q_matrix)

    return solved


def charge_diffuse_solve(initial_charge, LU_decomp, z_cells, x_cells):
    """
    Finds the charge distribution for the next time step using the initial charge distribution
    """

    flattened_charge = initial_charge.flatten()
    solved_charge = solve_matrix(LU_decomp, flattened_charge)
    reshaped = solved_charge.reshape(z_cells, x_cells)

    return reshaped


def drift_chamber(initial_charge, time_limit, timestep, LU_decomp, z_cells, x_cells): #Takes initial charge and runs diffusion/drifting until desired time
    """
    Takes an initial charge and runs drift-diffusion on it in the specified time-frame
    """

    array_list = []
    array_list.append(initial_charge)

    for i in range(int(time_limit / timestep)):
        next_charge = charge_diffuse_solve(initial_charge, LU_decomp, z_cells, x_cells)
        initial_charge = next_charge
        array_list.append(next_charge)

    return array_list


def  point_charge(z_cells, x_cells):
    """
    Returns a charge array with a single highly charged cell to represent a point charge
    """

    point_matrix = np.zeros((z_cells, x_cells))
    point_matrix[int(z_cells/2)][int(x_cells/2)] = 100 * 1.602E-19    # Charge of 100 electrons

    return point_matrix


def simulate_chamber(charge_distribution, detector_length, grid_spacing, times):

    x_cells, z_cells = round(detector_length[0] / grid_spacing), round(detector_length[2] / grid_spacing)
    time_limit, timestep = times[0], times[1]

    sparse_M_matrix = M_matrix(timestep, z_cells, x_cells, grid_spacing)

    # Performs LU decomposition of matrix
    M_LU_decomp = linalg.factorized(sparse_M_matrix)
    chamber_simulation = drift_chamber(charge_distribution, time_limit, timestep, M_LU_decomp, z_cells, x_cells)

    return chamber_simulation


def plot_point_charge():

    detector_length = (0.5, 1, 0.3)
    grid_spacing = 0.001
    x_cells, z_cells = round(detector_length[0] / grid_spacing), round(detector_length[2] / grid_spacing)
    time_limit, timestep = 1E-4, 1E-7

    simulation = simulate_chamber(point_charge(z_cells, x_cells), (detector_length[0], detector_length[1], detector_length[2]), grid_spacing, (time_limit, timestep))
    plt.imshow(simulation[int(time_limit / timestep)])
    plt.show()


if __name__ =="__main__":
    main()