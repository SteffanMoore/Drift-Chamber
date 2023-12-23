def M_matrix(tau, z_cells, x_cells):            #generates the M matrix
    D, mu, E, h = 0.1, 50, 10**5, grid_spacing
    alpha, beta, M_dimension = (D*tau)/(h**2), (tau*E)/(2*mu*h), z_cells*x_cells   #n_i and n_j are number of cells
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


print(M_matrix(0.1, 4, 4).toarray())


time_limit, timestep = 1E-4, 1E-7

sparse_M_matrix = M_matrix(timestep, z_cells, x_cells)
solve_M = linalg.factorized(sparse_M_matrix)   #this has been taken out of solve_matrix() to save time when looping

def solve_matrix(M_matrix, q_matrix):   #Performs the LU decomposition
    solved = solve_M(q_matrix)
    return solved

def charge_diffuse_solve(initial_charge, sparse_M_matrix):    #Finds the charge of the next time step
    flattened_charge, M = initial_charge.flatten(), sparse_M_matrix
    solved_charge = solve_matrix(M, flattened_charge)
    reshaped = solved_charge.reshape(z_cells, x_cells)
    return reshaped

def drift_chamber(initial_charge): #Takes initial charge and runs diffusion/drifting until desired time 
    array_list = []
    array_list.append(initial_charge)
    for i in range(int(time_limit/timestep)):
        next_charge = charge_diffuse_solve(initial_charge, solve_M)
        initial_charge = next_charge
        array_list.append(next_charge)
    return array_list


def  point_charge():            #creates an array with only one charged cell
    point_matrix = np.zeros((z_cells, x_cells))
    point_matrix[int(z_cells/2)][int(x_cells/2)] = 100*1.602E-19
    return point_matrix
    
plt.imshow(drift_chamber(point_charge())[int(time_limit/timestep)])