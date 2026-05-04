# Heat Equation Simulator (Tkinter + Matplotlib)

A Python-based interactive simulator for visualizing heat diffusion in **1D rods** and **2D plates**, built using **Tkinter** for UI and **Matplotlib** for visualization.

---

## 📌 Features

* 🧊 **1D Heat Diffusion**

  * Line plot animation
  * Multiple initial conditions (Gaussian, Spike, Two Peaks)

* 🌡️ **2D Heat Diffusion**

  * Heatmap animation using `imshow`
  * Adjustable grid resolution (Nx, Ny)

* 🎛️ **Interactive Controls**

  * Thermal diffusivity (α)
  * Grid resolution
  * Time steps
  * Shape parameters (center, width, height, etc.)

* ⏯️ **Real-time Animation**

  * Smooth frame updates using Tkinter `.after()`
  * Pause / Resume via status bar

* ⚠️ **Stability Checking**

  * Automatically warns if simulation is unstable:

    * 1D: `r ≥ 0.5`
    * 2D: `r ≥ 0.25`
  
* 🧱 **Boundary Conditions**

  * Dirichlet (fixed-temperature boundaries)
  * Neumann (insulated/no-flux boundaries)
  * Allows comparison of how edge constraints affect heat diffusion over time

## 🧠 Mathematical Model

This simulator solves the heat equation:

$\frac{\partial u}{\partial t} = \alpha \nabla^2 u$

Using the **explicit finite difference method**:

* 1D:
  $u_i^{n+1} = u_i^n + r (u_{i+1}^n - 2u_i^n + u_{i-1}^n)$

* Stability condition:
  $r = \frac{\alpha \Delta t}{\Delta x^2}$

* 2D:
  $u_{i,j}^{n+1} = u_{i,j}^n + r_x (u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n)+ r_y (u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n)$

* Stability condition:
  $r_x = \frac{\alpha \Delta t}{\Delta x^2}$ and 
  $r_y = \frac{\alpha \Delta t}{\Delta y^2}$

---

## 📁 Project Structure

```
.
├── main.py                      # Entry point
├── app.py                       # Main app + simulation runner
├── UI_helper.py                 # UI components and control panels
├── heat_equation_solver_1D.py   # 1D solver + initial conditions
├── heat_equation_solver_2D.py   # 2D solver + initial conditions
├── Data_Files                   # Folder with Sample Data Files
    ├── gaussian.txt             # File with Gaussian shape data
    ├── spike.txt                # File with spike shape data
    ├── two_peaks.txt            # File with two peaks shape data
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/244196806qq/HeatEquationSimulator.git
cd HeatEquationSimulator
```

### 2. Install dependencies

```bash
pip install numpy matplotlib
```

(Tkinter is included with standard Python installations)

### 3. Run the app

```bash
python main.py
```

---

## 🎮 How to Use

1. Select **1D Rod** or **2D Plate**
2. Adjust parameters:

   * α (thermal diffusivity)
   * Grid size (Nx / Ny)
   * Time steps
3. Choose an initial condition
4. Click **▶ RUN SIMULATION**
5. Click the **status bar** to pause/resume

---

## Loading Initial Conditions from Files

  The simulator supports loading custom initial temperature distributions from external data files. Users can place multiple `.csv` or `.txt` files inside a selected folder, and the application will automatically detect and display the available datasets in the UI.

## File Format

  Each file should contain two columns:

  ```text
  x,temp
  0.00,0.0
  0.01,0.2
  0.02,0.5
  ```
---

## 🛠️ Implementation Details

* Uses **explicit finite difference method**
* Animation handled via:

  ```python
  widget.after(delay, update)
  ```
* Prevents overlapping animations using stored `after_id`
* Dynamic UI updates for parameter controls
* Custom light theme for improved readability

---

## 📈 Future Improvements

* Export animation (GIF / video)
* Performance optimization (NumPy vectorization / GPU)
* Drag-and-drop dataset loading
* Real-time file reloading
* 2D image-based temperature initialization
* Generate temp value vs x position data file after simulation
---

## 💡 Motivation

This project was built to:

* Understand numerical solutions to PDEs
* Visualize diffusion processes intuitively
* Practice combining **math + programming + UI design**

---

## 🧑‍💻 Author

Devin Liang

Applied Mathematics Student
