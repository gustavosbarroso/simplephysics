import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# PARÂMETROS
# ---------------------------
R = 2.0
C = 1.0

# ---------------------------
# SISTEMA RC
# ---------------------------
def f(r, t):
    q = r[0]
    dqdt = -(1/(R*C)) * q
    return np.array([dqdt], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, N, r):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
    r = np.array(r, float)

    q_list = [r[0]]

    for k in range(N):
        t = tp[k]

        k1 = h * f(r, t)
        k2 = h * f(r + 0.5*k1, t + 0.5*h)
        k3 = h * f(r + 0.5*k2, t + 0.5*h)
        k4 = h * f(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6
        q_list.append(r[0])

    q_list = np.array(q_list)
    i_list = -(1/(R*C)) * q_list

    return tp, q_list, i_list

def solve(q0):
    return RK4(f, 0, 10, 500, [q0])

# ---------------------------
# INICIAIS
# ---------------------------
q0 = 1.0
tp, q, i_vals = solve(q0)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_circ, ax_plot) = plt.subplots(1, 2, figsize=(11,5))
plt.subplots_adjust(bottom=0.35)

# ---------------------------
# CIRCUITO
# ---------------------------
ax_circ.set_xlim(0, 10)
ax_circ.set_ylim(0, 6)
ax_circ.axis('off')
ax_circ.set_title("Circuito RC com elétrons")

x0, x1 = 2, 8
y0, y1 = 2, 4

# fios
ax_circ.plot([x0, x1], [y0, y0], lw=2)
ax_circ.plot([x1, x1], [y0, y1], lw=2)
ax_circ.plot([x1, x0], [y1, y1], lw=2)
ax_circ.plot([x0, x0], [y1, y0], lw=2)

# resistor
xr = np.linspace(4, 6, 9)
yr = y0 + 0.3*np.array([(-1)**k for k in range(len(xr))])
ax_circ.plot(xr, yr, lw=2.5)
ax_circ.text(5, y0-0.8, "R", ha='center')

# capacitor
ax_circ.plot([x1, x1], [2.3, 3.7], lw=4, color='white')
ax_circ.plot([x1-0.3, x1+0.3], [2.3, 2.3], lw=2.5)
ax_circ.plot([x1-0.3, x1+0.3], [3.7, 3.7], lw=2.5)
ax_circ.text(x1+0.6, 3.0, "C", va='center')

# ---------------------------
# ELÉTRONS
# ---------------------------
num_e = 40
electron_pos = np.linspace(0, 1, num_e)
electrons, = ax_circ.plot([], [], 'ro', ms=3)

def loop_path(s):
    if s < 0.25:
        return x0 + (x1-x0)*(s/0.25), y0
    elif s < 0.5:
        return x1, y0 + (y1-y0)*((s-0.25)/0.25)
    elif s < 0.75:
        return x1 - (x1-x0)*((s-0.5)/0.25), y1
    else:
        return x0, y1 - (y1-y0)*((s-0.75)/0.25)

# ---------------------------
# GRÁFICO
# ---------------------------
ax_plot.set_xlim(0, tp[-1])

ymin = min(np.min(q), np.min(i_vals))
ymax = max(np.max(q), np.max(i_vals))
ax_plot.set_ylim(ymin, ymax)

ax_plot.set_title("Carga e corrente (RC)")
ax_plot.set_xlabel("t (s)")
ax_plot.set_ylabel("q(t) [C], i(t) [A]")

line_q, = ax_plot.plot([], [], label="q(t)")
line_i, = ax_plot.plot([], [], label="i(t)")
ax_plot.legend()

# ---------------------------
# TEXTO
# ---------------------------
text_info = fig.text(
    0.02, 0.65, "",
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# ---------------------------
# ANIMAÇÃO
# ---------------------------
def update(frame):
    global electron_pos

    i_inst = i_vals[frame]

    speed = 0.02 * i_inst
    electron_pos = (electron_pos + speed) % 1

    xs, ys = [], []
    for s in electron_pos:
        x, y = loop_path(s)
        xs.append(x)
        ys.append(y)

    electrons.set_data(xs, ys)

    line_q.set_data(tp[:frame], q[:frame])
    line_i.set_data(tp[:frame], i_vals[:frame])

    text_info.set_text(
        f"R = {R:.2f} Ω\n"
        f"C = {C:.2f} F\n\n"
        f"q = {q[frame]:.3f} C\n"
        f"i = {i_vals[frame]:.3f} A\n"
        f"t = {tp[frame]:.2f} s"
    )

    return electrons, line_q, line_i

ani = FuncAnimation(fig, update, frames=len(q), interval=20, blit=False)

# ---------------------------
# SLIDERS
# ---------------------------
ax_R = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_C = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_q0 = plt.axes([0.2, 0.10, 0.6, 0.03])

slider_R = Slider(ax_R, 'R (Ω)', 0.1, 10, valinit=R)
slider_C = Slider(ax_C, 'C (F)', 0.1, 5, valinit=C)
slider_q0 = Slider(ax_q0, 'q0 (C)', -2, 2, valinit=q0)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global R, C, q0, tp, q, i_vals, electron_pos

    R = slider_R.val
    C = slider_C.val
    q0 = slider_q0.val

    tp, q, i_vals = solve(q0)

    # reset elétrons
    electron_pos = np.linspace(0, 1, num_e)

    # ajuste de escala
    ax_plot.set_xlim(0, tp[-1])

    ymin = min(np.min(q), np.min(i_vals))
    ymax = max(np.max(q), np.max(i_vals))
    margem = 0.2 * (ymax - ymin + 1e-6)

    ax_plot.set_ylim(ymin - margem, ymax + margem)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_R.on_changed(update_sliders)
slider_C.on_changed(update_sliders)
slider_q0.on_changed(update_sliders)

plt.show()
