import numpy as np
import matplotlib.pyplot as plt

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
        temps.append(new_temps)
    
    return temps

def plot_temps(temps):
    for i in range(0, len(temps), 500):
        plt.plot(temps[i], label=f"step {i}")

    plt.title("Heat diffusion over time")
    plt.xlabel("Position")
    plt.ylabel("Temperature")
    plt.show()

def generate_initial_temperatures():
    Nx = 101
    x = np.linspace(0, 1, Nx)

    center = 0.5
    width = 0.1
    initial_temp = np.exp(-((x - center) ** 2) / (2 * width ** 2))

    initial_temp[0] = 0
    initial_temp[-1] = 0

    return initial_temp

def main():
    initial_temp = generate_initial_temperatures()
    alpha = 1.6563/10000 # thermal diffusivity of silver, pure (99.9%)
    deltaX = 0.01
    deltaT = 0.4 * deltaX**2 / alpha
    r = alpha * deltaT / (deltaX ** 2)
    numTimes = 10000 # number of times it's simulated
    temps = solve_heat_1d(initial_temp, r, numTimes)
    plot_temps(temps) # plot and show graph of simulation

if __name__ == "__main__":
    main()