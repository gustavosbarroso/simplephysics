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
L = 1.0
C = 1.0

q0 = 0.0
i0 = 0.0

V0 = 5.0
omega = 2.0

# ---------------------------
# CLASSIFICAÇÃO
# ---------------------------
def classify_regime():
    omega0 = 1 / np.sqrt(L * C)
    gamma = R / (2 * L)

    if abs(gamma - omega0) < 1e-3:
        return "Criticamente amortecido"
    elif gamma > omega0:
        return "Superamortecido"
    else:
        return "Subamortecido"

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t):
    q, i = r
    Vt = V0 * np.cos(omega * t)

    return np.array([
        i,
        (Vt/L) - (R/L)*i - (1/(L*C))*q
    ], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, N, r):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
    r = np.array(r, float)

    qp, ip = [r[0]], [r[1]]

    for k in range(N):
        t = tp[k]

        k1 = h * f(r, t)
        k2 = h * f(r + 0.5*k1, t + 0.5*h)
        k3 = h * f(r + 0.5*k2, t + 0.5*h)
        k4 = h * f(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        qp.append(r[0])
        ip.append(r[1])

    return tp, qp, ip

def solve(q0, i0):
    return RK4(f, 0, 20, 1000, [q0, i0])

# ---------------------------
# INICIAL
# ---------------------------
tp, q, i_vals = solve(q0, i0)
q = np.array(q)
i_vals = np.array(i_vals)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_circ, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(bottom=0.55)

# ---------------------------
# CIRCUITO
# ---------------------------
ax_circ.set_xlim(0, 10)
ax_circ.set_ylim(0, 6)
ax_circ.axis('off')
ax_circ.set_title("RLC com Fonte AC (cos)")

x0, x1 = 2, 8
y0, y1 = 1, 5

# fios
ax_circ.plot([x0, x1], [y0, y0], lw=2)
ax_circ.plot([x1, x1], [y0, y1], lw=2)
ax_circ.plot([x1, x0], [y1, y1], lw=2)
ax_circ.plot([x0, x0], [y1, y0], lw=2)

# resistor
xr0, xr1 = 4, 6
x_res = np.linspace(xr0, xr1, 9)
y_res = [(y0 + (0.3 if k%2 else 0) * (-1 if k%4==3 else 1)) for k in range(len(x_res))]
ax_circ.plot(x_res, y_res, lw=2.5)

# capacitor
yc0, yc1 = 2.2, 3.8
ax_circ.plot([x1, x1], [yc0, yc1], lw=4, color='white')
ax_circ.plot([x1-0.3, x1+0.3], [yc0, yc0], lw=2.5)
ax_circ.plot([x1-0.3, x1+0.3], [yc1, yc1], lw=2.5)

# indutor
xl0, xl1 = 4, 6
theta = np.linspace(0, 4*np.pi, 200)
ax_circ.plot([xl0, xl1], [y1, y1], lw=4, color='white')
x_ind = xl0 + (xl1-xl0)*(theta/(4*np.pi))
y_ind = y1 + 0.4*np.sin(theta)
ax_circ.plot(x_ind, y_ind, lw=2.5)

# fonte AC
xc = x0
yc = (y0 + y1)/2
circle = plt.Circle((xc, yc), 0.6, fill=False, lw=2)
ax_circ.add_patch(circle)

t_sin = np.linspace(-np.pi, np.pi, 100)
x_sin = xc + 0.5 * t_sin/np.pi
y_sin = yc + 0.3*np.sin(t_sin)
ax_circ.plot(x_sin, y_sin, lw=2)

ax_circ.text(xc-1.0, yc, "AC")

ax_circ.text(5, y0-0.8, "R", ha='center')
ax_circ.text(x1+0.6, (yc0+yc1)/2, "C", va='center')
ax_circ.text(5, y1+0.8, "L", ha='center')

# ---------------------------
# HUD
# ---------------------------
text_info = ax_circ.text(
    -0.35, 0.85, "",
    transform=ax_circ.transAxes,
    fontsize=8.5,
    verticalalignment='top',
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
)

# ---------------------------
# CAMINHO DOS ELÉTRONS
# ---------------------------
path_x = []
path_y = []

for x in np.linspace(x0, x1, 100):
    path_x.append(x)
    path_y.append(y0)

for y in np.linspace(y0, y1, 100):
    path_x.append(x1)
    path_y.append(y)

for x in np.linspace(x1, x0, 100):
    path_x.append(x)
    path_y.append(y1)

for y in np.linspace(y1, y0, 100):
    path_x.append(x0)
    path_y.append(y)

path_x = np.array(path_x)
path_y = np.array(path_y)
N_path = len(path_x)

# elétrons
n_electrons = 25
electron_pos = np.linspace(0, N_path-1, n_electrons)

electrons, = ax_circ.plot(
    path_x[electron_pos.astype(int)],
    path_y[electron_pos.astype(int)],
    'o',
    markersize=4
)

# ---------------------------
# GRÁFICO
# ---------------------------
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("Resposta do circuito")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("q(t), i(t)")

line_q, = ax_plot.plot([], [], label="q(t)")
line_i, = ax_plot.plot([], [], label="i(t)")
ax_plot.legend()

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    global electron_pos

    line_q.set_data(tp[:frame], q[:frame])
    line_i.set_data(tp[:frame], i_vals[:frame])

    if frame > 5:
        ymax = max(
            np.max(np.abs(q[:frame])),
            np.max(np.abs(i_vals[:frame])),
            1e-3
        )
        ax_plot.set_ylim(-1.2*ymax, 1.2*ymax)

    # HUD
    regime = classify_regime()
    text_info.set_text(
        f"R = {R:.2f} Ω\n"
        f"L = {L:.2f} H\n"
        f"C = {C:.2f} F\n\n"
        f"Regime: {regime}\n\n"
        f"q0 = {q0:.2f} C\n"
        f"i0 = {i0:.2f} A\n"
        f"q = {q[frame]:.2f} C\n"
        f"i = {i_vals[frame]:.2f} A\n"
        f"t = {tp[frame]:.2f} s"
    )

    # ELÉTRONS
    current = i_vals[frame]
    speed = 5 * current

    electron_pos = (electron_pos + speed) % N_path

    electrons.set_data(
        path_x[electron_pos.astype(int)],
        path_y[electron_pos.astype(int)]
    )

    return line_q, line_i, electrons

ani = FuncAnimation(fig, update, frames=len(q), interval=15)

# ---------------------------
# SLIDERS
# ---------------------------
ax_R = plt.axes([0.2, 0.45, 0.6, 0.03])
ax_L = plt.axes([0.2, 0.40, 0.6, 0.03])
ax_C = plt.axes([0.2, 0.35, 0.6, 0.03])
ax_V0 = plt.axes([0.2, 0.30, 0.6, 0.03])
ax_w = plt.axes([0.2, 0.25, 0.6, 0.03])
ax_q0 = plt.axes([0.2, 0.18, 0.6, 0.03])
ax_i0 = plt.axes([0.2, 0.13, 0.6, 0.03])

slider_R = Slider(ax_R, 'R (Ω)', 0.1, 10, valinit=R)
slider_L = Slider(ax_L, 'L (H)', 0.1, 5, valinit=L)
slider_C = Slider(ax_C, 'C (F)', 0.1, 5, valinit=C)
slider_V0 = Slider(ax_V0, 'V0 (V)', 0, 10, valinit=V0)
slider_w = Slider(ax_w, 'ω (rad/s)', 0.1, 10, valinit=omega)
slider_q0 = Slider(ax_q0, 'q0 (C)', -5, 5, valinit=q0)
slider_i0 = Slider(ax_i0, 'i0 (A)', -5, 5, valinit=i0)

def update_sliders(val):
    global R, L, C, V0, omega, q0, i0, tp, q, i_vals

    R = slider_R.val
    L = slider_L.val
    C = slider_C.val
    V0 = slider_V0.val
    omega = slider_w.val
    q0 = slider_q0.val
    i0 = slider_i0.val

    tp, q, i_vals = solve(q0, i0)
    q = np.array(q)
    i_vals = np.array(i_vals)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_R.on_changed(update_sliders)
slider_L.on_changed(update_sliders)
slider_C.on_changed(update_sliders)
slider_V0.on_changed(update_sliders)
slider_w.on_changed(update_sliders)
slider_q0.on_changed(update_sliders)
slider_i0.on_changed(update_sliders)

plt.show()
