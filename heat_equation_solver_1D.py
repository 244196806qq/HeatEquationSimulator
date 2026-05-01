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

def file_initial_temperature_1D(filepath):
    data = np.genfromtxt(
        filepath,
        delimiter = ",",
        names = True
    )
    
    required = {"x", "temp"}
    if not required.issubset(data.dtype.names):
        raise ValueError("CSV file must contain 'x' and 'temp' columns.")
    
    x = data["x"]
    initial_temp = data["temp"]
    return x, initial_temp

def create_grid_1D(Nx):
    x = np.linspace(0, 1, int(Nx))
    return x

# initial condition function generator 
def gaussian_initial_temperatures_1D(Nx, center = 0.5, width = 0.1):
    x = create_grid_1D(Nx)
    initial_temp = np.exp(-((x - center) ** 2) / (2 * width ** 2))
    return x, initial_temp


def two_peak_initial_condition_1D(Nx, center1 = 0.5, width1 = 0.1, center2 = 0.5, width2 = 0.1, height1 = 1.0, height2 = 1.0):
    x = np.linspace(0, 1, int(Nx))
    peak1 = height1 * np.exp(-((x - center1) ** 2) / (2 * width1 ** 2))
    peak2 = height2 * np.exp(-((x - center2) ** 2) / (2 * width2 ** 2))
    initial_temp = peak1 + peak2
    return x, initial_temp


def spikes_initial_temperatures_1D(Nx, position=0.5, height=1.0):
    x = np.linspace(0, 1, int(Nx))
    initial_temp = np.zeros_like(x)
    spike_index = np.argmin(np.abs(x - position))
    initial_temp[spike_index] = height
    return x, initial_temp
