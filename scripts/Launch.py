import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTES
# ---------------------------
g = 9.81  # m/s²

# ---------------------------
# PARÂMETROS INICIAIS
# ---------------------------
v0 = 20.0          # m/s
theta0_deg = 45.0  # graus
theta0 = np.deg2rad(theta0_deg)

k = 0.02           # arrasto
m = 1.0            # kg

# ---------------------------
# DINÂMICA
# ---------------------------
def f(r, t):
    x, y, vx, vy = r

    v = np.sqrt(vx**2 + vy**2)

    ax = -(k/m) * v * vx
    ay = -g - (k/m) * v * vy

    return np.array([vx, vy, ax, ay], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, N, r0):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)

    r = np.array(r0, float)

    x_list, y_list, vx_list, vy_list = [r[0]], [r[1]], [r[2]], [r[3]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t)
        k2 = h * f(r + 0.5*k1, t + 0.5*h)
        k3 = h * f(r + 0.5*k2, t + 0.5*h)
        k4 = h * f(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6

        x_list.append(r[0])
        y_list.append(r[1])
        vx_list.append(r[2])
        vy_list.append(r[3])

        if r[1] < 0:
            break

    return (tp[:len(x_list)],
            np.array(x_list),
            np.array(y_list),
            np.array(vx_list),
            np.array(vy_list))

# ---------------------------
# SOLVER
# ---------------------------
def solve(v0, theta0_rad, k):
    vx0 = v0 * np.cos(theta0_rad)
    vy0 = v0 * np.sin(theta0_rad)

    tp, x, y, vx, vy = RK4(f, 0, 10, 500, [0, 0, vx0, vy0])

    return tp, x, y, vx, vy

# ---------------------------
# INICIAL
# ---------------------------
tp, x, y, vx, vy = solve(v0, theta0, k)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(left=0.25, bottom=0.35)

# ---------------------------
# SISTEMA
# ---------------------------
ax_sys.set_xlim(0, 50)
ax_sys.set_ylim(0, 25)
ax_sys.set_title("Lançamento oblíquo")
ax_sys.set_xlabel("x [m]")
ax_sys.set_ylabel("y [m]")

traj_line, = ax_sys.plot([], [], lw=2)
point, = ax_sys.plot([], [], 'ro')

# ---------------------------
# GRÁFICOS TEMPORAIS
# ---------------------------
ax_plot.set_title("Velocidades e altura")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("valores")

line_y, = ax_plot.plot([], [], label="y(t) [m]")
line_vx, = ax_plot.plot([], [], label="vx(t) [m/s]")
line_vy, = ax_plot.plot([], [], label="vy(t) [m/s]")

ax_plot.legend()

# ---------------------------
# ANIMAÇÃO
# ---------------------------
def update(frame):
    i = frame

    traj_line.set_data(x[:i], y[:i])
    point.set_data([x[i]], [y[i]])

    line_y.set_data(tp[:i], y[:i])
    line_vx.set_data(tp[:i], vx[:i])
    line_vy.set_data(tp[:i], vy[:i])

    ax_plot.set_xlim(0, tp[-1])

    if i > 5:
        ymax = max(
            np.max(np.abs(vx[:i])),
            np.max(np.abs(vy[:i])),
            np.max(y[:i])
        )
        ax_plot.set_ylim(-ymax * 1.2, ymax * 1.2)

    return traj_line, point, line_y, line_vx, line_vy

ani = FuncAnimation(fig, update, frames=len(tp), interval=20, blit=False)

# ---------------------------
# SLIDERS
# ---------------------------
ax_v0 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_theta = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_k = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_m = plt.axes([0.25, 0.10, 0.65, 0.03])

slider_v0 = Slider(ax_v0, 'v0 [m/s]', 0, 50, valinit=v0)
slider_theta = Slider(ax_theta, 'θ0 [deg]', 0, 90, valinit=theta0_deg)
slider_k = Slider(ax_k, 'k [kg/m]', 0, 0.5, valinit=k)
slider_m = Slider(ax_m, 'm [kg]', 0.1, 5.0, valinit=m)

# ---------------------------
# UPDATE
# ---------------------------
def update_sliders(_):
    global v0, theta0, k, m
    global tp, x, y, vx, vy

    v0 = slider_v0.val
    theta0_deg = slider_theta.val
    theta0 = np.deg2rad(theta0_deg)
    k = slider_k.val
    m = slider_m.val

    tp, x, y, vx, vy = solve(v0, theta0, k)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_v0.on_changed(update_sliders)
slider_theta.on_changed(update_sliders)
slider_k.on_changed(update_sliders)
slider_m.on_changed(update_sliders)

plt.show()
