import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import Circle

# ---------------------------
# PARÂMETROS
# ---------------------------
params = {
    "g": 9.81,
    "L": 0.5,
    "A": 0.3,
    "w_drive": 10.0,
    "theta0": 0.3,
    "omega0": 0.0
}

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t, params):
    theta, omega = r

    g = params["g"]
    L = params["L"]
    A = params["A"]
    w = params["w_drive"]

    ydd = -A * w**2 * np.cos(w * t)
    domega = -((g + ydd) / L) * np.sin(theta)

    return np.array([omega, domega], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b_int, N, r, params):
    h = (b_int - a) / N
    tp = np.linspace(a, b_int, N + 1)
    r = np.array(r, float)

    th, om = [r[0]], [r[1]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t, params)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h * f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        th.append(r[0])
        om.append(r[1])

    return tp, np.array(th), np.array(om)

# ---------------------------
# SOLVER
# ---------------------------
def solve(params):
    tp, th, om = RK4(
        f, 0, 20, 1000,
        [params["theta0"], params["omega0"]],
        params
    )

    y_pivot = params["A"] * np.cos(params["w_drive"] * tp)

    return tp, th, om, y_pivot

# ---------------------------
# ESCALA
# ---------------------------
def update_axis():
    R = params["L"] + abs(params["A"])
    margin = 1.1

    ax_sys.set_xlim(-margin*R, margin*R)
    ax_sys.set_ylim(-margin*R, margin*R)

# ---------------------------
# INICIAL
# ---------------------------
tp, th, om, y_pivot = solve(params)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.48)

update_axis()

ax_sys.set_aspect('equal')
ax_sys.set_title("Pêndulo de Kapitza")

pivot_dot, = ax_sys.plot([], [], 'ro')
rod, = ax_sys.plot([], [], lw=2)
mass = Circle((0,0), 0.06)
ax_sys.add_patch(mass)

# ---------------------------
# GRÁFICO
# ---------------------------
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("Evolução temporal")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("θ [rad], ω [rad/s]")

line_theta, = ax_plot.plot([], [], label="θ(t)")
line_omega, = ax_plot.plot([], [], label="ω(t)")
ax_plot.legend()

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    i = frame

    xp = 0.0
    yp = y_pivot[i]

    L = params["L"]

    xm = xp + L * np.sin(th[i])
    ym = yp - L * np.cos(th[i])

    rod.set_data([xp, xm], [yp, ym])
    mass.center = (xm, ym)
    pivot_dot.set_data([xp], [yp])

    line_theta.set_data(tp[:i], th[:i])
    line_omega.set_data(tp[:i], om[:i])

    if i > 10:
        ymin = min(np.min(th[:i]), np.min(om[:i]))
        ymax = max(np.max(th[:i]), np.max(om[:i]))
        margin = 0.2 * (ymax - ymin + 1e-6)
        ax_plot.set_ylim(ymin - margin, ymax + margin)

    return rod, mass, pivot_dot, line_theta, line_omega

ani = FuncAnimation(fig, update, frames=len(tp), interval=20)

# ---------------------------
# SLIDERS
# ---------------------------
ax_g = plt.axes([0.25, 0.40, 0.65, 0.03])
ax_L = plt.axes([0.25, 0.35, 0.65, 0.03])
ax_A = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_w = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_theta0 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_omega0 = plt.axes([0.25, 0.15, 0.65, 0.03])

slider_g = Slider(ax_g, 'g (m/s²)', 0.0, 30.0, valinit=params["g"])
slider_L = Slider(ax_L, 'L (m)', 0.1, 3.0, valinit=params["L"])
slider_A = Slider(ax_A, 'A (m)', 0, 1.0, valinit=params["A"])
slider_w = Slider(ax_w, 'ω_forçado (rad/s)', -30, 30, valinit=params["w_drive"])
slider_theta0 = Slider(ax_theta0, 'θ₀ (rad)', -np.pi, np.pi, valinit=params["theta0"])
slider_omega0 = Slider(ax_omega0, 'ω₀ (rad/s)', -30, 30, valinit=params["omega0"])

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(_):
    params["g"] = slider_g.val
    params["L"] = slider_L.val
    params["A"] = slider_A.val
    params["w_drive"] = slider_w.val
    params["theta0"] = slider_theta0.val
    params["omega0"] = slider_omega0.val

    global tp, th, om, y_pivot
    tp, th, om, y_pivot = solve(params)

    update_axis()

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_g.on_changed(update_sliders)
slider_L.on_changed(update_sliders)
slider_A.on_changed(update_sliders)
slider_w.on_changed(update_sliders)
slider_theta0.on_changed(update_sliders)
slider_omega0.on_changed(update_sliders)

plt.show()
