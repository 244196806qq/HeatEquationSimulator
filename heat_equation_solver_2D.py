import numpy as np
import matplotlib.pyplot as plt


def solve_heat_2D(initial_temp, r_x, r_y, num_times):
    temps = [np.array(initial_temp, dtype = float)]
    for _ in range(num_times):
        current = temps[-1]
        u_new = current.copy()

        # update the temperature at each position
        u_new[1:-1, 1:-1] = current[1:-1, 1:-1] + r_x * (
                                current[2:, 1:-1] - 2 * current[1:-1, 1:-1] + current[:-2, 1:-1]
                            ) + r_y * (
                                current[1:-1, 2:] - 2 * current[1:-1, 1:-1] + current[1:-1, :-2]
                            )
        u_new[0, :] = current[0, :]
        u_new[-1, :] = current[-1, :]
        u_new[:, 0] = current[:, 0]
        u_new[:, -1] = current[:, -1]

        temps.append(u_new)
    return temps

def gaussian_initial_temperatures_2D(Nx, Ny, center_x, center_y, width):
    x = np.linspace(0, 1, int(Nx))
    y = np.linspace(0, 1, int(Ny))
    X, Y = np.meshgrid(x,y)

    initial_temp = np.exp(
        -((X-center_x) ** 2 + (Y - center_y) ** 2) / (2 * width ** 2)
    )

    return X, Y, initial_temp


def two_peak_initial_condition_2D(
    Nx, Ny,
    center1=(0.3, 0.3), width1=0.08, height1=1.0,
    center2=(0.7, 0.7), width2=0.08, height2=1.0
):
    x = np.linspace(0, 1, int(Nx))
    y = np.linspace(0, 1, int(Ny))
    X, Y = np.meshgrid(x, y)

    peak1 = height1 * np.exp(
        -((X - center1[0]) ** 2 + (Y - center1[1]) ** 2) / (2 * width1 ** 2)
    )
    peak2 = height2 * np.exp(
        -((X - center2[0]) ** 2 + (Y - center2[1]) ** 2) / (2 * width2 ** 2)
    )

    return X, Y, peak1 + peak2

def spike_initial_temperatures_2D(Nx, Ny, x_pos=0.5, y_pos=0.5, height=1.0):
    x = np.linspace(0, 1, int(Nx))
    y = np.linspace(0, 1, int(Ny))
    X, Y = np.meshgrid(x, y)

    u = np.zeros_like(X)
    i = np.argmin(np.abs(x - x_pos))
    j = np.argmin(np.abs(y - y_pos))
    u[j, i] = height
    return X, Y, u

# X, Y, initial_temp = spike_initial_temperatures_2D(80, 80)
# temps = solve_heat_2D(initial_temp, r_x = 0.2, r_y = 0.2, num_times=200)

# plt.imshow(temps[0], origin="lower", cmap="hot", extent=[0, 1, 0, 1])
# plt.colorbar(label="Temperature")
# plt.title("Initial 2D Temperature")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.show()