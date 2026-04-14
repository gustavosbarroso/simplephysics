import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle, Circle

# ---------------------------
# CONSTANTES
# ---------------------------
g = 9.81
L = 0.5

A = 0.3
w_drive = 10.0   # precisa ser alto para efeito Kapitza

# ---------------------------
# SISTEMA (KAPITZA)
# ---------------------------
def f(r, t):
    theta, omega = r

    # aceleração do suporte vertical
    ydd = -A * w_drive**2 * np.cos(w_drive * t)

    domega = -( (g + ydd) / L ) * np.sin(theta)

    return np.array([omega, domega], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b_int, N, r):
    h = (b_int - a) / N
    tp = np.linspace(a, b_int, N + 1)
    r = np.array(r, float)

    th, om = [r[0]], [r[1]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t)
        k2 = h * f(r + 0.5*k1, t + 0.5*h)
        k3 = h * f(r + 0.5*k2, t + 0.5*h)
        k4 = h * f(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        th.append(r[0])
        om.append(r[1])

    return tp, np.array(th), np.array(om)

# ---------------------------
# SOLVER
# ---------------------------
def solve(theta0, omega0):
    tp, th, om = RK4(f, 0, 20, 2500, [theta0, omega0])

    # movimento do pivô
    y_pivot = A * np.cos(w_drive * tp)

    return tp, th, om, y_pivot

# ---------------------------
# INICIAIS
# ---------------------------
theta0 = 0.3
omega0 = 0.0

tp, th, om, y_pivot = solve(theta0, omega0)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.35)

# ---------------------------
# SISTEMA VISUAL
# ---------------------------
ax_sys.set_xlim(-1.5, 1.5)
ax_sys.set_ylim(-1.5, 1.5)
ax_sys.set_aspect('equal')
ax_sys.set_title("Pêndulo de Kapitza")

# pivô móvel
pivot_dot, = ax_sys.plot([], [], 'ro')

# pêndulo
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
# ANIMAÇÃO
# ---------------------------
def update(frame):
    i = frame
    t = tp[i]

    # pivô oscilando verticalmente
    xp = 0.0
    yp = y_pivot[i]

    # pêndulo
    xm = xp + L * np.sin(th[i])
    ym = yp - L * np.cos(th[i])

    rod.set_data([xp, xm], [yp, ym])
    mass.center = (xm, ym)
    pivot_dot.set_data([xp], [yp])

    # gráficos
    line_theta.set_data(tp[:i], th[:i])
    line_omega.set_data(tp[:i], om[:i])

    # escala dinâmica
    if i > 10:
        ymin = min(np.min(th[:i]), np.min(om[:i]))
        ymax = max(np.max(th[:i]), np.max(om[:i]))
        margin = 0.2 * (ymax - ymin + 1e-6)

        ax_plot.set_ylim(ymin - margin, ymax + margin)

    return rod, mass, pivot_dot, line_theta, line_omega

ani = FuncAnimation(fig, update, frames=len(tp), interval=20, blit=False)

# ---------------------------
# SLIDERS
# ---------------------------
ax_A = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_w = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_theta0 = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_omega0 = plt.axes([0.25, 0.10, 0.65, 0.03])

slider_A = Slider(ax_A, 'A (m)', 0, 1.0, valinit=A)
slider_w = Slider(ax_w, 'ω_forçado (rad/s)', -15, 15, valinit=w_drive)
slider_theta0 = Slider(ax_theta0, 'θ₀', -np.pi, np.pi, valinit=theta0)
slider_omega0 = Slider(ax_omega0, 'ω₀', -15, 15, valinit=omega0)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(_):
    global A, w_drive, theta0, omega0
    global tp, th, om, y_pivot

    A = slider_A.val
    w_drive = slider_w.val
    theta0 = slider_theta0.val
    omega0 = slider_omega0.val

    tp, th, om, y_pivot = solve(theta0, omega0)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_A.on_changed(update_sliders)
slider_w.on_changed(update_sliders)
slider_theta0.on_changed(update_sliders)
slider_omega0.on_changed(update_sliders)

plt.show()
