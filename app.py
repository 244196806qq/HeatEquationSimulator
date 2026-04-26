import tkinter as tk
from tkinter import ttk, font
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from heat_equation_solver_1D import (
    gaussian_initial_temperatures_1D,
    solve_heat_1D,
    two_peak_initial_condition_1D,
    spikes_initial_temperatures_1D,
)
from heat_equation_solver_2D import (
    gaussian_initial_temperatures_2D,
    solve_heat_2D,
    two_peak_initial_condition_2D,
    spike_initial_temperatures_2D,
)

from UI_helper import create_panel_1D, create_panel_2D, clear_frame

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

# ─── Simulation logic ─────────────────────────────────────────────────────────

def get_initial_condition_1D(initcond, Nx, controls):
    if initcond == "Gaussian":
        return gaussian_initial_temperatures_1D(
            Nx, controls["center"].get(), controls["width"].get()
        )
    elif initcond == "Spike":
        return spikes_initial_temperatures_1D(
            Nx, controls["position"].get(), controls["height"].get()
        )
    elif initcond == "Two Peaks":
        return two_peak_initial_condition_1D(
            Nx,
            controls["center1"].get(), controls["width1"].get(),
            controls["center2"].get(), controls["width2"].get(),
            controls["height1"].get(), controls["height2"].get(),
        )
    raise ValueError(f"Unknown: {initcond}")

def get_initial_condition_2D(initcond, Nx, Ny, controls):
    if initcond == "Gaussian":
        return gaussian_initial_temperatures_2D(
            Nx, Ny,
            controls["centerX"].get(), controls["centerY"].get(), controls["width"].get()
        )
    elif initcond == "Spike":
        return spike_initial_temperatures_2D(
            Nx, Ny,
            controls["posX"].get(), controls["posY"].get(), controls["height"].get()
        )
    elif initcond == "Two Peaks":
        return two_peak_initial_condition_2D(
            Nx, Ny,
            (controls["center1X"].get(), controls["center1Y"].get()),
            controls["width1"].get(), controls["height1"].get(),
            (controls["center2X"].get(), controls["center2Y"].get()),
            controls["width2"].get(), controls["height2"].get(),
        )
    raise ValueError(f"Unknown: {initcond}")

def compute_r(alpha, Nx):
    x = np.linspace(0, 1, int(Nx))
    dX = x[1] - x[0]
    dT = 0.001
    return alpha * dT / (dX ** 2)

# ─── 1D simulation ────────────────────────────────────────────────────────────

def run_simulation_1D(fig, canvas, status_var, animation_state, status_label, initcond, alpha, Nx, numTimes, controls):
    animation_state["running"] = True
    status_label.config(cursor="hand2")
    if animation_state["after_id"] is not None:
        canvas.get_tk_widget().after_cancel(animation_state["after_id"])
        animation_state["after_id"] = None

    r = compute_r(alpha, Nx)
    if r >= 0.5:
        status_var.set(f"⚠  Unstable: r = {r:.4f} ≥ 0.5 — reduce alpha or increase Nx")
        return

    x, initial_temp = get_initial_condition_1D(initcond, Nx, controls)
    temps = solve_heat_1D(initial_temp, r, numTimes)

    fig.clear()
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)

    y_max = max(max(t) for t in temps) * 1.08 or 1.0
    line, = ax.plot(x, temps[0], color=ACCENT, linewidth=1.8, alpha=0.95)
    fill = ax.fill_between(x, temps[0], alpha=0.15, color=ACCENT)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, y_max)
    ax.set_xlabel("Position  x")
    ax.set_ylabel("Temperature  u(x,t)")

    # Hover annotation
    annot = ax.annotate(
        "", xy=(0, 0), xytext=(12, 12), textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.4", fc=SURFACE, ec=ACCENT, lw=1),
        arrowprops=dict(arrowstyle="->", color=ACCENT),
        fontsize=8, color=TEXT,
    )
    annot.set_visible(False)

    def hover(event):
        if event.inaxes != ax or event.xdata is None:
            annot.set_visible(False)
            canvas.draw_idle()
            return
        idx = np.argmin(np.abs(line.get_xdata() - event.xdata))
        annot.xy = (line.get_xdata()[idx], line.get_ydata()[idx])
        annot.set_text(f"x={line.get_xdata()[idx]:.3f}\nu={line.get_ydata()[idx]:.4f}")
        annot.set_visible(True)
        canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    def update(frame=0):
        if animation_state["paused"]:
            animation_state["after_id"] = canvas.get_tk_widget().after(50, update, frame)
            return 
        
        if frame >= len(temps):
            animation_state["after_id"] = None
            status_var.set(f"✓  Done — r = {r:.4f}  |  steps = {numTimes}")
            animation_state["running"] = False
            status_label.config(cursor="arrow")
            return
        data = temps[frame]
        line.set_ydata(data)

        # Rebuild fill_between
        for coll in ax.collections:
            coll.remove()
        ax.fill_between(x, data, alpha=0.12, color=ACCENT)

        ax.set_title(
            f"1D Heat Diffusion  ·  step {frame}/{numTimes}  ·  max = {max(data):.5f}",
            fontsize=10, pad=10
        )
        if animation_state["paused"]:
            status_var.set(f"⏸  Paused at {frame}/{numTimes}  |  r = {r:.4f}")
        else:
            status_var.set(f"▶  step {frame}/{numTimes}  |  r = {r:.4f}")
        canvas.draw_idle()
        animation_state["after_id"] = canvas.get_tk_widget().after(20, update, frame + 1)


    status_var.set(f"▶  Running  |  r = {r:.4f}")
    update()


# ─── 2D simulation ────────────────────────────────────────────────────────────

def run_simulation_2D(fig, canvas, status_var, animation_state, status_label, initcond, alpha, Nx, Ny, numTimes, controls):
    animation_state["running"] = True
    status_label.config(cursor="hand2")
    if animation_state["after_id"] is not None:
        canvas.get_tk_widget().after_cancel(animation_state["after_id"])
        animation_state["after_id"] = None
    animation_state["paused"] = False

    r_x = compute_r(alpha, Nx)
    r_y = compute_r(alpha, Ny)
    if r_x >= 0.25 or r_y >= 0.25:
        status_var.set(f"⚠  Unstable: r_x={r_x:.3f}, r_y={r_y:.3f} — must be < 0.25")
        return

    X, Y, initial_temp = get_initial_condition_2D(initcond, Nx, Ny, controls)
    temps = solve_heat_2D(initial_temp, r_x, r_y, numTimes)

    fig.clear()
    ax = fig.add_subplot(1, 1, 1)

    vmin = 0
    vmax = max(t.max() for t in temps) or 1.0

    img = ax.imshow(
        temps[0], origin="lower", extent=[0, 1, 0, 1],
        aspect="auto", cmap="inferno", vmin=vmin, vmax=vmax
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cbar = fig.colorbar(img, ax=ax, label="Temperature", fraction=0.046, pad=0.04)
    cbar.ax.yaxis.label.set_color(TEXT_DIM)
    cbar.ax.tick_params(colors=TEXT_DIM)

    canvas.get_tk_widget().pack(fill="both", expand=True)

    def update(frame=0):
        if animation_state["paused"]:
            animation_state["after_id"] = canvas.get_tk_widget().after(50, update, frame)
            return 
        
        if frame >= len(temps):
            animation_state["after_id"] = None
            status_var.set(f"✓  Done — steps = {numTimes}")
            animation_state["running"] = False
            status_label.config(cursor="arrow")
            return
        img.set_data(temps[frame])
        ax.set_title(
            f"2D Heat Diffusion  ·  step {frame}/{numTimes}  ·  max = {temps[frame].max():.5f}",
            fontsize=10, pad=10
        )
        if animation_state["paused"]:
            status_var.set(f"⏸  Paused at {frame}/{numTimes}  |  r = {r:.4f}")
        else:
            status_var.set(f"▶  step {frame}/{numTimes}  |  r = {r:.4f}")
        canvas.draw_idle()
        animation_state["after_id"] = canvas.get_tk_widget().after(
            20, update, frame + 1
        )


    status_var.set(f"▶  Running  |  r_x={r_x:.3f}  r_y={r_y:.3f}")
    update()

# ─── Main window ──────────────────────────────────────────────────────────────

def create_window():
    root = tk.Tk()
    root.title("Heat Equation Simulator")
    root.configure(bg=BG)
    root.geometry("1180x720")
    root.minsize(900, 580)

    # ── Title bar ──
    title_bar = tk.Frame(root, bg=PANEL, height=46)
    title_bar.pack(fill=tk.X, side=tk.TOP)
    title_bar.pack_propagate(False)
    tk.Label(
        title_bar,
        text="  ∂u/∂t = α ∇²u   ·   HEAT EQUATION SIMULATOR",
        bg=PANEL, fg=ACCENT, font=("Arial", 13, "bold")
    ).pack(side=tk.LEFT, padx=16, pady=8)
    tk.Frame(title_bar, bg=BORDER, width=1).pack(side=tk.RIGHT, fill=tk.Y)

    # ── Status bar ──
    status_bar = tk.Frame(root, bg=SURFACE, height=26)
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    status_bar.pack_propagate(False)

    status_var = tk.StringVar(value="Ready")
    status_label = tk.Label(
        status_bar, textvariable=status_var,
        bg=SURFACE, fg=TEXT_DIM, font=("Arial", 16),
        anchor="w", padx=12, cursor = "arrow"
    )
    status_label.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # ── Main layout ──
    body = tk.Frame(root, bg=BG)
    body.pack(fill=tk.BOTH, expand=True)

    # Left sidebar with tabs
    sidebar = tk.Frame(body, bg=PANEL, width=230)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)
    tk.Frame(body, bg=BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)

    # Plot area
    plot_area = tk.Frame(body, bg=BG)
    plot_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Figure
    fig = Figure(figsize=(9, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=plot_area)
    canvas.draw_idle()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    # Welcome screen
    ax0 = fig.add_subplot(1, 1, 1)
    ax0.text(
        0.5, 0.56, "∂u/∂t = α ∇²u",
        ha="center", va="center", transform=ax0.transAxes,
        fontsize=26, color=ACCENT, fontfamily="monospace", alpha=0.85
    )
    ax0.text(
        0.5, 0.42, "Select a dimension, configure parameters,\nthen press  ▶  RUN SIMULATION",
        ha="center", va="center", transform=ax0.transAxes,
        fontsize=10, color=TEXT_DIM, fontfamily="monospace"
    )
    ax0.axis("off")
    canvas.draw_idle()

    # ── Dimension tab buttons ──
    tab_frame = tk.Frame(sidebar, bg=PANEL)
    tab_frame.pack(fill=tk.X)

    content_frame = tk.Frame(sidebar, bg=PANEL)
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Scrollable content
    scroll_canvas = tk.Canvas(content_frame, bg=PANEL, highlightthickness=0)
    scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    inner = tk.Frame(scroll_canvas, bg=PANEL)
    scroll_window = scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_configure(e):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        scroll_canvas.itemconfig(scroll_window, width=scroll_canvas.winfo_width())

    inner.bind("<Configure>", on_configure)
    scroll_canvas.bind("<Configure>", lambda e: scroll_canvas.itemconfig(scroll_window, width=e.width))

    # Mouse wheel scroll
    def _on_mousewheel(e):
        scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    active_dim = [None]
    tab_buttons = {}
    panels = {}
    animation_state = {"after_id": None, "paused": False, "running": False}

    def switch_dim(dim):
        if active_dim[0] == dim:
            return
        active_dim[0] = dim
        for d, tab in tab_buttons.items():
            tab.config(
                bg=ACCENT if d == dim else SURFACE,
                fg="white" if d == dim else TEXT_DIM
            )
        clear_frame(inner)
        if( dim == "1D"):
            panels[dim](inner, fig, canvas, animation_state, status_var, status_label, run_simulation_1D)
        elif(dim == "2D"):
            panels[dim](inner, fig, canvas, animation_state, status_var, status_label, run_simulation_2D)

    for dim, label in [("1D", "1D Rod"), ("2D", "2D Plate")]:
        tab = tk.Label(
            tab_frame,
            text=label,
            bg=SURFACE,
            fg=TEXT_DIM,
            font=("Arial", 11, "bold"),
            padx=12,
            pady=8,
            cursor="hand2"
        )

        tab.bind("<Button-1>", lambda e, d=dim: switch_dim(d))
        tab.pack(side=tk.LEFT, expand=True, fill=tk.X)
        tab_buttons[dim] = tab

    tk.Frame(tab_frame, bg=BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM)

    def toggle_pause(event = None):
        # print(animation_state["running"])
        # print(animation_state["paused"])
        if not animation_state["running"]:
            return
        
        animation_state["paused"] = not animation_state["paused"]

        if animation_state["paused"]:
            status_var.set("⏸  Paused (click to resume)")
        else:
            status_var.set("▶  Running")

    status_label.bind("<Button-1>", toggle_pause)

    panels["1D"] = create_panel_1D
    panels["2D"] = create_panel_2D

    switch_dim("1D")

    root.mainloop()
