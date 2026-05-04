import numpy as np

def solve_heat_2D(current, r_x, r_y, boundary):
    u_new = current.copy()
    # update the temperature at each position
    u_new[1:-1, 1:-1] = current[1:-1, 1:-1] + r_x * (
                            current[2:, 1:-1] - 2 * current[1:-1, 1:-1] + current[:-2, 1:-1]
                        ) + r_y * (
                            current[1:-1, 2:] - 2 * current[1:-1, 1:-1] + current[1:-1, :-2]
                        )
    if boundary == "Dirichlet": 
        u_new[0, :] = current[0, :]
        u_new[-1, :] = current[-1, :]
        u_new[:, 0] = current[:, 0]
        u_new[:, -1] = current[:, -1]
    elif boundary == "Neumann":
        u_new[0, :] = current[1, :]
        u_new[-1, :] = current[-2, :]
        u_new[:, 0] = current[:, 1]
        u_new[:, -1] = current[:, -2]
    return u_new

def create_grid_2D(Nx, Ny):
    x = np.linspace(0, 1, int(Nx))
    y = np.linspace(0, 1, int(Ny))
    return x, y

def gaussian_initial_temperatures_2D(Nx, Ny, center_x, center_y, width):
    x, y = create_grid_2D(Nx, Ny)
    X, Y = np.meshgrid(x,y)

    initial_temp = np.exp(-((X-center_x) ** 2 + (Y - center_y) ** 2) / (2 * width ** 2))

    return X, Y, initial_temp


def two_peak_initial_condition_2D(Nx, Ny, center1, width1, height1, center2, width2, height2):
    x, y = create_grid_2D(Nx, Ny)
    X, Y = np.meshgrid(x, y)

    peak1 = height1 * np.exp(-((X - center1[0]) ** 2 + (Y - center1[1]) ** 2) / (2 * width1 ** 2))
    peak2 = height2 * np.exp(-((X - center2[0]) ** 2 + (Y - center2[1]) ** 2) / (2 * width2 ** 2))

    return X, Y, peak1 + peak2

def spike_initial_temperatures_2D(Nx, Ny, x_pos, y_pos, height):
    x, y = create_grid_2D(Nx, Ny)
    X, Y = np.meshgrid(x, y)

    u = np.zeros_like(X)
    i = np.argmin(np.abs(x - x_pos))
    j = np.argmin(np.abs(y - y_pos))
    u[j, i] = height

    return X, Y, u
