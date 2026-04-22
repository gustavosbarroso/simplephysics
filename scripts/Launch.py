import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# PARAMS
# ---------------------------
params = {
    "g": 9.81,
    "v0": 20.0,
    "theta0_deg": 45.0,
    "k": 0.02,
    "m": 1.0,
    "speed": 3
}

# ---------------------------
# DINÂMICA COM ARRASTO
# ---------------------------
def f_drag(r, t, params):
    x, y, vx, vy = r

    g = params["g"]
    k = params["k"]
    m = params["m"]

    v = np.sqrt(vx**2 + vy**2)

    ax = -(k/m) * v * vx
    ay = -g - (k/m) * v * vy

    return np.array([vx, vy, ax, ay], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, N, r0, params):
    h = (b - a) / N
    t = a
    r = np.array(r0, float)

    tp = [t]
    x_list, y_list, vx_list, vy_list = [r[0]], [r[1]], [r[2]], [r[3]]

    for _ in range(N):
        k1 = h * f(r, t, params)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h * f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6
        t += h

        tp.append(t)
        x_list.append(r[0])
        y_list.append(r[1])
        vx_list.append(r[2])
        vy_list.append(r[3])

        if r[1] < 0:
            break

    return (np.array(tp),
            np.array(x_list),
            np.array(y_list),
            np.array(vx_list),
            np.array(vy_list))

# ---------------------------
# SOLUÇÃO COM ARRASTO
# ---------------------------
def solve_drag(params):
    v0 = params["v0"]
    theta = np.deg2rad(params["theta0_deg"])

    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    if abs(vx0) < 1e-12:
        vx0 = 0.0

    return RK4(f_drag, 0, 20, 600, [0, 0, vx0, vy0], params)

# ---------------------------
# SOLUÇÃO IDEAL
# ---------------------------
def solve_ideal(params):
    v0 = params["v0"]
    theta = np.deg2rad(params["theta0_deg"])
    g = params["g"]

    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    if abs(vx0) < 1e-12:
        vx0 = 0.0

    T = 2 * vy0 / g if vy0 > 0 else 5

    tp = np.linspace(0, T, 600)

    x = vx0 * tp
    y = vy0 * tp - 0.5 * g * tp**2

    vx = np.full_like(tp, vx0)
    vy = vy0 - g * tp

    idx = np.where(y >= 0)[0]

    return tp[idx], x[idx], y[idx], vx[idx], vy[idx]

# ---------------------------
# INICIAL
# ---------------------------
tp_d, x_d, y_d, vx_d, vy_d = solve_drag(params)
tp_i, x_i, y_i, vx_i, vy_i = solve_ideal(params)

n_frames = max(len(tp_d), len(tp_i))

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.35)

ax_sys.set_title("Trajetória")
ax_sys.set_xlabel("x [m]")
ax_sys.set_ylabel("y [m]")

traj_drag, = ax_sys.plot([], [], 'r-', label="Com arrasto")
traj_ideal, = ax_sys.plot([], [], 'b--', label="Sem arrasto")
point, = ax_sys.plot([], [], 'ro')

ax_sys.legend()

ax_plot.set_title("y(t)")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("y [m]")

line_y_drag, = ax_plot.plot([], [], 'r-', label="Com arrasto")
line_y_ideal, = ax_plot.plot([], [], 'b--', label="Sem arrasto")

ax_plot.legend()

# ---------------------------
# ANIMAÇÃO
# ---------------------------
def update(frame):
    speed = params["speed"]

    i = min(frame * speed, n_frames - 1)

    fator_d = len(tp_d) / n_frames
    fator_i = len(tp_i) / n_frames

    i_d = min(int(i * fator_d), len(tp_d)-1)
    i_i = min(int(i * fator_i), len(tp_i)-1)

    traj_drag.set_data(x_d[:i_d], y_d[:i_d])
    traj_ideal.set_data(x_i[:i_i], y_i[:i_i])

    point.set_data([x_d[i_d]], [y_d[i_d]])

    line_y_drag.set_data(tp_d[:i_d], y_d[:i_d])
    line_y_ideal.set_data(tp_i[:i_i], y_i[:i_i])

    ax_plot.set_xlim(0, max(tp_d[-1], tp_i[-1]))
    ymax = max(np.max(y_d), np.max(y_i))
    ax_plot.set_ylim(0, ymax*1.2)

    xmax = max(np.max(x_d), np.max(x_i))
    ax_sys.set_xlim(0, xmax*1.2 if xmax > 1e-10 else 1)
    ax_sys.set_ylim(0, ymax*1.2)

    return traj_drag, traj_ideal, point, line_y_drag, line_y_ideal

ani = FuncAnimation(fig, update, frames=n_frames, interval=8)

# ---------------------------
# SLIDERS
# ---------------------------
ax_v0 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_theta = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_k = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_m = plt.axes([0.25, 0.10, 0.65, 0.03])

slider_v0 = Slider(ax_v0, 'v0 [m/s]', 0, 50, valinit=params["v0"])
slider_theta = Slider(ax_theta, 'θ [°]', 0, 90, valinit=params["theta0_deg"])
slider_k = Slider(ax_k, 'k[kg/m]', 0, 0.1, valinit=params["k"])
slider_m = Slider(ax_m, 'm [kg]', 0.1, 5, valinit=params["m"])

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(_):
    global tp_d, x_d, y_d, vx_d, vy_d
    global tp_i, x_i, y_i, vx_i, vy_i
    global n_frames, ani

    params["v0"] = slider_v0.val
    params["theta0_deg"] = slider_theta.val
    params["k"] = slider_k.val
    params["m"] = slider_m.val

    tp_d, x_d, y_d, vx_d, vy_d = solve_drag(params)
    tp_i, x_i, y_i, vx_i, vy_i = solve_ideal(params)

    n_frames = max(len(tp_d), len(tp_i))

    ani.event_source.stop()
    ani = FuncAnimation(fig, update, frames=n_frames, interval=8)

    fig.canvas.draw_idle()

slider_v0.on_changed(update_sliders)
slider_theta.on_changed(update_sliders)
slider_k.on_changed(update_sliders)
slider_m.on_changed(update_sliders)

plt.show()
