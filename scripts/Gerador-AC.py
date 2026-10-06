# ---------------------------
# Imports
# ---------------------------
import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle


# ============================================================
# TENSÃO INDUZIDA (DDP)
# ============================================================

def ddp(N, A, B, w, t):
    return N * A * B * np.sin(w * t)


# ============================================================
# CORRENTE INDUZIDA
# ============================================================

def I(ddp, R):

    if R == 0:
        return np.zeros_like(ddp)

    return ddp / R


# ============================================================
# PARÂMETROS INICIAIS
# ============================================================

t = np.linspace(0, 10, 1000)

A = 2.0
B = 0.5
w = 10
N = 100
R = 10


# ============================================================
# SIMULAÇÃO INICIAL
# ============================================================

ddp_resultante = ddp(
    N,
    A,
    B,
    w,
    t
)

I_induzida = I(
    ddp_resultante,
    R
)


# ============================================================
# FIGURA
# ============================================================

fig = plt.figure(figsize=(15, 8))

gs = fig.add_gridspec(
    2,
    5,
    height_ratios=[5, 2],
    width_ratios=[4, 1, 4, 1, 4]
)


# ============================================================
# GERADOR
# ============================================================

ax = fig.add_subplot(gs[0, 0:2])

ax.set_xlim(-3, 3)
ax.set_ylim(-2.5, 2.5)

ax.set_aspect("equal")
ax.set_title("Gerador AC")

ax.set_xticks([])
ax.set_yticks([])


# ============================================================
# ÍMÃ ESQUERDO
# ============================================================

S_esquerdo = Rectangle(
    (-2.7, -2),
    0.4,
    4,
    facecolor="blue"
)

N_esquerdo = Rectangle(
    (-2.3, -2),
    0.4,
    4,
    facecolor="red"
)

ax.add_patch(S_esquerdo)
ax.add_patch(N_esquerdo)

ax.text(
    -2.5,
    0,
    "S",
    ha="center",
    va="center",
    fontsize=22,
    color="white"
)

ax.text(
    -2.1,
    0,
    "N",
    ha="center",
    va="center",
    fontsize=22,
    color="white"
)


# ============================================================
# ÍMÃ DIREITO
# ============================================================

S_direito = Rectangle(
    (1.9, -2),
    0.4,
    4,
    facecolor="blue"
)

N_direito = Rectangle(
    (2.3, -2),
    0.4,
    4,
    facecolor="red"
)

ax.add_patch(S_direito)
ax.add_patch(N_direito)

ax.text(
    2.1,
    0,
    "S",
    ha="center",
    va="center",
    fontsize=22,
    color="white"
)

ax.text(
    2.5,
    0,
    "N",
    ha="center",
    va="center",
    fontsize=22,
    color="white"
)


# ============================================================
# CAMPO MAGNÉTICO
# ============================================================

setas_campo = []

for y in np.linspace(-1.5, 1.5, 5):

    seta = ax.arrow(
        -1.7,
        y,
        3.0,
        0,
        head_width=0.10,
        head_length=0.15,
        length_includes_head=True,
        alpha=0.5
    )

    setas_campo.append(seta)


# ============================================================
# BOBINA RETANGULAR
# ============================================================

bobina, = ax.plot(
    [],
    [],
    linewidth=3,
    color="black"
)


# ============================================================
# EIXO / FIO ÚNICO
# ============================================================

eixo_fio, = ax.plot(
    [],
    [],
    linewidth=3,
    color="black"
)


# ============================================================
# LÂMPADA
# ============================================================

lampada = Circle(
    (0, -1.7),
    0.35,
    facecolor="gray",
    edgecolor="black",
    linewidth=2
)

ax.add_patch(lampada)

ax.text(
    0,
    -2.2,
    "Lâmpada",
    ha="center",
    fontsize=10
)


# ============================================================
# GRÁFICO V(t) E I(t)
# ============================================================

ax2 = fig.add_subplot(gs[0, 2:5])

pos = ax2.get_position()

ax2.set_position([
    pos.x0 + 0.04,
    pos.y0,
    pos.width,
    pos.height
])

ax2.set_xlim(0, 2)

ax2.set_title(
    "Gerador AC - Tensão e Corrente x Tempo"
)

ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("V(t), I(t)")

ax2.grid()


# ============================================================
# ESCALA INICIAL
# ============================================================

mascara = t <= 2

Vmax = np.max(
    np.abs(ddp_resultante[mascara])
)

Imax = np.max(
    np.abs(I_induzida[mascara])
)

ymax = max(
    Vmax,
    Imax
)

if ymax == 0:
    ymax = 1

ax2.set_ylim(
    -1.1 * ymax,
    1.1 * ymax
)


# ============================================================
# CURVA V(t)
# ============================================================

curva_V, = ax2.plot(
    t[mascara],
    ddp_resultante[mascara],
    linewidth=2,
    label="V(t)"
)


# ============================================================
# CURVA I(t)
# ============================================================

curva_I, = ax2.plot(
    t[mascara],
    I_induzida[mascara],
    linewidth=2,
    label="I(t)"
)


# ============================================================
# LEGENDA
# ============================================================

ax2.legend()


# ============================================================
# PONTO INSTANTÂNEO DA TENSÃO
# ============================================================

ponto_V, = ax2.plot(
    [],
    [],
    "o",
    markersize=8
)


# ============================================================
# PONTO INSTANTÂNEO DA CORRENTE
# ============================================================

ponto_I, = ax2.plot(
    [],
    [],
    "o",
    markersize=8
)


# ============================================================
# LINHA DO TEMPO
# ============================================================

linha_tempo = ax2.axvline(
    0,
    linestyle="--",
    alpha=0.6
)


# ============================================================
# TÍTULO DOS PARÂMETROS
# ============================================================

fig.text(
    0.30,
    0.31,
    "Parâmetros do gerador",
    ha="center",
    fontsize=12,
    fontweight="bold"
)


# ============================================================
# SLIDER N
# ============================================================

ax_N = plt.axes(
    [0.10, 0.25, 0.40, 0.03]
)

slider_N = Slider(
    ax_N,
    "N",
    1,
    500,
    valinit=N,
    valstep=1
)


# ============================================================
# SLIDER A
# ============================================================

ax_A = plt.axes(
    [0.10, 0.20, 0.40, 0.03]
)

slider_A = Slider(
    ax_A,
    "A",
    0.1,
    5,
    valinit=A
)


# ============================================================
# SLIDER B
# ============================================================

ax_B = plt.axes(
    [0.10, 0.15, 0.40, 0.03]
)

slider_B = Slider(
    ax_B,
    "B",
    -2,
    2,
    valinit=B
)


# ============================================================
# SLIDER ω
# ============================================================

ax_w = plt.axes(
    [0.10, 0.10, 0.40, 0.03]
)

slider_w = Slider(
    ax_w,
    "ω (rad/s)",
    0,
    20,
    valinit=w
)


# ============================================================
# SLIDER R
# ============================================================

ax_R = plt.axes(
    [0.10, 0.05, 0.40, 0.03]
)

slider_R = Slider(
    ax_R,
    "R (Ω)",
    1,
    100,
    valinit=R
)


# ============================================================
# ATUALIZAÇÃO DOS SLIDERS
# ============================================================

def update_sliders(val):

    global N
    global A
    global B
    global w
    global R

    global ddp_resultante
    global I_induzida

    # ---------------------------
    # Novos parâmetros
    # ---------------------------

    N = slider_N.val
    A = slider_A.val
    B = slider_B.val
    w = slider_w.val
    R = slider_R.val

    # ---------------------------
    # Recalcula tensão
    # ---------------------------

    ddp_resultante = ddp(
        N,
        A,
        B,
        w,
        t
    )

    # ---------------------------
    # Recalcula corrente
    # ---------------------------

    I_induzida = I(
        ddp_resultante,
        R
    )

    # ========================================================
    # ATUALIZA V(t)
    # ========================================================

    curva_V.set_ydata(
        ddp_resultante[mascara]
    )

    # ========================================================
    # ATUALIZA I(t)
    # ========================================================

    curva_I.set_ydata(
        I_induzida[mascara]
    )

    # ========================================================
    # ESCALA DINÂMICA
    # ========================================================

    Vmax = np.max(
        np.abs(ddp_resultante[mascara])
    )

    Imax = np.max(
        np.abs(I_induzida[mascara])
    )

    ymax = max(
        Vmax,
        Imax
    )

    if ymax == 0:
        ymax = 1

    ax2.set_ylim(
        -1.1 * ymax,
        1.1 * ymax
    )

    # ========================================================
    # ATUALIZA SENTIDO DO CAMPO
    # ========================================================

    for seta in setas_campo:
        seta.remove()

    setas_campo.clear()

    if B >= 0:
        sentido = 1
    else:
        sentido = -1

    for y in np.linspace(-1.5, 1.5, 5):

        seta = ax.arrow(
            -1.7 if sentido == 1 else 1.3,
            y,
            3.0 * sentido,
            0,
            head_width=0.10,
            head_length=0.15,
            length_includes_head=True,
            alpha=0.5
        )

        setas_campo.append(seta)

    fig.canvas.draw_idle()


# ============================================================
# CONECTA SLIDERS
# ============================================================

slider_N.on_changed(update_sliders)
slider_A.on_changed(update_sliders)
slider_B.on_changed(update_sliders)
slider_w.on_changed(update_sliders)
slider_R.on_changed(update_sliders)


# ============================================================
# ANIMAÇÃO
# ============================================================

def animar(frame):

    # ========================================================
    # TEMPO
    # ========================================================

    tempo = frame * 0.02

    # ========================================================
    # ÂNGULO DA BOBINA
    # ========================================================

    angulo = w * tempo

    # ========================================================
    # BOBINA RETANGULAR
    # ========================================================

    largura = 1.5 * np.cos(angulo)

    altura = 1.2

    x = np.array([
        -largura,
         largura,
         largura,
        -largura,
        -largura
    ])

    y = np.array([
        -altura,
        -altura,
         altura,
         altura,
        -altura
    ])

    bobina.set_data(
        x,
        y
    )

    # ========================================================
    # EIXO / FIO ÚNICO
    # ========================================================

    eixo_fio.set_data(
        [
            0,
            0
        ],
        [
            -1.7,
            -altura
        ]
    )

    # ========================================================
    # TENSÃO INSTANTÂNEA
    # ========================================================

    V = ddp(
        N,
        A,
        B,
        w,
        tempo
    )

    # ========================================================
    # CORRENTE INSTANTÂNEA
    # ========================================================

    corrente = I(
        V,
        R
    )

    # ========================================================
    # BRILHO DA LÂMPADA
    # ========================================================

    Vmax_lampada = abs(
        N * A * B * w
    )

    if Vmax_lampada > 0:

        brilho = min(
            abs(V) / Vmax_lampada,
            1
        )

    else:

        brilho = 0

    # --------------------------------------------------------
    # Cinza → amarelo
    # --------------------------------------------------------

    lampada.set_facecolor(
        (
            0.35 + 0.65 * brilho,
            0.35 + 0.65 * brilho,
            0.35 * (1 - brilho)
        )
    )

    # ========================================================
    # GRÁFICO
    # ========================================================

    if tempo <= 2:

        # ---------------------------
        # Ponto V(t)
        # ---------------------------

        ponto_V.set_data(
            [tempo],
            [V]
        )

        # ---------------------------
        # Ponto I(t)
        # ---------------------------

        ponto_I.set_data(
            [tempo],
            [corrente]
        )

        # ---------------------------
        # Linha do tempo
        # ---------------------------

        linha_tempo.set_xdata(
            [tempo, tempo]
        )

    # ========================================================
    # RETORNO
    # ========================================================

    return (
        bobina,
        eixo_fio,
        ponto_V,
        ponto_I,
        linha_tempo,
        lampada
    )


# ============================================================
# CRIA ANIMAÇÃO
# ============================================================

anim = FuncAnimation(
    fig,
    animar,
    frames=100,
    interval=20,
    repeat=True
)


# ============================================================
# EXIBIÇÃO
# ============================================================

plt.show()
