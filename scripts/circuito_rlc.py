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

# ---------------------------
# SISTEMA RLC
# ---------------------------
def f(r, t):
    q, i = r
    return np.array([
        i,
        -(R/L)*i - (1/(L*C))*q
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
    return RK4(f, 0, 15, 1500, [q0, i0])

# ---------------------------
# CLASSIFICAÇÃO
# ---------------------------
def classify_regime():
    delta = (R/L)**2 - 4*(1/(L*C))
    if abs(delta) < 1e-3:
        return "Criticamente amortecido"
    elif delta > 0:
        return "Superamortecido"
    else:
        return "Subamortecido"

# ---------------------------
# CONDIÇÕES INICIAIS
# ---------------------------
q0, i0 = 1.0, 0.0
tp, q, i_vals = solve(q0, i0)

q = np.array(q)
i_vals = np.array(i_vals)

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
ax_circ.set_title("Circuito RLC")

x0, x1 = 2, 8
y0, y1 = 1, 5

# fio completo
ax_circ.plot([x0, x1], [y0, y0], lw=2, color='black')
ax_circ.plot([x1, x1], [y0, y1], lw=2, color='black')
ax_circ.plot([x1, x0], [y1, y1], lw=2, color='black')
ax_circ.plot([x0, x0], [y1, y0], lw=2, color='black')

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

# labels
ax_circ.text(5, y0-0.8, "R", ha='center')
ax_circ.text(x1+0.6, (yc0+yc1)/2, "C", va='center')
ax_circ.text(5, y1+0.8, "L", ha='center')

# ---------------------------
# ELÉTRONS
# ---------------------------
num_e = 30
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
# GRÁFICO (SI PURO)
# ---------------------------
ax_plot.set_xlim(0, tp[-1])

# limites automáticos melhores
ymin = min(np.min(q), np.min(i_vals))
ymax = max(np.max(q), np.max(i_vals))
ax_plot.set_ylim(ymin, ymax)

ax_plot.set_title("Evolução temporal")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("q(t) [C], i(t) [A]")

line_q, = ax_plot.plot([], [], label="q(t) [C]")
line_i, = ax_plot.plot([], [], label="i(t) [A]")
ax_plot.legend()

# ---------------------------
# TEXTO INFO
# ---------------------------
text_info = fig.text(
    0.02, 0.65, "",
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    global electron_pos

    i_inst = i_vals[frame]
    speed = 0.01 * i_inst
    electron_pos = (electron_pos + speed) % 1

    xs, ys = [], []
    for s in electron_pos:
        x, y = loop_path(s)
        xs.append(x)
        ys.append(y)

    electrons.set_data(xs, ys)

    line_q.set_data(tp[:frame], q[:frame])
    line_i.set_data(tp[:frame], i_vals[:frame])

    regime = classify_regime()

    texto = (
        f"R = {R:.2f} Ω\n"
        f"L = {L:.2f} H\n"
        f"C = {C:.2f} F\n\n"
        f"Regime: {regime}\n\n"
        f"q = {q[frame]:.2f} C\n"
        f"i = {i_vals[frame]:.2f} A\n"
        f"t = {tp[frame]:.2f} s"
    )

    text_info.set_text(texto)

    return electrons, line_q, line_i

ani = FuncAnimation(fig, update, frames=len(q),
                    interval=20, blit=False)

# ---------------------------
# SLIDERS
# ---------------------------
ax_R = plt.axes([0.2, 0.25, 0.6, 0.03])
ax_L = plt.axes([0.2, 0.2, 0.6, 0.03])
ax_C = plt.axes([0.2, 0.15, 0.6, 0.03])

slider_R = Slider(ax_R, 'R (Ω)', 0.1, 10, valinit=R)
slider_L = Slider(ax_L, 'L (H)', 0.1, 5, valinit=L)
slider_C = Slider(ax_C, 'C (F)', 0.1, 5, valinit=C)

def update_sliders(val):
    global R, L, C, tp, q, i_vals

    R = slider_R.val
    L = slider_L.val
    C = slider_C.val

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

plt.show()
