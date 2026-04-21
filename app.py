import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from heat_equation_solver import generate_initial_temperatures, solve_heat_1d

def run_simulation(fig, canvas, alpha_slider):
    x, initial_temp = generate_initial_temperatures()
    temps = calculate_parameter(alpha_slider, x, initial_temp)

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

def calculate_parameter(alpha_slider, x, initial_temp):
    alpha = alpha_slider.get() # thermal diffusivity of silver, pure (99.9%)
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
    # dropdown = tk.OptionMenu(
    #     control_fram,
    #     from_ = 0.00001,
    #     to = 0.001,
    #     resolution = 0.00001,
    #     orient = tk.HORIZONTAL,
    #     label = "Width"
    # )

    # Run button
    runButton = tk.Button(
        control_fram, 
        text = "Run Animation", 
        command = lambda: run_simulation(fig, canvas, alpha_slider)
    )
    runButton.pack()
    
    return {
        "alpha_slider": alpha_slider,
        "run_button": runButton
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


