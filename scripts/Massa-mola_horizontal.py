import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import Rectangle


# ============================================================
# CONSTANTES
# ============================================================

k = 5.0
b = 0.5
m = 1.0

# posição da parede
x_left = 0.0

# posição de equilíbrio
x_eq = 1.0

# tamanho do bloco
block_size = 0.25


# ============================================================
# SISTEMA
#
# m x'' + b x' + k(x - x_eq) = 0
# ============================================================

def f(r, t):

    x, v = r

    return np.array([
        v,
        -(k / m) * (x - x_eq) - (b / m) * v
    ], float)


# ============================================================
# RK4
# ============================================================

def RK4(f, a, b_int, N, r):

    h = (b_int - a) / N

    tp = np.linspace(
        a,
        b_int,
        N + 1
    )

    r = np.array(r, float)

    x_list = [r[0]]
    v_list = [r[1]]

    for i in range(N):

        t = tp[i]

        k1 = h * f(r, t)

        k2 = h * f(
            r + 0.5 * k1,
            t + 0.5 * h
        )

        k3 = h * f(
            r + 0.5 * k2,
            t + 0.5 * h
        )

        k4 = h * f(
            r + k3,
            t + h
        )

        r = r + (
            k1
            + 2 * k2
            + 2 * k3
            + k4
        ) / 6

        x_list.append(r[0])
        v_list.append(r[1])

    return (
        tp,
        np.array(x_list),
        np.array(v_list)
    )


# ============================================================
# SOLVER
# ============================================================

def solve(x0, v0):

    return RK4(
        f,
        0,
        10,
        1000,
        [x0, v0]
    )


# ============================================================
# MOLA HORIZONTAL
# ============================================================

def spring(
    x_start,
    x_end,
    y=0,
    coils=12,
    amp=0.05
):

    xs = np.linspace(
        x_start,
        x_end,
        400
    )

    ys = amp * np.sin(
        np.linspace(
            0,
            coils * np.pi,
            400
        )
    )

    return xs, y + ys


# ============================================================
# CONDIÇÕES INICIAIS
# ============================================================

x0 = 1.3
v0 = 0.0

tp, x, v = solve(
    x0,
    v0
)


# ============================================================
# FIGURA
# ============================================================

fig, (
    ax_sys,
    ax_plot
) = plt.subplots(
    1,
    2,
    figsize=(11, 5)
)

plt.subplots_adjust(
    left=0.22,
    bottom=0.30,
    wspace=0.35
)


# ============================================================
# SISTEMA MASSA-MOLA
# ============================================================

ax_sys.set_xlim(
    -0.2,
    2.0
)

ax_sys.set_ylim(
    -0.3,
    0.6
)

ax_sys.set_aspect(
    'equal'
)

ax_sys.set_title(
    "Oscilador massa–mola amortecido"
)


# ------------------------------------------------------------
# PAREDE
# ------------------------------------------------------------

ax_sys.plot(
    [x_left, x_left],
    [0, 0.5],
    color='black',
    lw=3
)


# ------------------------------------------------------------
# CHÃO
# ------------------------------------------------------------

ax_sys.plot(
    [-0.1, 2.0],
    [0, 0],
    color='black',
    lw=2
)


# ------------------------------------------------------------
# MOLA
# ------------------------------------------------------------

spring_line, = ax_sys.plot(
    [],
    [],
    lw=2
)


# ------------------------------------------------------------
# BLOCO
# ------------------------------------------------------------

block = Rectangle(
    (
        x[0] - block_size / 2,
        0
    ),
    block_size,
    block_size,
    linewidth=1.5
)

ax_sys.add_patch(
    block
)


# ============================================================
# GRÁFICO x(t) E v(t)
# ============================================================

ax_plot.set_xlim(
    0,
    tp[-1]
)

ax_plot.set_title(
    "Evolução temporal"
)

ax_plot.set_xlabel(
    "t [s]"
)

ax_plot.set_ylabel(
    "x(t), v(t)"
)


# ------------------------------------------------------------
# CURVAS
# ------------------------------------------------------------

line_x, = ax_plot.plot(
    [],
    [],
    label="x(t) - m"
)

line_v, = ax_plot.plot(
    [],
    [],
    label="v(t) - m/s"
)

ax_plot.legend()


# ============================================================
# ESCALA DINÂMICA DO GRÁFICO
# ============================================================

def update_axes_plot(i):

    if i < 5:
        return

    # considera x e v no mesmo eixo
    ymin = min(
        np.min(x[:i]),
        np.min(v[:i])
    )

    ymax = max(
        np.max(x[:i]),
        np.max(v[:i])
    )

    # evita intervalo nulo
    if abs(ymax - ymin) < 1e-8:
        ymax += 1
        ymin -= 1

    # margem de 20%
    margem = 0.2 * (
        ymax - ymin
    )

    ax_plot.set_ylim(
        ymin - margem,
        ymax + margem
    )


# ============================================================
# HUD
# ============================================================

text_info = fig.text(
    0.02,
    0.60,
    "",
    fontsize=10,
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=0.8
    )
)


# ============================================================
# INIT
# ============================================================

def init():

    # face esquerda do bloco
    block_left = (
        x[0]
        - block_size / 2
    )

    # mola
    xs, ys = spring(
        x_left,
        block_left,
        y=block_size / 2
    )

    spring_line.set_data(
        xs,
        ys
    )

    # bloco
    block.set_xy(
        (
            x[0] - block_size / 2,
            0
        )
    )

    # gráficos
    line_x.set_data(
        [],
        []
    )

    line_v.set_data(
        [],
        []
    )

    return (
        spring_line,
        block,
        line_x,
        line_v
    )


# ============================================================
# UPDATE
# ============================================================

def update(frame):

    i = frame

    x_mass = x[i]

    # --------------------------------------------------------
    # BLOCO
    # --------------------------------------------------------

    block.set_xy(
        (
            x_mass - block_size / 2,
            0
        )
    )

    # --------------------------------------------------------
    # MOLA
    # --------------------------------------------------------

    block_left = (
        x_mass
        - block_size / 2
    )

    xs, ys = spring(
        x_left,
        block_left,
        y=block_size / 2
    )

    spring_line.set_data(
        xs,
        ys
    )

    # --------------------------------------------------------
    # x(t)
    # --------------------------------------------------------

    line_x.set_data(
        tp[:i],
        x[:i]
    )

    # --------------------------------------------------------
    # v(t)
    # --------------------------------------------------------

    line_v.set_data(
        tp[:i],
        v[:i]
    )

    # --------------------------------------------------------
    # ESCALA DINÂMICA
    # --------------------------------------------------------

    update_axes_plot(i)

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    text_info.set_text(
        f"k = {k:.2f} N/m\n"
        f"b = {b:.2f} kg/s\n"
        f"m = {m:.2f} kg\n\n"
        f"x = {x[i]:.3f} m\n"
        f"v = {v[i]:.3f} m/s\n"
        f"t = {tp[i]:.2f} s"
    )

    return (
        spring_line,
        block,
        line_x,
        line_v,
        text_info
    )


# ============================================================
# ANIMAÇÃO
# ============================================================

ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    init_func=init,
    interval=20,
    blit=False
)


# ============================================================
# SLIDERS
# ============================================================

ax_k = plt.axes([
    0.25,
    0.20,
    0.65,
    0.03
])

ax_b = plt.axes([
    0.25,
    0.15,
    0.65,
    0.03
])

ax_x0 = plt.axes([
    0.25,
    0.10,
    0.65,
    0.03
])

ax_v0 = plt.axes([
    0.25,
    0.05,
    0.65,
    0.03
])


slider_k = Slider(
    ax_k,
    'k (N/m)',
    0.5,
    20,
    valinit=k
)

slider_b = Slider(
    ax_b,
    'b (kg/s)',
    0,
    10,
    valinit=b
)

slider_x0 = Slider(
    ax_x0,
    'x₀ (m)',
    0.3,
    1.8,
    valinit=x0
)

slider_v0 = Slider(
    ax_v0,
    'v₀ (m/s)',
    -5,
    5,
    valinit=v0
)


# ============================================================
# ATUALIZAÇÃO DOS SLIDERS
# ============================================================

def update_sliders(val):

    global k, b
    global x0, v0
    global tp, x, v

    k = slider_k.val
    b = slider_b.val

    x0 = slider_x0.val
    v0 = slider_v0.val

    tp, x, v = solve(
        x0,
        v0
    )

    # reinicia animação
    ani.event_source.stop()

    ani.frame_seq = (
        ani.new_frame_seq()
    )

    ani.event_source.start()

    fig.canvas.draw_idle()


# ============================================================
# CONEXÃO DOS SLIDERS
# ============================================================

slider_k.on_changed(
    update_sliders
)

slider_b.on_changed(
    update_sliders
)

slider_x0.on_changed(
    update_sliders
)

slider_v0.on_changed(
    update_sliders
)


plt.show()
