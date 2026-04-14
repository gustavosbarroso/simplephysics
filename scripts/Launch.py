import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.ticker import ScalarFormatter

# ---------------------------
# CONSTANTE
# ---------------------------
g = 9.81  # m/s²

# ---------------------------
# PARÂMETROS INICIAIS
# ---------------------------
v0 = 20.0
theta0_deg = 45.0
theta0 = np.deg2rad(theta0_deg)

# ---------------------------
# SOLUÇÃO ANALÍTICA
# ---------------------------
def solve(v0, theta):
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)

    # CORREÇÃO DE PONTO FLUTUANTE
    if abs(vx0) < 1e-12:
        vx0 = 0.0

    if abs(vy0) < 1e-12:
        vy0 = 0.0

    # tempo de voo
    if vy0 == 0:
        T = 5
    else:
        T = 2 * vy0 / g

    tp = np.linspace(0, T, 500)

    x = vx0 * tp
    y = vy0 * tp - 0.5 * g * tp**2

    vx = np.full_like(tp, vx0)
    vy = vy0 - g * tp

    return tp, x, y, vx, vy

# ---------------------------
# INICIAL
# ---------------------------
tp, x, y, vx, vy = solve(v0, theta0)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.35)

# ---------------------------
# SISTEMA
# ---------------------------
ax_sys.set_title("Lançamento oblíquo")
ax_sys.set_xlabel("x [m]")
ax_sys.set_ylabel("y [m]")

# remover notação científica feia
ax_sys.xaxis.set_major_formatter(ScalarFormatter())
ax_sys.ticklabel_format(style='plain', axis='x')

traj_line, = ax_sys.plot([], [], lw=2)
point, = ax_sys.plot([], [], 'ro')

# ---------------------------
# GRÁFICO
# ---------------------------
ax_plot.set_title("y(t), vx(t), vy(t)")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("Valores (m e m/s)")

line_y,  = ax_plot.plot([], [], label="y(t) [m]")
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
        ax_plot.set_ylim(-ymax*1.2, ymax*1.2)

    # ajuste automático do sistema
    xmax = max(x)
    ymax_sys = max(y)

    if xmax < 1e-10:
        ax_sys.set_xlim(-1, 1)  # lançamento vertical
    else:
        ax_sys.set_xlim(0, xmax*1.2)

    ax_sys.set_ylim(0, ymax_sys*1.2 if ymax_sys > 0 else 1)

    return traj_line, point, line_y, line_vx, line_vy

ani = FuncAnimation(fig, update, frames=range(0, len(tp), 3), interval=10)

# ---------------------------
# SLIDERS
# ---------------------------
ax_v0 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_theta = plt.axes([0.25, 0.20, 0.65, 0.03])

slider_v0 = Slider(ax_v0, 'v0 [m/s]', 0, 50, valinit=v0)
slider_theta = Slider(ax_theta, 'θ0 [°]', 0, 90, valinit=theta0_deg)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(_):
    global v0, theta0
    global tp, x, y, vx, vy

    v0 = slider_v0.val
    theta0 = np.deg2rad(slider_theta.val)

    tp, x, y, vx, vy = solve(v0, theta0)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_v0.on_changed(update_sliders)
slider_theta.on_changed(update_sliders)

plt.show()
