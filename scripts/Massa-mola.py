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

# posição do teto
y_top = 1.0

# ---------------------------
# SISTEMA
# m y'' + b y' + k(y - y_eq) = 0
# com gravidade embutida
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
    return RK4(f, 0, 10, 1000, [y0, v0])

# ---------------------------
# MOLA (vertical)
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
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(11, 5))
plt.subplots_adjust(left=0.25, bottom=0.30)

ax_sys.set_xlim(-0.5, 0.5)
ax_sys.set_ylim(-0.5, 1.2)
ax_sys.set_title("Oscilador massa–mola vertical")

# teto
ax_sys.plot([-0.3, 0.3], [y_top, y_top], color='black', lw=3)

# mola + massa
spring_line, = ax_sys.plot([], [], lw=2)
mass, = ax_sys.plot([], [], 'o', markersize=12)

# gráfico temporal
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_ylim(min(y), max(y))
ax_plot.set_title("y(t)")
ax_plot.set_xlabel("t")
ax_plot.set_ylabel("y")

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
    spring_line.set_data([0, 0], [y_top, y_top - y[0]])
    mass.set_data([0], [y_top - y[0]])
    return spring_line, mass

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    i = frame

    y_mass = y_top - y[i]

    # mola vertical
    xs, ys = spring(y_top, y_mass)
    spring_line.set_data(xs, ys)

    # massa
    mass.set_data([0], [y_mass])

    # gráfico
    line_y.set_data(tp[:i], y[:i])

    text_info.set_text(
        f"k = {k:.2f} (N/m)\n"
        f"b = {b:.2f}(s⁻¹)\n"
        f"m = {m:.2f} (kg)\n"
        f"g = {g:.2f} (m/s²)\n\n"
        f"y = {y[i]:.3f} (m)\n"
        f"v = {v[i]:.3f} (m/s)\n"
        f"t = {tp[i]:.2f} s"
    )

    return spring_line, mass, line_y, text_info

ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    init_func=init,
    interval=20,
    blit=False
)

# ---------------------------
# SLIDERS
# ---------------------------
ax_k = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_b = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_y0 = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_v0 = plt.axes([0.25, 0.05, 0.65, 0.03])

slider_k = Slider(ax_k, 'k(N/m)', 0.5, 20, valinit=k)
slider_b = Slider(ax_b, 'b(s⁻¹)', 0, 10, valinit=b)
slider_y0 = Slider(ax_y0, 'y0(m)', -0.5, 0.8, valinit=y0)
slider_v0 = Slider(ax_v0, 'v0(m/s)', -5, 5, valinit=v0)

def update_sliders(val):
    global k, b, y0, v0, tp, y, v

    k = slider_k.val
    b = slider_b.val
    y0 = slider_y0.val
    v0 = slider_v0.val

    tp, y, v = solve(y0, v0)

    ax_plot.set_ylim(min(y), max(y))

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_k.on_changed(update_sliders)
slider_b.on_changed(update_sliders)
slider_y0.on_changed(update_sliders)
slider_v0.on_changed(update_sliders)

plt.show()
