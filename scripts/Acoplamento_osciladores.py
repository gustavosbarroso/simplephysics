import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider


# ============================================================
# PARÂMETROS INICIAIS
# ============================================================

m = 1.0
k = 2.0
kc = 1.0

x1_0 = 1.0
x2_0 = -1.0

v1_0 = 0.0
v2_0 = 0.0


# ============================================================
# TEMPO
# ============================================================

t_max = 20.0
N = 400


# ============================================================
# EQUAÇÕES DIFERENCIAIS
# ============================================================

def f(r, t):

    x1, v1, x2, v2 = r

    a1 = (-k*x1 + kc*(x2 - x1)) / m
    a2 = (-k*x2 + kc*(x1 - x2)) / m

    return np.array([
        v1,
        a1,
        v2,
        a2
    ], float)


# ============================================================
# RK4
# ============================================================

def RK4(f, a, b, N, r):

    h = (b - a) / N

    tp = np.linspace(a, b, N + 1)

    r = np.array(r, float)

    x1 = [r[0]]
    v1 = [r[1]]

    x2 = [r[2]]
    v2 = [r[3]]

    for i in range(N):

        t = tp[i]

        k1 = h * f(r, t)

        k2 = h * f(r + 0.5*k1,t + 0.5*h)

        k3 = h * f(r + 0.5*k2,t + 0.5*h)

        k4 = h * f(r + k3,t + h)

        r = r + (k1+ 2*k2+ 2*k3+ k4) / 6

        x1.append(r[0])
        v1.append(r[1])

        x2.append(r[2])
        v2.append(r[3])

    return (tp,np.array(x1),np.array(v1),np.array(x2), np.array(v2))


# ============================================================
# SOLVER
# ============================================================

def solve():

    r0 = [x1_0,v1_0,x2_0,v2_0]

    return RK4(f,0,t_max,N,r0)


# ============================================================
# PRIMEIRA SIMULAÇÃO
# ============================================================

tp, x1, v1, x2, v2 = solve()


# ============================================================
# ENERGIA
# ============================================================

def calcular_energia():

    Ec = 0.5 * m * (
        v1**2 + v2**2
    )

    Ep = (
        0.5 * k * (
            x1**2 + x2**2
        )
        +
        0.5 * kc * (
            x2 - x1
        )**2
    )

    return Ec + Ep


E = calcular_energia()


# ============================================================
# IDENTIFICAÇÃO DO MODO
# ============================================================

def identificar_modo():

    if abs(x1_0 - x2_0) < 1e-2:

        return "Modo simétrico"

    elif abs(x1_0 + x2_0) < 1e-2:

        return "Modo antissimétrico"

    else:

        return "Batimento"


modo = identificar_modo()


# ============================================================
# FIGURA
# ============================================================

fig, (ax_sistema, ax_grafico) = plt.subplots(
    1,
    2,
    figsize=(11, 5),
    gridspec_kw={
        'width_ratios': [1.15, 0.90]
    }
)

plt.subplots_adjust(
    left=0.23,
    bottom=0.38,
    right=0.95,
    wspace=0.35
)


# ============================================================
# SISTEMA FÍSICO
# ============================================================

L = 5

ax_sistema.set_title(
    "Osciladores Acoplados"
)

ax_sistema.set_xlabel(
    "x (m)"
)

ax_sistema.set_yticks([])

ax_sistema.set_xlim(
    -L,
    L
)

ax_sistema.set_ylim(
    -1,
    1
)

ax_sistema.grid(
    alpha=0.3
)


# ============================================================
# PAREDES
# ============================================================

ax_sistema.plot(
    [-L, -L],
    [-1, 1],
    'k',
    lw=3
)

ax_sistema.plot(
    [L, L],
    [-1, 1],
    'k',
    lw=3
)


# ============================================================
# ELEMENTOS ANIMADOS
# ============================================================

mola_esquerda, = ax_sistema.plot(
    [],
    [],
    'g--',
    lw=2
)

mola_central, = ax_sistema.plot(
    [],
    [],
    'g--',
    lw=2
)

mola_direita, = ax_sistema.plot(
    [],
    [],
    'g--',
    lw=2
)

massa1, = ax_sistema.plot(
    [],
    [],
    'ro',
    markersize=12
)

massa2, = ax_sistema.plot(
    [],
    [],
    'bo',
    markersize=12
)


# ============================================================
# DESENHO DAS MOLAS
# ============================================================

def desenhar_mola(
    xa,
    xb,
    n=12,
    amplitude=0.08
):

    xs = np.linspace(
        xa,
        xb,
        n + 1
    )

    ys = np.zeros(
        n + 1
    )

    for j in range(1, n):

        if j % 2 == 1:
            ys[j] = amplitude

        else:
            ys[j] = -amplitude

    return xs, ys


# ============================================================
# GRÁFICO x(t)
# ============================================================

ax_grafico.set_xlim(
    0,
    tp[-1]
)

ax_grafico.set_title(
    "Posições ao longo do tempo"
)

ax_grafico.set_xlabel(
    "t (s)"
)

ax_grafico.set_ylabel(
    "x (m)"
)

line_x1, = ax_grafico.plot(
    [],
    [],
    'r-',
    label="x₁ (m)"
)

line_x2, = ax_grafico.plot(
    [],
    [],
    'b-',
    label="x₂ (m)"
)

ponto_x1, = ax_grafico.plot(
    [],
    [],
    'ro'
)

ponto_x2, = ax_grafico.plot(
    [],
    [],
    'bo'
)

ax_grafico.grid(
    alpha=0.3
)

ax_grafico.legend()


# ============================================================
# ESCALA DINÂMICA DO GRÁFICO
# ============================================================

def update_axes_plot(i):

    if i < 5:
        return

    ymin = min(
        np.min(x1[:i]),
        np.min(x2[:i])
    )

    ymax = max(
        np.max(x1[:i]),
        np.max(x2[:i])
    )

    if abs(ymax - ymin) < 1e-8:

        ymax += 1
        ymin -= 1

    margem = 0.2 * (
        ymax - ymin
    )

    ax_grafico.set_ylim(
        ymin - margem,
        ymax + margem
    )


# ============================================================
# HUD
# ============================================================

text_info = fig.text(
    0.02,
    0.72,
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

    X1 = -1 + x1[0]
    X2 = 1 + x2[0]


    # ----------------------------------------
    # MOLA ESQUERDA
    # ----------------------------------------

    xs, ys = desenhar_mola(
        -L,
        X1
    )

    mola_esquerda.set_data(
        xs,
        ys
    )


    # ----------------------------------------
    # MOLA CENTRAL
    # ----------------------------------------

    xs, ys = desenhar_mola(
        X1,
        X2
    )

    mola_central.set_data(
        xs,
        ys
    )


    # ----------------------------------------
    # MOLA DIREITA
    # ----------------------------------------

    xs, ys = desenhar_mola(
        X2,
        L
    )

    mola_direita.set_data(
        xs,
        ys
    )


    # ----------------------------------------
    # MASSAS
    # ----------------------------------------

    massa1.set_data(
        [X1],
        [0]
    )

    massa2.set_data(
        [X2],
        [0]
    )


    return (
        mola_esquerda,
        mola_central,
        mola_direita,
        massa1,
        massa2
    )


# ============================================================
# UPDATE DA ANIMAÇÃO
# ============================================================

def update(frame):

    i = frame


    # ========================================================
    # POSIÇÕES
    # ========================================================

    X1 = -1 + x1[i]
    X2 = 1 + x2[i]


    # ========================================================
    # MOLA ESQUERDA
    # ========================================================

    xs, ys = desenhar_mola(
        -L,
        X1
    )

    mola_esquerda.set_data(
        xs,
        ys
    )


    # ========================================================
    # MOLA CENTRAL
    # ========================================================

    xs, ys = desenhar_mola(
        X1,
        X2
    )

    mola_central.set_data(
        xs,
        ys
    )


    # ========================================================
    # MOLA DIREITA
    # ========================================================

    xs, ys = desenhar_mola(
        X2,
        L
    )

    mola_direita.set_data(
        xs,
        ys
    )


    # ========================================================
    # MASSAS
    # ========================================================

    massa1.set_data(
        [X1],
        [0]
    )

    massa2.set_data(
        [X2],
        [0]
    )


    # ========================================================
    # GRÁFICO
    # ========================================================

    line_x1.set_data(
        tp[:i],
        x1[:i]
    )

    line_x2.set_data(
        tp[:i],
        x2[:i]
    )

    ponto_x1.set_data(
        [tp[i]],
        [x1[i]]
    )

    ponto_x2.set_data(
        [tp[i]],
        [x2[i]]
    )

    update_axes_plot(i)


    # ========================================================
    # HUD
    # ========================================================

    texto = (
        f"m = {m:.2f} kg\n"
        f"k = {k:.2f} N/m\n"
        f"kc = {kc:.2f} N/m\n\n"

        f"x₁ = {x1[i]:.3f} m\n"
        f"x₂ = {x2[i]:.3f} m\n\n"

        f"v₁ = {v1[i]:.3f} m/s\n"
        f"v₂ = {v2[i]:.3f} m/s\n\n"

        f"E = {E[i]:.3f} J\n\n"

        f"t = {tp[i]:.2f} s\n"
        f"{modo}"
    )

    text_info.set_text(
        texto
    )


    return (
        mola_esquerda,
        mola_central,
        mola_direita,
        massa1,
        massa2,
        line_x1,
        line_x2,
        ponto_x1,
        ponto_x2,
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
    blit=False,
    repeat=True
)


# ============================================================
# SLIDERS
# ============================================================

ax_m = plt.axes(
    [0.25, 0.25, 0.65, 0.03]
)

ax_k = plt.axes(
    [0.25, 0.20, 0.65, 0.03]
)

ax_kc = plt.axes(
    [0.25, 0.15, 0.65, 0.03]
)

ax_x1 = plt.axes(
    [0.25, 0.10, 0.65, 0.03]
)

ax_x2 = plt.axes(
    [0.25, 0.05, 0.65, 0.03]
)


# ============================================================
# SLIDER m
# ============================================================

slider_m = Slider(
    ax_m,
    'm (kg)',
    0.5,
    5.0,
    valinit=m,
    valstep=0.1
)


# ============================================================
# SLIDER k
# ============================================================

slider_k = Slider(
    ax_k,
    'k (N/m)',
    0.5,
    10.0,
    valinit=k,
    valstep=0.1
)


# ============================================================
# SLIDER kc
# ============================================================

slider_kc = Slider(
    ax_kc,
    'kc (N/m)',
    0.1,
    10.0,
    valinit=kc,
    valstep=0.1
)


# ============================================================
# SLIDER x1
# ============================================================

slider_x1 = Slider(
    ax_x1,
    'x₁₀ (m)',
    -2.0,
    2.0,
    valinit=x1_0,
    valstep=0.1
)


# ============================================================
# SLIDER x2
# ============================================================

slider_x2 = Slider(
    ax_x2,
    'x₂₀ (m)',
    -2.0,
    2.0,
    valinit=x2_0,
    valstep=0.1
)


# ============================================================
# ATUALIZAÇÃO DOS SLIDERS
# ============================================================

def update_sliders(val):

    global m, k, kc
    global x1_0, x2_0

    global tp, x1, v1
    global x2, v2

    global E, modo


    # --------------------------------------------------------
    # NOVOS PARÂMETROS
    # --------------------------------------------------------

    m = slider_m.val
    k = slider_k.val
    kc = slider_kc.val

    x1_0 = slider_x1.val
    x2_0 = slider_x2.val


    # --------------------------------------------------------
    # NOVA SOLUÇÃO
    # --------------------------------------------------------

    tp, x1, v1, x2, v2 = solve()


    # --------------------------------------------------------
    # NOVA ENERGIA
    # --------------------------------------------------------

    E = calcular_energia()


    # --------------------------------------------------------
    # NOVO MODO
    # --------------------------------------------------------

    modo = identificar_modo()


    # --------------------------------------------------------
    # EIXO DO TEMPO
    # --------------------------------------------------------

    ax_grafico.set_xlim(
        0,
        tp[-1]
    )


    # --------------------------------------------------------
    # REINICIA ANIMAÇÃO
    # --------------------------------------------------------

    ani.event_source.stop()

    ani.frame_seq = ani.new_frame_seq()

    ani.event_source.start()


    fig.canvas.draw_idle()


# ============================================================
# CONECTA OS SLIDERS
# ============================================================

slider_m.on_changed(
    update_sliders
)

slider_k.on_changed(
    update_sliders
)

slider_kc.on_changed(
    update_sliders
)

slider_x1.on_changed(
    update_sliders
)

slider_x2.on_changed(
    update_sliders
)


# ============================================================
# MOSTRA
# ============================================================

plt.show()
