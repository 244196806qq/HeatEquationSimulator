import tkinter as tk
import numpy as np
from tkinter import messagebox


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


def build_parameter_controls_1D(parameter_frame, shape_var):
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


def create_controls_1D(control_frame, fig, canvas, run_simulation_1D):
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
        shape_controls = build_parameter_controls_1D(parameter_frame, shape_var)

    shape_var.trace_add("write", on_shape_change)

    shape_controls = build_parameter_controls_1D(parameter_frame, shape_var)

    # Run button
    runButton = tk.Button(
        control_frame, 
        text = "Run Animation", 
        command = lambda: run_simulation_1D(
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
