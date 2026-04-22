import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle, Circle

# ===========================
# PARÂMETROS (FONTE ÚNICA)
# ===========================
params = {
    "g": 9.81,
    "m": 1.0,
    "M": 2.0,
    "l": 1.0,
    "A": 0.0,
    "w": 2.0,
    "theta0": 0.05
}

# ===========================
# SISTEMA DINÂMICO
# ===========================
def f(r, t, params):
    theta, omega, xpos, vel = r

    g = params["g"]
    m = params["m"]
    M = params["M"]
    l = params["l"]
    A = params["A"]
    w = params["w"]

    F = A * np.cos(w * t)

    A_mat = np.array([
        [l, -np.cos(theta)],
        [-m*l*np.cos(theta), (M + m)]
    ])

    b_vec = np.array([
        g * np.sin(theta),
        F - m*l*(omega**2)*np.sin(theta)
    ])

    a_theta, a_x = np.linalg.solve(A_mat, b_vec)

    return np.array([omega, a_theta, vel, a_x], float)

# ===========================
# RK4
# ===========================
def RK4(f, a, b, N, r, params):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
    r = np.array(r, float)

    theta, omega, x, v = [r[0]], [r[1]], [r[2]], [r[3]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t, params)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h * f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        theta.append(r[0])
        omega.append(r[1])
        x.append(r[2])
        v.append(r[3])

    return tp, np.array(theta), np.array(omega), np.array(x), np.array(v)

# ===========================
# SOLVER
# ===========================
def solve(params):
    tp, th, om, x, v = RK4(
        f, 0, 10, 1500,
        [params["theta0"], 0, 0, 0],
        params
    )

    l = params["l"]

    xb = x
    yb = np.zeros_like(x)

    xp = xb + l * np.sin(th)
    yp = yb + 0.3 + l * np.cos(th)

    return tp, th, om, x, v, xb, yb, xp, yp

# ===========================
# INICIAL
# ===========================
tp, th, om, x, v, xb, yb, xp, yp = solve(params)

# ===========================
# FIGURA
# ===========================
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.45)

ax_sys.set_xlim(-5, 5)
ax_sys.set_ylim(-1, 2.5)
ax_sys.set_aspect('equal')
ax_sys.set_title("Carrinho + Pêndulo Invertido")

cart_width = 0.6
cart_height = 0.3

cart = Rectangle((0,0), cart_width, cart_height, fc='black')
wheel1 = Circle((0,0), 0.1, fc='gray')
wheel2 = Circle((0,0), 0.1, fc='gray')

rod, = ax_sys.plot([], [], 'r-', lw=2)
mass = Circle((0,0), 0.1, fc='blue')

ax_sys.add_patch(cart)
ax_sys.add_patch(wheel1)
ax_sys.add_patch(wheel2)
ax_sys.add_patch(mass)

# ===========================
# GRÁFICO
# ===========================
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("Evolução temporal")
ax_plot.set_xlabel("t [s]")
ax_plot.set_ylabel("θ [rad], x [m], ω [rad/s]")

line_theta, = ax_plot.plot([], [], label="θ(t)")
line_x, = ax_plot.plot([], [], label="x(t)")
line_omega, = ax_plot.plot([], [], label="ω(t)")
ax_plot.legend()

# ===========================
# UPDATE ANIMAÇÃO
# ===========================
def update(frame):
    i = frame

    x_c = xb[i]
    y_c = 0

    cart.set_xy((x_c - cart_width/2, y_c))
    wheel1.center = (x_c - 0.2, y_c - 0.1)
    wheel2.center = (x_c + 0.2, y_c - 0.1)

    x_top = x_c
    y_top = y_c + cart_height

    l = params["l"]

    x_mass = x_top + l * np.sin(th[i])
    y_mass = y_top + l * np.cos(th[i])

    rod.set_data([x_top, x_mass], [y_top, y_mass])
    mass.center = (x_mass, y_mass)

    line_theta.set_data(tp[:i], th[:i])
    line_x.set_data(tp[:i], x[:i])
    line_omega.set_data(tp[:i], om[:i])

    if i > 10:
        ymin = min(np.min(th[:i]), np.min(x[:i]), np.min(om[:i]))
        ymax = max(np.max(th[:i]), np.max(x[:i]), np.max(om[:i]))

        if abs(ymax - ymin) < 1e-6:
            ymax += 1
            ymin -= 1

        margin = 0.2 * (ymax - ymin)
        ax_plot.set_ylim(ymin - margin, ymax + margin)

    return cart, wheel1, wheel2, rod, mass, line_theta, line_x, line_omega

ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    interval=20,
    blit=False
)

# ===========================
# SLIDERS (via params)
# ===========================
ax_A = plt.axes([0.25, 0.35, 0.65, 0.03])
ax_w = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_M = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_m = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_l = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_t0 = plt.axes([0.25, 0.10, 0.65, 0.03])

slider_A = Slider(ax_A, 'A [N]', 0, 30, valinit=params["A"])
slider_w = Slider(ax_w, 'ω [rad/s]', 0, 30, valinit=params["w"])
slider_M = Slider(ax_M, 'M [kg]', 0.5, 10, valinit=params["M"])
slider_m = Slider(ax_m, 'm [kg]', 0.1, 5, valinit=params["m"])
slider_l = Slider(ax_l, 'l [m]', 0.5, 3, valinit=params["l"])
slider_t0 = Slider(ax_t0, 'θ₀ [rad]', -np.pi, np.pi, valinit=params["theta0"])

# ===========================
# UPDATE SLIDERS
# ===========================
def update_sliders(_):
    global tp, th, om, x, v, xb, yb, xp, yp

    params["A"] = slider_A.val
    params["w"] = slider_w.val
    params["M"] = slider_M.val
    params["m"] = slider_m.val
    params["l"] = slider_l.val
    params["theta0"] = slider_t0.val

    tp, th, om, x, v, xb, yb, xp, yp = solve(params)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_A.on_changed(update_sliders)
slider_w.on_changed(update_sliders)
slider_M.on_changed(update_sliders)
slider_m.on_changed(update_sliders)
slider_l.on_changed(update_sliders)
slider_t0.on_changed(update_sliders)

plt.show()
