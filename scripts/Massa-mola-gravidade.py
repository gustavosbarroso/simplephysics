import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTES
# ---------------------------
k = 5.0
b = 0.5
m = 1.0
g = 9.81

y_top = 1.0

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t):
    y, v = r
    return np.array([
        v,
        -(k/m)*y - (b/m)*v + g
    ], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b_int, N, r):
    h = (b_int - a) / N
    tp = np.linspace(a, b_int, N + 1)
    r = np.array(r, float)

    y_list, v_list = [r[0]], [r[1]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t)
        k2 = h * f(r + 0.5*k1, t + 0.5*h)
        k3 = h * f(r + 0.5*k2, t + 0.5*h)
        k4 = h * f(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6

        y_list.append(r[0])
        v_list.append(r[1])

    return tp, np.array(y_list), np.array(v_list)

# ---------------------------
# SOLVER
# ---------------------------
def solve(y0, v0):
    return RK4(f, 0, 10, 500, [y0, v0])

# ---------------------------
# MOLAS
# ---------------------------
def spring(y_start, y_end, x=0, coils=25, amp=0.08):
    ys = np.linspace(y_start, y_end, 400)
    xs = amp * np.sin(np.linspace(0, coils * np.pi, 400))
    return x + xs, ys

# ---------------------------
# INICIAIS
# ---------------------------
y0 = 0.3
v0 = 0.0

tp, y, v = solve(y0, v0)

# ---------------------------
# ESCALA FÍSICA (CORREÇÃO PRINCIPAL)
# ---------------------------
def update_axis():
    global y

    y_mass = y_top - y

    y_min = np.min(y_mass)
    y_max = np.max(y_mass)

    span = y_max - y_min
    if span < 1e-6:
        span = 1.0

    margin = 0.25 * span

    ax_sys.set_xlim(-0.4, 0.4)
    ax_sys.set_ylim(y_min - margin, y_max + margin)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(11, 5))
plt.subplots_adjust(left=0.25, bottom=0.35)

ax_sys.set_title("Oscilador massa–mola vertical")

spring_line, = ax_sys.plot([], [], lw=2)
mass, = ax_sys.plot([], [], 'o', markersize=12)

ax_sys.plot([-0.3, 0.3], [y_top, y_top], color='black', lw=3)

# gráfico temporal
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("y(t) (em metros)")
ax_plot.set_xlabel("t (s)")
ax_plot.set_ylabel("y (m)")

line_y, = ax_plot.plot([], [], label="y(t)")
ax_plot.legend()

# HUD
text_info = fig.text(
    0.02, 0.60, "",
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# ---------------------------
# INIT
# ---------------------------
def init():
    update_axis()

    spring_line.set_data([0, 0], [y_top, y_top - y[0]])
    mass.set_data([0], [y_top - y[0]])

    return spring_line, mass

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    i = frame

    y_mass = y_top - y[i]

    xs, ys = spring(y_top, y_mass)
    spring_line.set_data(xs, ys)

    mass.set_data([0], [y_mass])

    line_y.set_data(tp[:i], y[:i])

    # escala temporal
    if i > 5:
        ymin = np.min(y[:i])
        ymax = np.max(y[:i])

        span = ymax - ymin
        if span < 1e-6:
            span = 1.0

        margin = 0.2 * span
        ax_plot.set_ylim(ymin - margin, ymax + margin)

    text_info.set_text(
        f"k = {k:.2f} N/m\n"
        f"b = {b:.2f} s⁻¹\n"
        f"g = {g:.2f} m/s²\n"
        f"m = {m:.2f} kg\n\n"
        f"y = {y[i]:.3f} m\n"
        f"v = {v[i]:.3f} m/s\n"
        f"t = {tp[i]:.2f} s"
    )

    return spring_line, mass, line_y, text_info

ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    init_func=init,
    interval=20,
    blit=False,
    cache_frame_data=False
)

# ---------------------------
# SLIDERS
# ---------------------------
ax_k = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_b = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_g = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_y0 = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_v0 = plt.axes([0.25, 0.05, 0.65, 0.03])

slider_k = Slider(ax_k, 'k (N/m)', 0.5, 20, valinit=k)
slider_b = Slider(ax_b, 'b (s⁻¹)', 0, 10, valinit=b)
slider_g = Slider(ax_g, 'g (m/s²)', 1, 20, valinit=g)
slider_y0 = Slider(ax_y0, 'y0 (m)', 0.1, 0.8, valinit=y0)
slider_v0 = Slider(ax_v0, 'v0 (m/s)', -5, 5, valinit=v0)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global k, b, g, y0, v0, tp, y, v

    k = slider_k.val
    b = slider_b.val
    g = slider_g.val
    y0 = slider_y0.val
    v0 = slider_v0.val

    tp, y, v = solve(y0, v0)

    update_axis()

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_k.on_changed(update_sliders)
slider_b.on_changed(update_sliders)
slider_g.on_changed(update_sliders)
slider_y0.on_changed(update_sliders)
slider_v0.on_changed(update_sliders)

plt.show()
