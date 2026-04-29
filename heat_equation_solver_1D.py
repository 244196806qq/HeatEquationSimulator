import numpy as np



# # batch solver
# def solve_heat_1D(initial_temp, r, numTimes):
#     temps = [
#         np.array(initial_temp, dtype = float) # store initial as np array
#         ]
#     # simulate for n times
#     for _ in range(numTimes):
#         current_state = temps[-1] # the current temperature values 
#         u_new = current_state.copy()

#         # update the temperature at each position
#         u_new[1:-1] = current_state[1:-1] + r * (
#             current_state[2:] - 2 * current_state[1:-1] + current_state[:-2]
#         ) 

#         # keep boundaries the same temperature
#         u_new[0] = current_state[0]
#         u_new[-1] = current_state[-1]

#         # Add the new set of temperature into temps
#         temps.append(u_new)

#     return temps

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


# initial condition function generator 
def gaussian_initial_temperatures_1D(Nx, center = 0.5, width = 0.1):
    x = np.linspace(0, 1, int(Nx))
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
