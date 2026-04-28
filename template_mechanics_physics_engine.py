import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ===========================
# PARÂMETROS (FONTE ÚNICA)
# ===========================
params = {
    "param1": 1.0,
    "param2": 0.5,
    "x0": 1.0,
    "v0": 0.0
}

# ===========================
# SISTEMA DINÂMICO
# ===========================
def f(r, t, params):
    x, v = r

    p1 = params["param1"]
    p2 = params["param2"]

    dx = v
    dv = -p1 * x - p2 * v

    return np.array([dx, dv], float)

# ===========================
# RK4 (GENÉRICO)
# ===========================
def RK4(f, a, b, N, r0, params):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
    r = np.array(r0, float)

    x_list, v_list = [r[0]], [r[1]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t, params)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h * f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        x_list.append(r[0])
        v_list.append(r[1])

    return tp, np.array(x_list), np.array(v_list)

# ===========================
# SOLVER CENTRAL
# ===========================
def solve(params):
    tp, x, v = RK4(
        f,
        0, 10, 500,
        [params["x0"], params["v0"]],
        params
    )

    return tp, x, v

# ===========================
# ESCALA DO SISTEMA
# ===========================
def update_axis():
    ax_sys.set_xlim(-2, 2)
    ax_sys.set_ylim(-2, 2)

# ===========================
# INICIALIZAÇÃO
# ===========================
tp, x, v = solve(params)

# ===========================
# FIGURA
# ===========================
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.35)

update_axis()

ax_sys.set_title("Sistema físico")

point, = ax_sys.plot([], [], 'o')

# ---------------------------
# GRÁFICO
# ---------------------------
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("Evolução temporal")

line_x, = ax_plot.plot([], [], label="x(t)")
line_v, = ax_plot.plot([], [], label="v(t)")
ax_plot.legend()

# ===========================
# UPDATE ANIMAÇÃO
# ===========================
def update(frame):
    i = frame

    point.set_data([x[i]], [0])

    line_x.set_data(tp[:i], x[:i])
    line_v.set_data(tp[:i], v[:i])

    if i > 10:
        ymin = min(np.min(x[:i]), np.min(v[:i]))
        ymax = max(np.max(x[:i]), np.max(v[:i]))
        margin = 0.2 * (ymax - ymin + 1e-6)
        ax_plot.set_ylim(ymin - margin, ymax + margin)

    return point, line_x, line_v

ani = FuncAnimation(fig, update, frames=len(tp), interval=20)

# ===========================
# SLIDERS
# ===========================
ax_p1 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_p2 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_x0 = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_v0 = plt.axes([0.25, 0.10, 0.65, 0.03])

slider_p1 = Slider(ax_p1, 'param1', 0.1, 10, valinit=params["param1"])
slider_p2 = Slider(ax_p2, 'param2', 0.0, 5, valinit=params["param2"])
slider_x0 = Slider(ax_x0, 'x0', -2, 2, valinit=params["x0"])
slider_v0 = Slider(ax_v0, 'v0', -5, 5, valinit=params["v0"])

# ===========================
# UPDATE SLIDERS
# ===========================
def update_sliders(_):
    params["param1"] = slider_p1.val
    params["param2"] = slider_p2.val
    params["x0"] = slider_x0.val
    params["v0"] = slider_v0.val

    global tp, x, v
    tp, x, v = solve(params)

    update_axis()

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_p1.on_changed(update_sliders)
slider_p2.on_changed(update_sliders)
slider_x0.on_changed(update_sliders)
slider_v0.on_changed(update_sliders)

plt.show()
