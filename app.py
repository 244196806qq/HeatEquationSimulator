import tkinter as tk
import numpy as np
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from heat_equation_solver_1D import gaussian_initial_temperatures, solve_heat_1d, two_peak_initial_conidtion, spikes_initial_temperatures


def run_simulation(fig, canvas, initcond, alpha, Nx, numTimes, shape_controls):
    # calculate all the values for the graph
    x, initial_temp = generate_initial_condition(initcond, Nx, shape_controls)
    temps = calculate_parameter(alpha, x, numTimes, initial_temp)

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


def generate_initial_condition(initcond, Nx, shape_controls):
    if (initcond == "Gaussian"):
        return gaussian_initial_temperatures(Nx, shape_controls["center_slider"].get(), shape_controls["width_slider"].get())
    elif (initcond == "Spike"):
        return spikes_initial_temperatures(Nx, shape_controls["position_slider"].get(), shape_controls["height_slider"].get())
    elif (initcond == "Two Peaks"):
        return two_peak_initial_conidtion(
            Nx, 
            shape_controls["center1_slider"].get(), 
            shape_controls["width1_slider"].get(), 
            shape_controls["center2_slider"].get(), 
            shape_controls["width2_slider"].get(), 
            shape_controls["height1_slider"].get(),
            shape_controls["height2_slider"].get())
    else:
        raise ValueError(f"Unknown initial condition: {initcond}")



def calculate_parameter(alpha, x, numTimes, initial_temp):
    deltaX = x[1] - x[0]
    deltaT = 0.001
    r = alpha * deltaT / (deltaX ** 2)
    return solve_heat_1d(initial_temp, r, numTimes)

def update_r_label(alpha_slider, Nx_slider, r_label):
    alpha = alpha_slider.get()
    Nx = Nx_slider.get()

    x = np.linspace(0, 1, int(Nx))
    deltaX = x[1] - x[0]
    deltaT = 0.001

    r = alpha * deltaT / (deltaX ** 2)

    r_label.config(text = f"r = {r:.4f}")

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def build_parameter_controls(parameter_frame, shape_var):
    clear_frame(parameter_frame)
    controls = {}

    shape = shape_var.get()

    if shape == "Gaussian":
        center_slider = tk.Scale(
            parameter_frame, from_=0.0, to=1.0, resolution=0.05,
            orient=tk.HORIZONTAL, label="Center"
        )
        center_slider.set(0.5)
        center_slider.pack()

        width_slider = tk.Scale(
            parameter_frame, from_=0.02, to=0.3, resolution=0.01,
            orient=tk.HORIZONTAL, label="Width"
        )
        width_slider.set(0.1)
        width_slider.pack()

        controls["center_slider"] = center_slider
        controls["width_slider"] = width_slider

    elif shape == "Spike":
        position_slider = tk.Scale(
            parameter_frame, from_=0.0, to=1.0, resolution=0.05,
            orient=tk.HORIZONTAL, label="Position"
        )
        position_slider.set(0.5)
        position_slider.pack()

        height_slider = tk.Scale(
            parameter_frame, from_=0.0, to=1.0, resolution=0.05,
            orient=tk.HORIZONTAL, label="Height"
        )
        height_slider.set(0.3)
        height_slider.pack()

        controls["position_slider"] = position_slider
        controls["height_slider"] = height_slider

    elif shape == "Two Peaks":
        center1_slider = tk.Scale(
            parameter_frame, from_=0.0, to=1.0, resolution=0.05,
            orient=tk.HORIZONTAL, label="Center 1"
        )
        center1_slider.set(0.3)
        center1_slider.pack()

        width1_slider = tk.Scale(
            parameter_frame, from_=0.02, to=0.3, resolution=0.01,
            orient=tk.HORIZONTAL, label="Width 1"
        )
        width1_slider.set(0.08)
        width1_slider.pack()

        center2_slider = tk.Scale(
            parameter_frame, from_=0.0, to=1.0, resolution=0.05,
            orient=tk.HORIZONTAL, label="Center 2"
        )
        center2_slider.set(0.7)
        center2_slider.pack()

        width2_slider = tk.Scale(
            parameter_frame, from_=0.02, to=0.3, resolution=0.01,
            orient=tk.HORIZONTAL, label="Width 2"
        )
        width2_slider.set(0.08)
        width2_slider.pack() 

        height1_slider = tk.Scale(
            parameter_frame, from_=0.01, to=1.0, resolution=0.05,
            orient=tk.HORIZONTAL, label="Height 1"
        )
        height1_slider.set(0.3)
        height1_slider.pack()

        height2_slider = tk.Scale(
            parameter_frame, from_=0.01, to=1.0, resolution=0.01,
            orient=tk.HORIZONTAL, label="Height 2"
        )
        height2_slider.set(0.08)
        height2_slider.pack()

        controls["center1_slider"] = center1_slider
        controls["width1_slider"] = width1_slider
        controls["center2_slider"] = center2_slider
        controls["width2_slider"] = width2_slider
        controls["height1_slider"] = height1_slider
        controls["height2_slider"] = height2_slider

    return controls


def create_controls(control_frame, fig, canvas):
    # text for value of r
    r_label = tk.Label(control_frame, text = "r = 0.005")

    # slider for alpha
    alpha_slider = tk.Scale(
        control_frame, 
        from_ = 0.001,
        to = 0.04,
        resolution = 0.001,
        orient = tk.HORIZONTAL,
        label = "Alpha",
        command = lambda value: update_r_label(alpha_slider, Nx_slider, r_label)
    )
    alpha_slider.set(0.005)
    alpha_slider.pack()

    # slider for number of position points
    Nx_slider = tk.Scale(
        control_frame, 
        from_ = 10,
        to = 200,
        resolution = 10,
        orient = tk.HORIZONTAL,
        label = "Number of X",
        command = lambda value: update_r_label(alpha_slider, Nx_slider, r_label)
    )
    Nx_slider.set(100)
    Nx_slider.pack()    
    
    # show the value of r
    r_label.pack()

    # input for number of run times
    numTimes_group = tk.Frame(control_frame)
    numTimes_group.pack(fill=tk.X, pady=5)

    numTimes_label = tk.Label(numTimes_group, text="Run Time")
    numTimes_label.pack()
    def only_numbers(char):
        return char.isdigit()

    vcmd = numTimes_group.register(only_numbers)

    numTimes_slider = tk.Entry(
        numTimes_group,
        width = 10,
        validate="key",
        validatecommand=(vcmd, "%S")

    )
    numTimes_slider.insert(0, "1000")
    numTimes_slider.pack()    

    # dropdown menu
    shape_group = tk.Frame(control_frame)
    shape_group.pack(fill=tk.X, pady=5)

    shape_label = tk.Label(shape_group, text="Shape of Graph")
    shape_label.pack()

    shape_var = tk.StringVar()
    shape_var.set("Gaussian")
    condition_dropdown = tk.OptionMenu(
        shape_group,
        shape_var,
        "Gaussian",
        "Spike",
        "Two Peaks"
    )
    condition_dropdown.pack()

    # parameter menu
    parameter_frame = tk.Frame(control_frame)
    parameter_frame.pack()
    
    shape_controls = {}

    def on_shape_change(*args):
        nonlocal shape_controls
        shape_controls = build_parameter_controls(parameter_frame, shape_var)

    shape_var.trace_add("write", on_shape_change)

    shape_controls = build_parameter_controls(parameter_frame, shape_var)

    # Run button
    runButton = tk.Button(
        control_frame, 
        text = "Run Animation", 
        command = lambda: run_simulation(
            fig, 
            canvas, 
            shape_var.get(), 
            alpha_slider.get(),
            Nx_slider.get(),  
            int(numTimes_slider.get()),
            shape_controls
        )
    )
    runButton.pack()
    
    return {
        "alpha_slider": alpha_slider,
        "center_slider": 1,
        "Nx_slider": Nx_slider,
        "number_times": numTimes_slider,
        "condition_dropmenu": condition_dropdown,
        "run_button": runButton,
    }



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

    controls = create_controls(control_frame, fig, canvas)

    root.mainloop()


