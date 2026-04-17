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
w_drive = 2.0

cart_w = 0.4
cart_h = 0.2
wheel_r = 0.07
ground_y = -0.5

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t):
    theta, omega = r

    dtheta = omega
    domega = (
        -(g / L) * np.sin(theta)
        + (A / L) * np.cos(theta) * np.cos(w_drive * t)
    )

    return np.array([dtheta, domega], float)

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

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6

        th.append(r[0])
        om.append(r[1])

    return tp, np.array(th), np.array(om)

# ---------------------------
# SOLVER
# ---------------------------
def solve(theta0, omega0):
    tp, th, om = RK4(f, 0, 20, 1000, [theta0, omega0])
    x_cart = A * np.cos(w_drive * tp)
    return tp, th, om, x_cart

# ---------------------------
# ESCALA FÍSICA
# ---------------------------
def update_axis():
    x_max = A + L

    y_top = ground_y + wheel_r + cart_h
    y_min = y_top - L
    y_max = y_top + L

    ax_sys.set_xlim(-x_max, x_max)
    ax_sys.set_ylim(y_min, y_max)

# ---------------------------
# INICIAIS
# ---------------------------
theta0 = 0.5
omega0 = 0.0

tp, th, om, x_cart = solve(theta0, omega0)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))

# ===========================
# LAYOUT CORRIGIDO (IMPORTANTE)
# ===========================
slider_height = 0.03
slider_spacing = 0.015
start_y = 0.40

plt.subplots_adjust(left=0.25, bottom=0.55)

update_axis()

ax_sys.set_aspect('equal')
ax_sys.set_title("Cart + Pêndulo")

ax_sys.plot([-10, 10], [ground_y, ground_y], lw=3)

# carrinho
cart = Rectangle((0,0), cart_w, cart_h)
wheel1 = Circle((0,0), wheel_r)
wheel2 = Circle((0,0), wheel_r)

ax_sys.add_patch(cart)
ax_sys.add_patch(wheel1)
ax_sys.add_patch(wheel2)

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
# INIT
# ---------------------------
def init():
    return cart, wheel1, wheel2, rod, mass

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    i = frame

    xc = x_cart[i]
    yc = ground_y

    cart.set_xy((xc - cart_w/2, yc + wheel_r))
    wheel1.center = (xc - cart_w/4, yc)
    wheel2.center = (xc + cart_w/4, yc)

    x_top = xc
    y_top = yc + wheel_r + cart_h

    x_mass = x_top + L * np.sin(th[i])
    y_mass = y_top - L * np.cos(th[i])

    rod.set_data([x_top, x_mass], [y_top, y_mass])
    mass.center = (x_mass, y_mass)

    line_theta.set_data(tp[:i], th[:i])
    line_omega.set_data(tp[:i], om[:i])

    if i > 10:
        ymin = min(np.min(th[:i]), np.min(om[:i]))
        ymax = max(np.max(th[:i]), np.max(om[:i]))

        if abs(ymax - ymin) < 1e-6:
            ymax += 1
            ymin -= 1

        margin = 0.2 * (ymax - ymin)
        ax_plot.set_ylim(ymin - margin, ymax + margin)

    return cart, wheel1, wheel2, rod, mass, line_theta, line_omega

ani = FuncAnimation(fig, update, frames=len(tp), init_func=init, interval=20)

# ---------------------------
# SLIDERS (ORGANIZADOS)
# ---------------------------
ax_L = plt.axes([0.25, start_y, 0.65, slider_height])
ax_A = plt.axes([0.25, start_y - 1*(slider_height + slider_spacing), 0.65, slider_height])
ax_w = plt.axes([0.25, start_y - 2*(slider_height + slider_spacing), 0.65, slider_height])
ax_theta0 = plt.axes([0.25, start_y - 3*(slider_height + slider_spacing), 0.65, slider_height])
ax_omega0 = plt.axes([0.25, start_y - 4*(slider_height + slider_spacing), 0.65, slider_height])

slider_L = Slider(ax_L, 'L(m)', 0.1, 3.0, valinit=L)
slider_A = Slider(ax_A, 'A(m)', 0, 1.0, valinit=A)
slider_w = Slider(ax_w, 'ω(rad/s)', 0.1, 10, valinit=w_drive)
slider_theta0 = Slider(ax_theta0, 'θ₀(rad)', -np.pi, np.pi, valinit=theta0)
slider_omega0 = Slider(ax_omega0, 'ω₀(rad/s)', -5, 5, valinit=omega0)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(_):
    global L, A, w_drive, theta0, omega0
    global tp, th, om, x_cart

    L = slider_L.val
    A = slider_A.val
    w_drive = slider_w.val
    theta0 = slider_theta0.val
    omega0 = slider_omega0.val

    tp, th, om, x_cart = solve(theta0, omega0)

    update_axis()

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_L.on_changed(update_sliders)
slider_A.on_changed(update_sliders)
slider_w.on_changed(update_sliders)
slider_theta0.on_changed(update_sliders)
slider_omega0.on_changed(update_sliders)

plt.show()
