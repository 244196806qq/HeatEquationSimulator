import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from heat_equation_solver_1D import gaussian_initial_temperatures_1D, solve_heat_1D, two_peak_initial_condition_1D, spikes_initial_temperatures_1D
from heat_equation_solver_2D import gaussian_initial_temperatures_2D, solve_heat_2D, two_peak_initial_condition_2D, spike_initial_temperatures_2D
from UI_helper import create_controls

def run_simulation_1D(fig, canvas, initcond, alpha, Nx, numTimes, shape_controls):
    # calculate all the values for the graph
    x, initial_temp = generate_initial_condition_1D(initcond, Nx, shape_controls)
    temps = calculate_parameter_1D(alpha, x, numTimes, initial_temp)

    # create the graph
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)
    line, = ax.plot(x, temps[0])
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, max(max(t) for t in temps) * 1.05)
    ax.set_title("Heat diffusion on a 1D rod")
    ax.set_xlabel("Position")
    ax.set_ylabel("Temperature")

    # add annotates to the graph
    annot = ax.annotate(
        "",
        xy= (0,0),
        xytext = (10, 10),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="w"),
        arrowprops=dict(arrowstyle="->")
    )
    annot.set_visible(False)

    def update_annot(index):
        x_data = line.get_xdata()
        y_data = line.get_ydata()

        x_val = x_data[index]
        y_val = y_data[index]

        annot.xy = (x_val, y_val)
        annot.set_text(f"x = {x_val:.3f}\ny = {y_val:.3f}")
        annot.set_visible(True)
    
    def hover(event):
        if event.inaxes != ax or event.xdata is None:
            annot.set_visible(False)
            canvas.draw_idle()
            return
        
        x_data = line.get_xdata()
        distances = np.abs(x_data - event.xdata)
        nearest_index = np.argmin(distances)
        update_annot(nearest_index)
        canvas.draw_idle()
    
    fig.canvas.mpl_connect("motion_notify_event", hover)

    # update the graph (animation)
    def update(frame = 0):
        # check if the graph is moving
        current_max = max(temps[frame])
        # print(current_max)
        ax.set_title(f"Heat diffusion on a 1D rod (step: {frame})\n (max: {current_max:.6f})")
        if frame >= len(temps):
            return 
        
        line.set_ydata(temps[frame])

        canvas.draw_idle()

        canvas.get_tk_widget().after(20, update, frame + 1)
    
    update()

def run_simulation_2D(fig, canvas, initcond, alpha, Nx, numTimes, shape_controls):
    # calculate all the values for the graph
    x, initial_temp = generate_initial_condition_2D(initcond, Nx, shape_controls)
    temps = calculate_parameter_1D(alpha, x, numTimes, initial_temp)

    # create the graph
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)
    line, = ax.plot(x, temps[0])
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, max(max(t) for t in temps) * 1.05)
    ax.set_title("Heat diffusion on a 1D rod")
    ax.set_xlabel("Position")
    ax.set_ylabel("Temperature")

    # add annotates to the graph
    annot = ax.annotate(
        "",
        xy= (0,0),
        xytext = (10, 10),
        textcoords="offset points",
        bbox=dict(boxstyle="round", fc="w"),
        arrowprops=dict(arrowstyle="->")
    )
    annot.set_visible(False)

    def update_annot(index):
        x_data = line.get_xdata()
        y_data = line.get_ydata()

        x_val = x_data[index]
        y_val = y_data[index]

        annot.xy = (x_val, y_val)
        annot.set_text(f"x = {x_val:.3f}\ny = {y_val:.3f}")
        annot.set_visible(True)
    
    def hover(event):
        if event.inaxes != ax or event.xdata is None:
            annot.set_visible(False)
            canvas.draw_idle()
            return
        
        x_data = line.get_xdata()
        distances = np.abs(x_data - event.xdata)
        nearest_index = np.argmin(distances)
        update_annot(nearest_index)
        canvas.draw_idle()
    
    fig.canvas.mpl_connect("motion_notify_event", hover)

    # update the graph (animation)
    def update(frame = 0):
        # check if the graph is moving
        current_max = max(temps[frame])
        # print(current_max)
        ax.set_title(f"Heat diffusion on a 1D rod (step: {frame})\n (max: {current_max:.6f})")
        if frame >= len(temps):
            return 
        
        line.set_ydata(temps[frame])

        canvas.draw_idle()

        canvas.get_tk_widget().after(20, update, frame + 1)
    
    update()

def generate_initial_condition_1D(initcond, Nx, shape_controls):
    if (initcond == "Gaussian"):
        return gaussian_initial_temperatures_1D(Nx, shape_controls["center_slider"].get(), shape_controls["width_slider"].get())
    elif (initcond == "Spike"):
        return spikes_initial_temperatures_1D(Nx, shape_controls["position_slider"].get(), shape_controls["height_slider"].get())
    elif (initcond == "Two Peaks"):
        return two_peak_initial_condition_1D(
            Nx, 
            shape_controls["center1_slider"].get(), 
            shape_controls["width1_slider"].get(), 
            shape_controls["center2_slider"].get(), 
            shape_controls["width2_slider"].get(), 
            shape_controls["height1_slider"].get(),
            shape_controls["height2_slider"].get())
    else:
        raise ValueError(f"Unknown initial condition: {initcond}")



def calculate_parameter_1D(alpha, x, numTimes, initial_temp):
    deltaX = x[1] - x[0]
    deltaT = 0.001
    r = alpha * deltaT / (deltaX ** 2)
    return solve_heat_1D(initial_temp, r, numTimes)

def generate_initial_condition_2D(initcond, Nx, Ny, shape_controls):
    if (initcond == "Gaussian"):
        return gaussian_initial_temperatures_2D(Nx, Ny, shape_controls["centerX_slider"].get(), shape_controls["centerY_slider"].get(), shape_controls["width_slider"].get())
    elif (initcond == "Spike"):
        return spike_initial_temperatures_2D(Nx, shape_controls["position_slider"].get(), shape_controls["height_slider"].get())
    elif (initcond == "Two Peaks"):
        return two_peak_initial_condition_2D(
            Nx, 
            shape_controls["center1_slider"].get(), 
            shape_controls["width1_slider"].get(), 
            shape_controls["center2_slider"].get(), 
            shape_controls["width2_slider"].get(), 
            shape_controls["height1_slider"].get(),
            shape_controls["height2_slider"].get())
    else:
        raise ValueError(f"Unknown initial condition: {initcond}")

def create_window():
    root = tk.Tk()
    root.title("Heat Equation App")

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.LEFT, fill=tk.Y)

    plot_frame = tk.Frame(root)
    plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    fig = Figure(figsize=(10, 6), dpi=100)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw_idle()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    controls = create_controls(control_frame, fig, canvas, run_simulation_1D)

    root.mainloop()


