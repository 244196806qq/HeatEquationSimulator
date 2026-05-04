import numpy as np

# step by step solver
def solve_heat_1D(current_temp, r, boundary):
    u_new = current_temp.copy()
    # update the temperature at each position
    u_new[1:-1] = current_temp[1:-1] + r * (
        current_temp[2:] - 2 * current_temp[1:-1] + current_temp[:-2]
    ) 
    # keep boundaries the same temperature
    if boundary == "Dirichlet":
        u_new[0] = current_temp[0]
        u_new[-1] = current_temp[-1]
    elif boundary == "Neumann":
        u_new[0] = u_new[1]
        u_new[-1] = u_new[-2]
    return u_new

def solve_heat_1D_analytical(x, frame, deltaT, alpha, width, center):
    time = frame * deltaT
    analytical = (width/np.sqrt((width**2) + 2 * alpha * time)) * np.exp(-((x-center)**2)/(2*(width**2 + 2*alpha*time)))
    return analytical

# def file_initial_temperature_1D(filepath):
def file_initial_temperature_1D(filepath):
    # 1. Read first line manually
    with open(filepath, "r") as file:
        header = file.readline().strip().replace(" ", "")

    if header != "x,temp":
        raise ValueError("File must start with header: x,temp")

    # 2. Now parse data rows only
    try:
        data = np.genfromtxt(
            filepath,
            delimiter=",",
            names=True
        )
    except Exception:
        raise ValueError("Data rows must be comma-separated numbers")

    # 3. Handle single-row files
    if data.shape == ():
        raise ValueError("File must contain at least 3 data points")

    x = data["x"]
    initial_temp = data["temp"]

    # 4. Convert single values to arrays if needed
    x = np.atleast_1d(x)
    initial_temp = np.atleast_1d(initial_temp)

    if len(x) < 3:
        raise ValueError("File must contain at least 3 data points")

    if np.isnan(x).any() or np.isnan(initial_temp).any():
        raise ValueError("File contains missing or invalid numbers")
    
    return x, initial_temp

def create_grid_1D(Nx):
    x = np.linspace(0, 1, int(Nx))
    return x

# initial condition function generator 
def gaussian_initial_temperatures_1D(Nx, center, width):
    x = create_grid_1D(Nx)
    initial_temp = np.exp(-((x - center) ** 2) / (2 * width ** 2))
    return x, initial_temp


def two_peak_initial_condition_1D(Nx, center1, width1, center2, width2, height1, height2):
    x = create_grid_1D(Nx)
    peak1 = height1 * np.exp(-((x - center1) ** 2) / (2 * width1 ** 2))
    peak2 = height2 * np.exp(-((x - center2) ** 2) / (2 * width2 ** 2))
    initial_temp = peak1 + peak2
    return x, initial_temp


def spikes_initial_temperatures_1D(Nx, position, height):
    x = create_grid_1D(Nx)
    initial_temp = np.zeros_like(x)
    spike_index = np.argmin(np.abs(x - position))
    initial_temp[spike_index] = height
    return x, initial_temp
