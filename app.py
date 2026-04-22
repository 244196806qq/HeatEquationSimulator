import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from heat_equation_solver import generate_initial_temperatures, solve_heat_1d


def run_simulation(fig, canvas, alpha, Nx, center, width):
    x, initial_temp = generate_initial_temperatures(Nx, center, width)
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
        canvas.draw()

        canvas.get_tk_widget().after(30, update, frame + 1)
    
    update()


def calculate_parameter(alpha, x, initial_temp):
    deltaX = x[1] - x[0]
    deltaT = 0.4 * deltaX**2 / alpha
    r = alpha * deltaT / (deltaX ** 2)
    numTimes = 100 # number of times it's simulated

    return solve_heat_1d(initial_temp, r, numTimes)


def create_controls(root, fig, canvas):
    control_fram = tk.Frame(root)
    control_fram.pack(side = tk.LEFT, fill = tk.Y)

    # slider for alpha
    alpha_slider = tk.Scale(
        control_fram, 
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
        control_fram, 
        from_ = 0.00001,
        to = 0.001,
        resolution = 0.00001,
        orient = tk.HORIZONTAL,
        label = "Width"
    )
    width_slider.set(0.0002)
    width_slider.pack()

    # slider for center
    center_slider = tk.Scale(
        control_fram, 
        from_ = 1,
        to = 100,
        resolution = 1,
        orient = tk.HORIZONTAL,
        label = "Center"
    )
    center_slider.set(20)
    center_slider.pack()

    # slider for number of position points
    Nx_slider = tk.Scale(
        control_fram, 
        from_ = 1,
        to = 1000,
        resolution = 10,
        orient = tk.HORIZONTAL,
        label = "Nx"
    )
    Nx_slider.set(100)
    Nx_slider.pack()

    # dropdown menu
    initial_condition_var = tk.StringVar()
    initial_condition_var.set("Gaussian")
    condition_dropdown = tk.OptionMenu(
        control_fram,
        initial_condition_var,
        "Gaussian",
        "Spike",
        "Two Peaks"
    )
    condition_dropdown.pack()

    # Run button
    runButton = tk.Button(
        control_fram, 
        text = "Run Animation", 
        command = lambda: run_simulation(fig, canvas, alpha_slider.get(), Nx_slider.get(), center_slider.get(), width_slider.get())
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

    fig = Figure(figsize = (10,6), dpi = 100)

    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

    controls = create_controls(root, fig, canvas)

    root.mainloop()


