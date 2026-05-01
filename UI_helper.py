import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
import os

# ─── Theme ────────────────────────────────────────────────────────────────────
BG = "#f7f9fb" # background of graph panel
PANEL = "#ffffff" # background of sidebar panel
SURFACE = "#eef2f6" # entry and dropdown
BORDER = "#cbd5e1" # panel border 
ACCENT = "#2563eb" # labels and headers
TEXT = "#111827" # primary text color
TEXT_DIM = "#4b5563" # secondary text
SUCCESS = "#16a34a" # completion indicator
WARNING = "#dc2626" # erro indicator

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    "#0a0c12",
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   TEXT_DIM,
    "axes.titlecolor":   TEXT,
    "xtick.color":       TEXT_DIM,
    "ytick.color":       TEXT_DIM,
    "text.color":        TEXT,
    "grid.color":        BORDER,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})


# def update_r_label(alpha_slider, Nx_slider, r_label):
#     alpha = alpha_slider.get()
#     Nx = Nx_slider.get()

#     x = np.linspace(0, 1, int(Nx))
#     deltaX = x[1] - x[0]
#     deltaT = 0.001

#     r = alpha * deltaT / (deltaX ** 2)

#     r_label.config(text = f"r = {r:.4f}")

# ─── Helpers ──────────────────────────────────────────────────────────────────

def styled_scale(parent, label, from_, to, resolution, initial, width=180):
    frame = tk.Frame(parent, bg=PANEL)
    frame.pack(fill=tk.X, padx=12, pady=3)
    row = tk.Frame(frame, bg=PANEL)
    row.pack(fill=tk.X)
    tk.Label(row, text=label, bg=PANEL, fg=TEXT_DIM,
             font=("Arial", 11), anchor="w").pack(side=tk.LEFT)
    val_lbl = tk.Label(row, text=f"{initial}", bg=PANEL, fg=ACCENT,
                       font=("Arial", 11, "bold"), width=6, anchor="e")
    val_lbl.pack(side=tk.RIGHT)
    scale = tk.Scale(
        frame,
        from_=from_,
        to=to,
        resolution=resolution,
        orient=tk.HORIZONTAL,
        bg=PANEL,
        fg=TEXT,
        troughcolor="#dbeafe",
        activebackground=ACCENT,
        highlightthickness=1,
        highlightbackground=BORDER,
        width=14,
        sliderlength=22,
        showvalue=False,
        command=lambda v: val_lbl.config(text=f"{float(v):.3g}")
    )
    scale.set(initial)
    scale.pack(fill=tk.X)
    return scale

def section_header(parent, text):
    f = tk.Frame(parent, bg=PANEL)
    f.pack(fill=tk.X, padx=12, pady=(14, 4))
    tk.Label(f, text="▸ " + text.upper(), bg=PANEL, fg=ACCENT,
             font=("Arial", 10, "bold")).pack(anchor="w")
    tk.Frame(f, bg=BORDER, height=1).pack(fill=tk.X, pady=(3, 0))

def section_sep(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill=tk.X, padx=12, pady=6)

# ─── Shape controls ───────────────────────────────────────────────────────────

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def build_shape_controls_1D(container, shape):
    clear_frame(container)
    c = {}
    if shape == "Gaussian":
        c["center"] = styled_scale(container, "Center",      0.0,  1.0,  0.05,  0.5)
        c["width"]  = styled_scale(container, "Width",       0.02, 0.35, 0.01,  0.1)
        show_analytical_var = tk.BooleanVar(value = False)
        c["show_analytical_var"] = show_analytical_var
        analytical_checkbox = tk.Checkbutton(
            container,
            text = "Show Analytical Solution",
            variable = show_analytical_var,
            bg=PANEL,
            fg=TEXT_DIM,
            activebackground=PANEL,
            activeforeground=ACCENT,
            selectcolor=SURFACE,
            font=("Arial", 11),
        )
        analytical_checkbox.pack(anchor="w", padx=12, pady=(4, 8))
    elif shape == "Spike":
        c["position"] = styled_scale(container, "Position", 0.0, 1.0, 0.05, 0.5)
        c["height"]   = styled_scale(container, "Height",   0.1, 2.0, 0.05, 1.0)
    elif shape == "Two Peaks":
        c["center1"] = styled_scale(container, "Center 1",  0.0, 1.0, 0.05, 0.3)
        c["width1"]  = styled_scale(container, "Width 1",   0.02, 0.3, 0.01, 0.08)
        c["height1"] = styled_scale(container, "Height 1",  0.1, 2.0, 0.05, 1.0)
        c["center2"] = styled_scale(container, "Center 2",  0.0, 1.0, 0.05, 0.7)
        c["width2"]  = styled_scale(container, "Width 2",   0.02, 0.3, 0.01, 0.08)
        c["height2"] = styled_scale(container, "Height 2",  0.1, 2.0, 0.05, 1.0)
    elif shape == "From File":
        folder_var = tk.StringVar(value="")
        file_var = tk.StringVar(value="")

        c["folder_path"] = folder_var
        c["file_path"] = file_var
        file_options = []
        def choose_folder():
            folder = filedialog.askdirectory(title = "Select Data Folder")
            
            if not folder:
                return
            
            folder_var.set(folder)
            files = [
                f for f in os.listdir(folder)
                if f.endswith((".csv", "txt"))
            ]
            files.sort()
            file_dropdown["values"] = files
            
            if files: 
                file_var.set(files[0])
            else:
                file_var.set("")

        tk.Button(
            container,
            text="Choose Data Folder",
            command=choose_folder,
            bg=SURFACE,
            fg=TEXT_DIM,
            relief="flat",
            cursor="hand2",
            font=("Arial", 11)
        ).pack(fill=tk.X, padx=12, pady=(6, 2))

        tk.Label(
            container,
            textvariable=folder_var,
            bg=PANEL,
            fg=TEXT_DIM,
            wraplength=180,
            font=("Arial", 8)
        ).pack(fill=tk.X, padx=12, pady=(0, 6))

        file_dropdown = ttk.Combobox(
            container,
            textvariable=file_var,
            values=file_options,
            state="readonly",
            font=("Arial", 11)
        )
        file_dropdown.pack(fill=tk.X, padx = 12, pady = (2,6))

    return c

def build_shape_controls_2D(container, shape):
    clear_frame(container)
    c = {}
    if shape == "Gaussian":
        c["centerX"] = styled_scale(container, "Center X",  0.0, 1.0, 0.05, 0.5)
        c["centerY"] = styled_scale(container, "Center Y",  0.0, 1.0, 0.05, 0.5)
        c["width"]   = styled_scale(container, "Width",     0.02, 0.35, 0.01, 0.1)
    elif shape == "Spike":
        c["posX"]   = styled_scale(container, "Position X", 0.0, 1.0, 0.05, 0.5)
        c["posY"]   = styled_scale(container, "Position Y", 0.0, 1.0, 0.05, 0.5)
        c["height"] = styled_scale(container, "Height",     0.1, 5.0, 0.1,  1.0)
    elif shape == "Two Peaks":
        c["center1X"] = styled_scale(container, "Peak 1  X",   0.0, 1.0, 0.05, 0.3)
        c["center1Y"] = styled_scale(container, "Peak 1  Y",   0.0, 1.0, 0.05, 0.3)
        c["width1"]   = styled_scale(container, "Width 1",     0.02, 0.3, 0.01, 0.08)
        c["height1"]  = styled_scale(container, "Height 1",    0.1, 2.0, 0.05, 1.0)
        c["center2X"] = styled_scale(container, "Peak 2  X",   0.0, 1.0, 0.05, 0.7)
        c["center2Y"] = styled_scale(container, "Peak 2  Y",   0.0, 1.0, 0.05, 0.7)
        c["width2"]   = styled_scale(container, "Width 2",     0.02, 0.3, 0.01, 0.08)
        c["height2"]  = styled_scale(container, "Height 2",    0.1, 2.0, 0.05, 1.0)
    return c

# ─── Control panels ───────────────────────────────────────────────────────────

def make_dropdown(parent, var, options, on_change):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Heat.TCombobox",
        fieldbackground=SURFACE, background=SURFACE,
        foreground=TEXT, bordercolor=BORDER,
        arrowcolor=ACCENT, selectbackground=SURFACE,
        selectforeground=ACCENT,
    )
    cb = ttk.Combobox(
        parent, textvariable=var, values=options,
        state="readonly", style="Heat.TCombobox",
        font=("Arial", 11),
    )
    def clear_combobox_highlight():
        cb.selection_clear()
        cb.icursor(tk.END)
        cb.winfo_toplevel().focus_force()

    def handle_select(event):
        if on_change is not None:
            on_change()

        cb.after(10, clear_combobox_highlight)

    cb.pack(fill=tk.X, padx=12, pady=4)
    cb.bind("<<ComboboxSelected>>", handle_select)
    # var.trace_add("write", handle_change)
    return cb

def make_run_button(parent, command):
    btn = tk.Button(
        parent, text="▶  RUN SIMULATION",
        command=command,
        bg=ACCENT, fg=ACCENT, font=("Arial", 10, "bold"),
        relief="flat", cursor="hand2", padx=10, pady=8,
        activebackground="#81d4fa", activeforeground=BG,
    )
    btn.pack(fill=tk.X, padx=12, pady=(10, 6))
    return btn

def create_panel_1D(panel, fig, canvas, animation_state, status_var, status_label, run_simulation_1D):
    section_header(panel, "Solver Parameters")

    speed_scale = styled_scale(panel, "Animation Speed (ms)", 5, 100, 1, 20)
    alpha_scale = styled_scale(panel, "Thermal diffusivity  α", 0.001, 0.04, 0.001, 0.005)
    Nx_scale = styled_scale(panel, "Grid points  Nx", 10, 200, 10, 100)

    # numTimes entry
    section_header(panel, "Simulation")
    nt_frame = tk.Frame(panel, bg=PANEL)
    nt_frame.pack(fill=tk.X, padx=12, pady=3)
    tk.Label(nt_frame, text="Time steps", bg=PANEL, fg=TEXT_DIM,
             font=("Arial", 11)).pack(anchor="w")
    vcmd = panel.register(str.isdigit)
    nt_entry = tk.Entry(
        nt_frame, width=10, validate="key",
        validatecommand=(vcmd, "%S"),
        bg=SURFACE, fg=ACCENT, insertbackground=ACCENT,
        relief="flat", font=("Arial", 11),
        highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER,
    )
    nt_entry.insert(0, "1000")
    nt_entry.pack(anchor="w", pady=2)

    boundary_var = tk.StringVar(value="Dirichlet")
    def on_boundary_change(*_):
        pass
    
    make_dropdown(
        panel,
        boundary_var,
        ["Dirichlet", "Neumann"],
        on_boundary_change
    )

    section_header(panel, "Initial Condition")

    shape_var = tk.StringVar(value="Gaussian")
    shape_container = tk.Frame(panel, bg=PANEL)

    shape_controls_ref = [None]

    def rebuild_shape_controls(*_):
        shape_controls_ref[0] = build_shape_controls_1D(
            shape_container,
            shape_var.get()
        )

    make_dropdown(
        panel,
        shape_var,
        ["Gaussian", "Spike", "Two Peaks", "From File"],
        rebuild_shape_controls
    )

    rebuild_shape_controls()

    shape_container.pack(fill=tk.X)

    def run_safe():
        if not nt_entry.get():
            status_var.set("⚠ Enter number of time steps")
            return

        run_simulation_1D(
            fig,
            canvas,
            status_var,
            animation_state,
            status_label,
            shape_var.get(),
            speed_scale.get(),
            alpha_scale.get(),
            int(Nx_scale.get()),
            int(nt_entry.get()),
            shape_controls_ref[0],
            boundary_var.get()
        )

    section_sep(panel)
    make_run_button(panel, run_safe)


def create_panel_2D(panel, fig, canvas, animation_state, status_var, status_label, run_simulation_2D):
    section_header(panel, "Solver Parameters")
    
    speed_scale = styled_scale(panel, "Animation Speed (ms)", 5, 100, 1, 20)
    alpha_scale = styled_scale(panel, "Thermal diffusivity  α", 0.001, 0.04, 0.001, 0.005)
    Nx_scale    = styled_scale(panel, "Grid points  Nx",        10, 120, 1, 60)
    Ny_scale    = styled_scale(panel, "Grid points  Ny",        10, 120, 1, 60)

    section_header(panel, "Simulation")
    nt_frame = tk.Frame(panel, bg=PANEL)
    nt_frame.pack(fill=tk.X, padx=12, pady=3)
    tk.Label(nt_frame, text="Time steps", bg=PANEL, fg=TEXT_DIM,
             font=("Arial", 9)).pack(anchor="w")
    vcmd = panel.register(str.isdigit)
    nt_entry = tk.Entry(
        nt_frame, width=10, validate="key",
        validatecommand=(vcmd, "%S"),
        bg=SURFACE, fg=ACCENT, insertbackground=ACCENT,
        relief="flat", font=("Arial", 9),
        highlightthickness=1, highlightcolor=BORDER, highlightbackground=BORDER,
    )
    nt_entry.insert(0, "500")
    nt_entry.pack(anchor="w", pady=2)

    boundary_var = tk.StringVar(value="Dirichlet")
    def on_boundary_change(*_):
        pass
    
    make_dropdown(
        panel,
        boundary_var,
        ["Dirichlet", "Neumann"],
        on_boundary_change
    )

    section_header(panel, "Initial Condition")

    shape_var = tk.StringVar(value="Gaussian")
    shape_container = tk.Frame(panel, bg=PANEL)

    shape_controls_ref = [None]

    def rebuild_shape_controls(*_):
        shape_controls_ref[0] = build_shape_controls_2D(
            shape_container,
            shape_var.get()
        )

    make_dropdown(
        panel,
        shape_var,
        ["Gaussian", "Spike", "Two Peaks"],
        rebuild_shape_controls
    )

    rebuild_shape_controls()
    shape_container.pack(fill=tk.X)

    def run_safe():
        if not nt_entry.get():
            status_var.set("⚠ Enter number of time steps")
            return
        
        run_simulation_2D( 
            fig,
            canvas,
            status_var,
            animation_state,
            status_label,
            shape_var.get(),
            speed_scale.get(),
            alpha_scale.get(),
            int(Nx_scale.get()),
            int(Ny_scale.get()),
            int(nt_entry.get()),
            shape_controls_ref[0],
            boundary_var.get()
        )

    section_sep(panel)
    make_run_button(panel, run_safe)

