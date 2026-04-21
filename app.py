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

def create_window():
    root = tk.Tk()
    root.title("Heat Equation App")

    alpha_slider = tk.Scale(
        root, 
        from_ = 0.00001,
        to = 0.001,
        resolution = 0.0001,
        orient = tk.HORIZONTAL,
        label = "Alpha"
    )
    alpha_slider.pack()
    
    fig = Figure(figsize = (10,6), dpi = 100)

    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

    button = tk.Button(
        root, 
        text = "Run Animation", 
        command = lambda: run_simulation(fig, canvas, alpha_slider))
    button.pack()

    root.mainloop()


