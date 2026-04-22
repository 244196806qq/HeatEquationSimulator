import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from heat_equation_solver import gaussian_initial_temperatures, solve_heat_1d, two_peak_initial_conidtion, spikes_initial_temperatures


def run_simulation(fig, canvas, initcond, alpha, Nx, center, width, is_animating):
    if is_animating["value"]:
        return

    is_animating["value"] = True

    x, initial_temp = generate_initial_condition(initcond, Nx, center, width)
    
    temps = calculate_parameter(alpha, x, initial_temp)
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)
    line, = ax.plot(x, temps[0])
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, max(max(t) for t in temps) * 1.05)

    ax.set_title("Heat diffusion on a 1D rod")
    ax.set_xlabel("Position")
    ax.set_ylabel("Temperature")

    def update(frame = 0):
        if frame >= len(temps):
            return 
        
        line.set_ydata(temps[frame])
        canvas.draw_idle()

        canvas.get_tk_widget().after(30, update, frame + 1)
    
    update()



def generate_initial_condition(initcond, Nx, center, width):
    if (initcond == "Gaussian"):
        return gaussian_initial_temperatures(Nx, center, width)
    elif (initcond == "Spike"):
        return spikes_initial_temperatures(Nx, center, width)
    elif (initcond == "Two Peaks"):
        return two_peak_initial_conidtion(Nx, center, width)
    else:
        raise ValueError(f"Unknown initial condition: {initcond}")



def calculate_parameter(alpha, x, initial_temp):
    deltaX = x[1] - x[0]
    deltaT = 0.0001
    r = 0.4 #alpha * deltaT / (deltaX ** 2)
    numTimes = 100 # number of times it's simulated
    return solve_heat_1d(initial_temp, r, numTimes)


def create_controls(control_frame, fig, canvas, is_animating):
    # dropdown menu
    initial_condition_var = tk.StringVar()
    initial_condition_var.set("Gaussian")
    condition_dropdown = tk.OptionMenu(
        control_frame,
        initial_condition_var,
        "Gaussian",
        "Spike",
        "Two Peaks"
    )
    condition_dropdown.pack()


    # slider for alpha
    alpha_slider = tk.Scale(
        control_frame, 
        from_ = 0.00001,
        to = 0.001,
        resolution = 0.00001,
        orient = tk.HORIZONTAL,
        label = "Alpha"
    )
    alpha_slider.set(0.0002)
    alpha_slider.pack()

    # slider for width
    width_slider = tk.Scale(
        control_frame, 
        from_ = 0.05,
        to = 0.3,
        resolution = 0.05,
        orient = tk.HORIZONTAL,
        label = "Width"
    )
    width_slider.set(0.2)
    width_slider.pack()

    # slider for center
    center_slider = tk.Scale(
        control_frame, 
        from_ = 0.01,
        to = 1,
        resolution = 0.05,
        orient = tk.HORIZONTAL,
        label = "Center"
    )
    center_slider.set(0.5)
    center_slider.pack()

    # slider for number of position points
    Nx_slider = tk.Scale(
        control_frame, 
        from_ = 10,
        to = 1000,
        resolution = 10,
        orient = tk.HORIZONTAL,
        label = "Nx"
    )
    Nx_slider.set(100)
    Nx_slider.pack()

    # Run button
    runButton = tk.Button(
        control_frame, 
        text = "Run Animation", 
        command = lambda: run_simulation(
            fig, 
            canvas, 
            initial_condition_var.get(), 
            alpha_slider.get(),
            Nx_slider.get(), 
            center_slider.get(), 
            width_slider.get(),
            is_animating
        )
    )
    runButton.pack()
    
    return {
        "alpha_slider": alpha_slider,
        "width_slider": width_slider,
        "center_slider": center_slider,
        "Nx_slider": Nx_slider,
        "condition_dropmenu": condition_dropdown,
        "run_button": runButton,
    }






def create_window():
    root = tk.Tk()
    root.title("Heat Equation App")
    is_animating = {"value": False}

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.LEFT, fill=tk.Y)

    plot_frame = tk.Frame(root)
    plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    fig = Figure(figsize=(10, 6), dpi=100)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw_idle()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    controls = create_controls(control_frame, fig, canvas, is_animating)

    root.mainloop()


