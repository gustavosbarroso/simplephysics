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
L = 0.10

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t):
    theta, omega = r
    return np.array([omega, -(g / L) * np.sin(theta)], float)

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, N, r):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
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
    tp, th, om = RK4(f, 0, 10, 1000, [theta0, omega0])
    x = L * np.sin(th)
    y = -L * np.cos(th)
    return tp, th, om, x, y

# ---------------------------
# INICIAIS
# ---------------------------
theta0 = 1.0
omega0 = 0.0

tp, th, om, x, y = solve(theta0, omega0)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_pend, ax_plot) = plt.subplots(1, 2, figsize=(11,5))
plt.subplots_adjust(left=0.25, bottom=0.3)

# ---------------------------
# PÊNDULO (escala dinâmica)
# ---------------------------
ax_pend.set_aspect('equal')
ax_pend.set_title("Pêndulo")

def update_axes_pend():
    margem = 0.2 * L
    limite = L + margem
    ax_pend.set_xlim(-limite, limite)
    ax_pend.set_ylim(-limite, limite)

update_axes_pend()

line, = ax_pend.plot([], [], 'o-', lw=2)

# ---------------------------
# GRÁFICO (escala dinâmica)
# ---------------------------
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("Evolução temporal")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("θ(t), ω(t)")

line_th, = ax_plot.plot([], [], label="θ(t)")
line_om, = ax_plot.plot([], [], label="ω(t)")
ax_plot.legend()

# função de escala dinâmica do gráfico
def update_axes_plot(i):
    if i < 5:
        return

    ymin = min(np.min(th[:i]), np.min(om[:i]))
    ymax = max(np.max(th[:i]), np.max(om[:i]))

    if abs(ymax - ymin) < 1e-8:
        ymax += 1
        ymin -= 1

    margem = 0.2 * (ymax - ymin)
    ax_plot.set_ylim(ymin - margem, ymax + margem)

# ---------------------------
# HUD
# ---------------------------
text_info = fig.text(
    0.02, 0.75,
    "",
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

# ---------------------------
# INIT
# ---------------------------
def init():
    line.set_data([0, x[0]], [0, y[0]])
    return line,

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    i = frame

    # pêndulo
    line.set_data([0, x[i]], [0, y[i]])

    # gráfico
    line_th.set_data(tp[:i], th[:i])
    line_om.set_data(tp[:i], om[:i])

    update_axes_plot(i)  # 🔥 escala dinâmica

    # HUD
    texto = (
        f"L = {L:.2f} m\n"
        f"g = {g:.2f} m/s²\n\n"
        f"θ₀ = {theta0:.2f} rad\n"
        f"ω₀ = {omega0:.2f} rad/s\n\n"
        f"θ = {th[i]:.2f} rad\n"
        f"ω = {om[i]:.2f} rad/s\n\n"
        f"t = {tp[i]:.2f} s"
    )

    text_info.set_text(texto)

    return line, line_th, line_om, text_info

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
ax_g = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_L = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_theta0 = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_omega0 = plt.axes([0.25, 0.05, 0.65, 0.03])

slider_g = Slider(ax_g, 'g (m/s²)', 1, 20, valinit=g)
slider_L = Slider(ax_L, 'L (m)', 0.1, 5.0, valinit=L)
slider_theta0 = Slider(ax_theta0, 'θ₀', -np.pi, np.pi, valinit=theta0)
slider_omega0 = Slider(ax_omega0, 'ω₀', -10, 10, valinit=omega0)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global g, L, theta0, omega0
    global tp, th, om, x, y

    g = slider_g.val
    L = slider_L.val
    theta0 = slider_theta0.val
    omega0 = slider_omega0.val

    tp, th, om, x, y = solve(theta0, omega0)

    update_axes_pend()

    line.set_data([0, x[0]], [0, y[0]])

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_g.on_changed(update_sliders)
slider_L.on_changed(update_sliders)
slider_theta0.on_changed(update_sliders)
slider_omega0.on_changed(update_sliders)

plt.show()
