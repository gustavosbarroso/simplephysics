# ============================================================
# TUNELAMENTO QUÂNTICO - DIFERENÇAS FINITAS
# Crank-Nicolson + Sliders
# ============================================================

# ---------------------------
# Imports
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

from scipy.sparse import diags, identity
from scipy.sparse.linalg import splu


# ============================================================
# PARÂMETROS NUMÉRICOS
# ============================================================

h_bar = 1.0
m = 1.0

x_min = -6.5
x_max = 6.5

N = 500

x = np.linspace(x_min, x_max, N + 1)
dx = x[1] - x[0]

# Usaremos apenas os pontos internos
x_int = x[1:-1]
M = len(x_int)


# ============================================================
# PARÂMETROS FÍSICOS INICIAIS
# ============================================================

V0_inicial = 20.0
a_inicial = 0.5

x0_inicial = -2.5
sigma_inicial = 0.4
k0_inicial = 5.0


# ============================================================
# PARÂMETROS TEMPORAIS
# ============================================================

dt = 0.002

# Número de passos calculados por frame
passos_por_frame = 5


# ============================================================
# FUNÇÃO DE ONDA INICIAL
# ============================================================

def criar_pacote(x0, sigma, k0):

    psi = np.exp(
        -(x_int - x0)**2 / (4 * sigma**2)
    ) * np.exp(
        1j * k0 * x_int
    )

    # Normalização
    norma = np.sqrt(
        np.sum(np.abs(psi)**2) * dx
    )

    psi /= norma

    return psi


# ============================================================
# POTENCIAL
# ============================================================

def criar_potencial(V0, a):

    V = np.zeros_like(x_int)

    mascara = (
        (x_int > 0) &
        (x_int < a)
    )

    V[mascara] = V0

    return V


# ============================================================
# HAMILTONIANA POR DIFERENÇAS FINITAS
# ============================================================

def criar_hamiltoniana(V0, a):

    V = criar_potencial(V0, a)

    # Termo cinético
    diagonal = (
        h_bar**2 / (m * dx**2)
        + V
    )

    fora_diagonal = (
        -h_bar**2 / (2 * m * dx**2)
    )

    H = diags(
        [
            fora_diagonal * np.ones(M - 1),
            diagonal,
            fora_diagonal * np.ones(M - 1)
        ],
        offsets=[-1, 0, 1],
        format="csc"
    )

    return H, V


# ============================================================
# CRANK-NICOLSON
# ============================================================

def criar_evolucao(H):

    I = identity(
        M,
        format="csc"
    )

    fator = 1j * dt / (2 * h_bar)

    A = I + fator * H
    B = I - fator * H

    # Fatoração LU de A
    solver = splu(A)

    return B, solver


# ============================================================
# ESTADO INICIAL
# ============================================================

V0 = V0_inicial
a = a_inicial

x0 = x0_inicial
sigma = sigma_inicial
k0 = k0_inicial

psi = criar_pacote(
    x0,
    sigma,
    k0
)

H, V = criar_hamiltoniana(
    V0,
    a
)

B, solver = criar_evolucao(H)


# ============================================================
# FIGURA
# ============================================================

fig, ax = plt.subplots(
    figsize=(11, 6)
)

plt.subplots_adjust(
    left=0.08,
    right=0.90,
    bottom=0.38
)


# ---------------------------
# Probabilidade
# ---------------------------

line_prob, = ax.plot(
    x_int,
    np.abs(psi)**2,
    label=r"$|\Psi(x,t)|^2$",
    linewidth=2
)


# ---------------------------
# Potencial
# ---------------------------

axV = ax.twinx()

line_V, = axV.plot(
    x_int,
    V,
    label=r"$V(x)$",
    linewidth=2
)


ax.set_xlim(
    x_min,
    x_max
)

ax.set_ylim(
    0,
    4
)

axV.set_ylim(
    0,
    45
)


ax.set_xlabel(
    r"$x$"
)

ax.set_ylabel(
    r"$|\Psi(x,t)|^2$"
)

axV.set_ylabel(
    r"$V(x)$"
)


ax.set_title(
    "Tunelamento Quântico"
)


# ============================================================
# TEXTO DE INFORMAÇÕES
# ============================================================

texto = ax.text(
    0.02,
    0.94,
    "",
    transform=ax.transAxes,
    verticalalignment="top"
)


# ============================================================
# SLIDERS
# ============================================================

# V0
ax_V0 = plt.axes(
    [0.15, 0.28, 0.65, 0.025]
)

slider_V0 = Slider(
    ax_V0,
    r"$V_0$",
    1.0,
    40.0,
    valinit=V0_inicial,
    valstep=0.5
)


# largura da barreira
ax_a = plt.axes(
    [0.15, 0.235, 0.65, 0.025]
)

slider_a = Slider(
    ax_a,
    r"$a$",
    0.1,
    2.0,
    valinit=a_inicial,
    valstep=0.05
)


# posição inicial
ax_x0 = plt.axes(
    [0.15, 0.19, 0.65, 0.025]
)

slider_x0 = Slider(
    ax_x0,
    r"$x_0$",
    -5.0,
    -1.0,
    valinit=x0_inicial,
    valstep=0.1
)


# largura do pacote
ax_sigma = plt.axes(
    [0.15, 0.145, 0.65, 0.025]
)

slider_sigma = Slider(
    ax_sigma,
    r"$\sigma$",
    0.2,
    1.0,
    valinit=sigma_inicial,
    valstep=0.05
)


# número de onda
ax_k0 = plt.axes(
    [0.15, 0.10, 0.65, 0.025]
)

slider_k0 = Slider(
    ax_k0,
    r"$k_0$",
    1.0,
    8.0,
    valinit=k0_inicial,
    valstep=0.1
)


# ============================================================
# BOTÃO RESET
# ============================================================

ax_reset = plt.axes(
    [0.82, 0.10, 0.10, 0.04]
)

botao_reset = Button(
    ax_reset,
    "Reset"
)


# ============================================================
# ATUALIZAÇÃO DOS PARÂMETROS
# ============================================================

def atualizar(_):

    global V0
    global a
    global x0
    global sigma
    global k0

    global psi
    global H
    global V
    global B
    global solver

    # ---------------------------
    # Ler sliders
    # ---------------------------

    V0 = slider_V0.val
    a = slider_a.val

    x0 = slider_x0.val
    sigma = slider_sigma.val
    k0 = slider_k0.val

    # ---------------------------
    # Recalcular Hamiltoniana
    # ---------------------------

    H, V = criar_hamiltoniana(
        V0,
        a
    )

    # ---------------------------
    # Recalcular evolução
    # ---------------------------

    B, solver = criar_evolucao(H)

    # ---------------------------
    # Criar novo pacote
    # ---------------------------

    psi = criar_pacote(
        x0,
        sigma,
        k0
    )

    # ---------------------------
    # Atualizar gráfico
    # ---------------------------

    line_prob.set_ydata(
        np.abs(psi)**2
    )

    line_V.set_ydata(V)

    axV.set_ylim(
        0,
        max(45, V0 * 1.15)
    )

    fig.canvas.draw_idle()


# Todos os sliders chamam a mesma função
slider_V0.on_changed(atualizar)
slider_a.on_changed(atualizar)
slider_x0.on_changed(atualizar)
slider_sigma.on_changed(atualizar)
slider_k0.on_changed(atualizar)


# ============================================================
# RESET
# ============================================================

def resetar(event):

    slider_V0.reset()
    slider_a.reset()
    slider_x0.reset()
    slider_sigma.reset()
    slider_k0.reset()


botao_reset.on_clicked(resetar)


# ============================================================
# ANIMAÇÃO
# ============================================================

def update(frame):

    global psi

    # ---------------------------
    # Vários passos de
    # Crank-Nicolson
    # ---------------------------

    for _ in range(passos_por_frame):

        psi = solver.solve(
            B @ psi
        )

    # ---------------------------
    # Atualizar probabilidade
    # ---------------------------

    prob = np.abs(psi)**2

    line_prob.set_ydata(
        prob
    )

    # ---------------------------
    # Tempo
    # ---------------------------

    t = (
        frame
        * dt
        * passos_por_frame
    )

    # ---------------------------
    # Probabilidade à esquerda
    # ---------------------------

    mascara_esquerda = (
        x_int < 0
    )

    P_esquerda = np.sum(
        prob[mascara_esquerda]
    ) * dx

    # ---------------------------
    # Probabilidade à direita
    # ---------------------------

    mascara_direita = (
        x_int > a
    )

    P_direita = np.sum(
        prob[mascara_direita]
    ) * dx

    # ---------------------------
    # Probabilidade na barreira
    # ---------------------------

    mascara_barreira = (
        (x_int >= 0)
        &
        (x_int <= a)
    )

    P_barreira = np.sum(
        prob[mascara_barreira]
    ) * dx

    # ---------------------------
    # Probabilidade total
    # ---------------------------

    P_total = (
        P_esquerda
        + P_barreira
        + P_direita
    )

    # ---------------------------
    # Informações
    # ---------------------------

    texto.set_text(
        f"$t = {t:.3f}\\ \\mathrm{{u.t.}}$\n"
        f"Esquerda: {100 * P_esquerda:.1f}%\n"
        f"Tunelamento: {100 * P_direita:.1f}%\n"
        f"Na barreira: {100 * P_barreira:.1f}%\n"
        f"Total: {100 * P_total:.1f}%"
    )

    return (
        line_prob,
        line_V,
        texto
    )


# ============================================================
# CRIAR ANIMAÇÃO
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    interval=20,
    blit=False,
    cache_frame_data=False
)


# ============================================================
# MOSTRAR
# ============================================================

plt.show()
