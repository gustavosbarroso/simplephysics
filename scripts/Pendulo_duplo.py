import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTES
# ---------------------------
g = 9.81
L1 = 1.0
L2 = 1.0
m1 = 1.0
m2 = 1.0

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t):
    theta1, omega1, theta2, omega2 = r

    delta = theta2 - theta1

    den1 = (m1 + m2)*L1 - m2*L1*np.cos(delta)**2

    a1 = (
        m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
        + m2*g*np.sin(theta2)*np.cos(delta)
        + m2*L2*omega2**2*np.sin(delta)
        - (m1 + m2)*g*np.sin(theta1)
    ) / den1

    den2 = (L2/L1)*den1

    a2 = (
        -m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
        + (m1 + m2)*g*np.sin(theta1)*np.cos(delta)
        - (m1 + m2)*L1*omega1**2*np.sin(delta)
        - (m1 + m2)*g*np.sin(theta2)
    ) / den2

    return np.array([omega1, a1, omega2, a2], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, N, r):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
    r = np.array(r, float)

    th1, om1 = [r[0]], [r[1]]
    th2, om2 = [r[2]], [r[3]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t)
        k2 = h * f(r + 0.5*k1, t + 0.5*h)
        k3 = h * f(r + 0.5*k2, t + 0.5*h)
        k4 = h * f(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        th1.append(r[0])
        om1.append(r[1])
        th2.append(r[2])
        om2.append(r[3])

    return tp, np.array(th1), np.array(om1), np.array(th2), np.array(om2)

# ---------------------------
# SOLVER
# ---------------------------
def solve(theta1_0, omega1_0, theta2_0, omega2_0):
    tp, th1, om1, th2, om2 = RK4(
        f, 0, 10, 500,
        [theta1_0, omega1_0, theta2_0, omega2_0]
    )

    x1 = L1 * np.sin(th1)
    y1 = -L1 * np.cos(th1)

    x2 = x1 + L2 * np.sin(th2)
    y2 = y1 - L2 * np.cos(th2)

    return tp, th1, om1, th2, om2, x1, y1, x2, y2

# ---------------------------
# INICIAIS
# ---------------------------
theta1_0 = 1.0
theta2_0 = 1.0

tp, th1, om1, th2, om2, x1, y1, x2, y2 = solve(theta1_0, 0, theta2_0, 0)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_pend, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.4)

# Pêndulo
ax_pend.set_xlim(-3, 3)
ax_pend.set_ylim(-3, 3)
ax_pend.set_aspect('equal')
ax_pend.set_title("Pêndulo Duplo")

line, = ax_pend.plot([], [], 'o-', lw=2)

# ---------------------------
# GRÁFICO (ESCALA DINÂMICA)
# ---------------------------
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_ylim(-1, 1)

ax_plot.set_title("Evolução temporal")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("θ(rad) e ω(rad/s)")

line_th1, = ax_plot.plot([], [], label="θ1(t)")
line_om1, = ax_plot.plot([], [], label="ω1(t)")
line_th2, = ax_plot.plot([], [], label="θ2(t)")
line_om2, = ax_plot.plot([], [], label="ω2(t)")

ax_plot.legend()

# ---------------------------
# HUD
# ---------------------------
text_info = fig.text(
    0.02, 0.55,
    "",
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# ---------------------------
# INIT
# ---------------------------
def init():
    line.set_data([0, x1[0], x2[0]], [0, y1[0], y2[0]])
    return line,

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    i = frame

    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])

    line_th1.set_data(tp[:i], th1[:i])
    line_om1.set_data(tp[:i], om1[:i])
    line_th2.set_data(tp[:i], th2[:i])
    line_om2.set_data(tp[:i], om2[:i])

    # ---------------------------
    # ESCALA DINÂMICA
    # ---------------------------
    if i > 5:
        data_min = min(
            np.min(th1[:i]),
            np.min(th2[:i]),
            np.min(om1[:i]),
            np.min(om2[:i])
        )

        data_max = max(
            np.max(th1[:i]),
            np.max(th2[:i]),
            np.max(om1[:i]),
            np.max(om2[:i])
        )

        if abs(data_max - data_min) < 1e-6:
            data_min -= 1
            data_max += 1

        margin = 0.2 * (data_max - data_min)

        ax_plot.set_ylim(
            data_min - margin,
            data_max + margin
        )

    text_info.set_text(
        f"m1 = {m1:.2f} kg\n"
        f"m2 = {m2:.2f} kg\n"
        f"L1 = {L1:.2f} m\n"
        f"L2 = {L2:.2f} m\n"
        f"g = {g:.2f} m/s²\n\n"
        f"θ1₀ = {theta1_0:.2f} rad\n"
        f"θ2₀ = {theta2_0:.2f} rad\n\n"
        f"θ1 = {th1[i]:.2f} rad\n"
        f"ω1 = {om1[i]:.2f} rad/s\n"
        f"θ2 = {th2[i]:.2f} rad\n"
        f"ω2 = {om2[i]:.2f} rad/s\n\n"
        f"t = {tp[i]:.2f} s"
    )

    return line, line_th1, line_om1, line_th2, line_om2, text_info

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
ax_g = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_L1 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_L2 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_m1 = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_m2 = plt.axes([0.25, 0.10, 0.65, 0.03])
ax_t1 = plt.axes([0.25, 0.05, 0.65, 0.03])
ax_t2 = plt.axes([0.25, 0.00, 0.65, 0.03])

slider_g = Slider(ax_g, 'g(m/s²)', 1, 20, valinit=g)
slider_L1 = Slider(ax_L1, 'L1(m)', 0.5, 2.0, valinit=L1)
slider_L2 = Slider(ax_L2, 'L2(m)', 0.5, 2.0, valinit=L2)
slider_m1 = Slider(ax_m1, 'm1(kg)', 0.1, 5.0, valinit=m1)
slider_m2 = Slider(ax_m2, 'm2(kg)', 0.1, 5.0, valinit=m2)
slider_t1 = Slider(ax_t1, 'θ1₀(rad)', -np.pi, np.pi, valinit=theta1_0)
slider_t2 = Slider(ax_t2, 'θ2₀(rad)', -np.pi, np.pi, valinit=theta2_0)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global g, L1, L2, m1, m2, theta1_0, theta2_0
    global tp, th1, om1, th2, om2, x1, y1, x2, y2

    g = slider_g.val
    L1 = slider_L1.val
    L2 = slider_L2.val
    m1 = slider_m1.val
    m2 = slider_m2.val
    theta1_0 = slider_t1.val
    theta2_0 = slider_t2.val

    tp, th1, om1, th2, om2, x1, y1, x2, y2 = solve(theta1_0, 0, theta2_0, 0)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_g.on_changed(update_sliders)
slider_L1.on_changed(update_sliders)
slider_L2.on_changed(update_sliders)
slider_m1.on_changed(update_sliders)
slider_m2.on_changed(update_sliders)
slider_t1.on_changed(update_sliders)
slider_t2.on_changed(update_sliders)

plt.show()
