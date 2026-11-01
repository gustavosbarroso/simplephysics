
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import Circle

# ---------------------------
# PARÂMETROS
# ---------------------------
params = {
    "g": 9.81,
    "l0": 0.50,
    "m": 2.0,
    "k": 50.0,
    "theta0": 0.0,
    "omega0": 1,
    "x0": 0.3,
    "vx0": 0.4
}

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t, params):

    theta, omega, x, vx = r

    g = params["g"]
    l0 = params["l0"]
    m = params["m"]
    k = params["k"]

    ftheta = omega

    fomega = -(g/(l0+x))*np.sin(theta) - (
        2*omega*vx/(l0+x)
    )

    fx = vx

    fvx = (l0+x)*omega**2 - (k/m)*x + g*np.cos(theta)

    return np.array([ftheta, fomega, fx, fvx], float)


# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b_int, N, r, params):

    h = (b_int-a)/N
    tp = np.linspace(a, b_int, N+1)

    r = np.array(r, float)

    th = [r[0]]
    om = [r[1]]
    x = [r[2]]
    vx = [r[3]]

    for i in range(N):

        t = tp[i]

        k1 = h*f(r, t, params)
        k2 = h*f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h*f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h*f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        th.append(r[0])
        om.append(r[1])
        x.append(r[2])
        vx.append(r[3])

    return tp, np.array(th), np.array(om), np.array(x), np.array(vx)


# ---------------------------
# SOLVER
# ---------------------------
def solve(params):

    tp, th, om, x, vx = RK4(
        f, 0, 10, 300,
        [
            params["theta0"],
            params["omega0"],
            params["x0"],
            params["vx0"]
        ],
        params
    )

    return tp, th, om, x, vx


# ---------------------------
# ESCALA DA ANIMAÇÃO
# ---------------------------
def update_axis():

    R = np.max(params["l0"] + x)

    R = max(R, 0.5)

    margin = 1.2

    ax_sys.set_xlim(-margin*R, margin*R)
    ax_sys.set_ylim(-margin*R, 0.3*R)

    ax_sys.set_aspect('equal', adjustable='box')


# ---------------------------
# INICIAL
# ---------------------------
tp, th, om, x, vx = solve(params)


# ---------------------------
# FIGURA
# ---------------------------
fig = plt.figure(figsize=(13, 9))

plt.subplots_adjust(
    left=0.08,
    right=0.97,
    top=0.94,
    bottom=0.38,
    wspace=0.35,
    hspace=0.35
)

gs = fig.add_gridspec(
    2, 2,
    left=0.08,
    right=0.97,
    top=0.94,
    bottom=0.38,
    width_ratios=[1, 1.15]
)

ax_sys = fig.add_subplot(gs[:, 0])
ax_theta = fig.add_subplot(gs[0, 1])
ax_radial = fig.add_subplot(gs[1, 1])

update_axis()

ax_sys.set_aspect('equal')
ax_sys.set_title("Pêndulo elástico")
ax_sys.set_xlabel("x [m]")
ax_sys.set_ylabel("y [m]")
ax_sys.grid(True)


# ---------------------------
# ELEMENTOS DO SISTEMA
# ---------------------------

# Suporte
support, = ax_sys.plot(
    [-0.15, 0.15], [0, 0],
    color='black', lw=4
)

pivot_dot, = ax_sys.plot(
    [0], [0], 'ro', markersize=6
)

# Mola
spring, = ax_sys.plot(
    [], [], color='royalblue', lw=2
)

# Massa
mass = Circle(
    (0, 0),
    0.08,
    color='crimson',
    zorder=5
)

ax_sys.add_patch(mass)


# ---------------------------
# GRÁFICOS TEMPORAIS
# ---------------------------

ax_theta.set_xlim(0, tp[-1])
ax_theta.set_title("Movimento angular")
ax_theta.set_xlabel("Tempo [s]")
ax_theta.set_ylabel("θ [rad] / ω [rad/s]")
ax_theta.grid(True)

line_theta, = ax_theta.plot(
    [], [], label="θ(t)"
)

line_omega, = ax_theta.plot(
    [], [], label="ω(t)"
)

ax_theta.legend()


ax_radial.set_xlim(0, tp[-1])
ax_radial.set_title("Movimento radial")
ax_radial.set_xlabel("Tempo [s]")
ax_radial.set_ylabel("x [m] / vx [m/s]")
ax_radial.grid(True)

line_x, = ax_radial.plot(
    [], [], label="x(t)"
)

line_vx, = ax_radial.plot(
    [], [], label="vx(t)"
)

ax_radial.legend()


# ---------------------------
# ESCALA DOS GRÁFICOS
# ---------------------------
def update_plots_axis():

    ymin = min(np.min(th), np.min(om))
    ymax = max(np.max(th), np.max(om))

    margin = 0.1*(ymax-ymin+1e-6)

    ax_theta.set_ylim(
        ymin-margin,
        ymax+margin
    )

    ymin = min(np.min(x), np.min(vx))
    ymax = max(np.max(x), np.max(vx))

    margin = 0.1*(ymax-ymin+1e-6)

    ax_radial.set_ylim(
        ymin-margin,
        ymax+margin
    )


update_plots_axis()


# ---------------------------
# GEOMETRIA DA MOLA
# ---------------------------
def spring_coordinates(xm, ym, coils=12, amplitude=0.04):

    # Vetor do ponto de suspensão até a massa
    dx = xm
    dy = ym

    length = np.sqrt(dx**2 + dy**2)

    # Vetor perpendicular à mola
    px = -dy/length
    py = dx/length

    # Coordenadas ao longo da mola
    s = np.linspace(0, 1, 2*coils+1)

    # Zigue-zague
    offset = np.zeros(len(s))
    offset[1:-1:2] = amplitude
    offset[2:-1:2] = -amplitude

    xs = s*dx + offset*px
    ys = s*dy + offset*py

    return xs, ys


# ---------------------------
# UPDATE DA ANIMAÇÃO
# ---------------------------
def update(frame):

    i = frame

    # Comprimento instantâneo
    L = params["l0"] + x[i]

    # Posição da massa
    xm = L*np.sin(th[i])
    ym = -L*np.cos(th[i])

    # Coordenadas da mola
    xs, ys = spring_coordinates(
        xm, ym,
        coils=12,
        amplitude=min(0.04, 0.04*L)
    )

    spring.set_data(xs, ys)

    mass.center = (xm, ym)

    # Gráfico angular
    line_theta.set_data(
        tp[:i+1],
        th[:i+1]
    )

    line_omega.set_data(
        tp[:i+1],
        om[:i+1]
    )

    # Gráfico radial
    line_x.set_data(
        tp[:i+1],
        x[:i+1]
    )

    line_vx.set_data(
        tp[:i+1],
        vx[:i+1]
    )

    return (
        spring,
        mass,
        pivot_dot,
        line_theta,
        line_omega,
        line_x,
        line_vx
    )


ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    interval=20,
    blit=False,
    repeat=True
)


# ---------------------------
# SLIDERS
# ---------------------------

# Primeira coluna
ax_g = plt.axes([0.13, 0.30, 0.32, 0.025])
ax_l0 = plt.axes([0.13, 0.25, 0.32, 0.025])
ax_m = plt.axes([0.13, 0.20, 0.32, 0.025])
ax_k = plt.axes([0.13, 0.15, 0.32, 0.025])

# Segunda coluna
ax_theta0 = plt.axes([0.62, 0.30, 0.30, 0.025])
ax_omega0 = plt.axes([0.62, 0.25, 0.30, 0.025])
ax_x0 = plt.axes([0.62, 0.20, 0.30, 0.025])
ax_vx0 = plt.axes([0.62, 0.15, 0.30, 0.025])


slider_g = Slider(
    ax_g, 'g (m/s²)',
    9.0, 10.0,
    valinit=9.81
)

slider_l0 = Slider(
    ax_l0, 'l0 (m)',
    0.3, 1.0,
    valinit=0.5
)

slider_m = Slider(
    ax_m, 'm (kg)',
    3, 5.0,
    valinit=2.0
)

slider_k = Slider(
    ax_k, 'k (N/m)',
    50, 100,
    valinit=100
)

slider_theta0 = Slider(
    ax_theta0, 'θ0 (rad)',
    -np.pi/2, np.pi/2,
    valinit=params["theta0"]
)

slider_omega0 = Slider(
    ax_omega0, 'ω0 (rad/s)',
    -2, 2,
    valinit=params["omega0"]
)

slider_x0 = Slider(
    ax_x0, 'x0 (m)',
        0, 1,
    valinit=params["x0"]
)

slider_vx0 = Slider(
    ax_vx0, 'vx0 (m/s)',
    -0.5, 0.5,
    valinit=params["vx0"]
)


# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(_):

    params["g"] = slider_g.val
    params["l0"] = slider_l0.val
    params["m"] = slider_m.val
    params["k"] = slider_k.val

    params["theta0"] = slider_theta0.val
    params["omega0"] = slider_omega0.val

    params["x0"] = slider_x0.val
    params["vx0"] = slider_vx0.val

    global tp, th, om, x, vx

    tp, th, om, x, vx = solve(params)

    update_axis()
    update_plots_axis()

    # Limpa os gráficos anteriores
    line_theta.set_data([], [])
    line_omega.set_data([], [])
    line_x.set_data([], [])
    line_vx.set_data([], [])

    # Reinicia a animação
    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    update(0)

    fig.canvas.draw_idle()


slider_g.on_changed(update_sliders)
slider_l0.on_changed(update_sliders)
slider_m.on_changed(update_sliders)
slider_k.on_changed(update_sliders)

slider_theta0.on_changed(update_sliders)
slider_omega0.on_changed(update_sliders)
slider_x0.on_changed(update_sliders)
slider_vx0.on_changed(update_sliders)


# ---------------------------
# EXIBIÇÃO
# ---------------------------
plt.show()
