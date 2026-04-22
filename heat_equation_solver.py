import numpy as np



# solver
def solve_heat_1d(initial_temp, r, numTimes):
    temps = [
        initial_temp
        ]
    # simulate for n times
    for time_steps in range(numTimes):
        current_state = temps[time_steps] # the current temperature values 
        new_temps = [] # placeholder for the new temp at each position
        #calculate the temp at each position after each time interval
        for space_index in range(len(current_state)):
            if (space_index == 0 or space_index == len(current_state) - 1):
                new_temps.append(current_state[space_index])
            else: 
                current = current_state[space_index]
                right = current_state[space_index + 1]
                left = current_state[space_index - 1]
                # compute u^{n+1} from u^n using the explicit finite-difference heat update
                newTemp = current + r * (right - 2 * current + left) 
                new_temps.append(newTemp)
        temps.append(np.array(new_temps))
    
    return temps



# initial condition function generator 
def gaussian_initial_temperatures(Nx = 101, center = 0.5, width = 0.1):
    x = np.linspace(0, 1, int(Nx))
    initial_temp = np.exp(-((x - center) ** 2) / (2 * width ** 2))
    initial_temp[0] = 0
    initial_temp[-1] = 0
    return x, initial_temp


def two_peak_initial_conidtion(Nx = 101, center = 0.5, width = 0.1, height = 1.0):
    x = np.linspace(0, 1, int(Nx))
    peak1 = height * np.exp(-((x - center) ** 2) / (2 * width ** 2))
    peak2 = np.random.rand() * height * np.exp(-((x - (np.random.rand() * center)) ** 2) / (2 * (np.random.rand() * width) ** 2))
    initial_temp = peak1 + peak2
    initial_temp[0] = 0
    initial_temp[-1] = 0
    return x, initial_temp

def spikes_initial_temperatures(Nx = 101, center = 0.5, width = 0.1):
    x = np.linspace(0, 1, int(Nx))
    initial_temp = np.random.rand(Nx)
    initial_temp[0] = 0
    initial_temp[-1] = 0
    return x, initial_temp
