# ---------------------------
# Imports
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation


# ---------------------------
# Gerador de ondas
# ---------------------------
def onda(A, comprimento_onda, f, x, t, phi):
    return A * np.sin(((2 * np.pi) / comprimento_onda) * x- (2 * np.pi * f) * t+ phi)


# ---------------------------
# Parâmetros espaciais
# ---------------------------
x = np.linspace(0, 10, 1000)

x_min = 0
x_max = 10

t = 0


# ---------------------------
# Valores iniciais
# ---------------------------
A1_0 = 10
A2_0 = 10

lambda1_0 = 2
lambda2_0 = 2

f1_0 = 1
f2_0 = 1

phi1_0 = 0
phi2_0 = np.pi / 2


# ---------------------------
# Ondas iniciais
# ---------------------------
y1 = onda(A1_0,lambda1_0, f1_0, x, t, phi1_0)

y2 = onda(A2_0,lambda2_0, f2_0, x, t, phi2_0)

y_resultante = y1 + y2


# ---------------------------
# Figura
# ---------------------------
fig = plt.figure(figsize=(15, 8))

gs = fig.add_gridspec(
    2,
    5,
    height_ratios=[5, 2],
    width_ratios=[4, 1, 4, 1, 4]
)


# ---------------------------
# Primeiro gráfico
# ---------------------------
ax1 = fig.add_subplot(gs[0, 0])

line1, = ax1.plot(x, y1)

ax1.set_title(r"$y_1(x,t)$")
ax1.set_xlabel("x")
ax1.set_ylabel(r"$y_1(m)$")

ax1.set_xlim(x_min, x_max)
ax1.set_ylim(-22, 22)

ax1.grid()


# ---------------------------
# Sinal de soma
# ---------------------------
ax_plus = fig.add_subplot(gs[0, 1])

ax_plus.text(
    0.2,
    0.5,
    "+",
    fontsize=35,
    ha="center",
    va="center"
)

ax_plus.axis("off")


# ---------------------------
# Segundo gráfico
# ---------------------------
ax2 = fig.add_subplot(gs[0, 2])

line2, = ax2.plot(x, y2)

ax2.set_title(r"$y_2(x,t)$")
ax2.set_xlabel("x(m)")
ax2.set_ylabel(r"$y_2(m)$")

ax2.set_xlim(x_min, x_max)
ax2.set_ylim(-22, 22)

ax2.grid()


# ---------------------------
# Sinal de igualdade
# ---------------------------
ax_equal = fig.add_subplot(gs[0, 3])

ax_equal.text(
    0.2,
    0.5,
    "=",
    fontsize=35,
    ha="center",
    va="center"
)

ax_equal.axis("off")


# ---------------------------
# Gráfico resultante
# ---------------------------
ax3 = fig.add_subplot(gs[0, 4])

line3, = ax3.plot(x, y_resultante)

ax3.set_title(r"$y_1(x,t) + y_2(x,t)$")
ax3.set_xlabel("x(m)")
ax3.set_ylabel(r"$y_1(m) + y_2(m)$")

ax3.set_xlim(x_min, x_max)
ax3.set_ylim(-22, 22)

ax3.grid()


# ============================================================
# SLIDERS
# ============================================================

# ============================================================
# ONDA 1 — ESQUERDA
# ============================================================

# ---------------------------
# Título Onda 1
# ---------------------------
fig.text(
    0.10,
    0.31,
    "Onda 1",
    ha="center",
    fontsize=12,
    fontweight="bold"
)


# ---------------------------
# Slider A1
# ---------------------------
ax_A1 = plt.axes([0.08, 0.25, 0.30, 0.03])

slider_A1 = Slider(
    ax_A1,
    "A₁(m)",
    -10,
    10,
    valinit=A1_0
)


# ---------------------------
# Slider lambda1
# ---------------------------
ax_lambda1 = plt.axes([0.08, 0.20, 0.30, 0.03])

slider_lambda1 = Slider(
    ax_lambda1,
    "λ₁(m)",
    0.5,
    5,
    valinit=lambda1_0
)


# ---------------------------
# Slider f1
# ---------------------------
ax_f1 = plt.axes([0.08, 0.15, 0.30, 0.03])

slider_f1 = Slider(
    ax_f1,
    "f₁(Hz)",
    0,
    5,
    valinit=f1_0
)


# ---------------------------
# Slider phi1
# ---------------------------
ax_phi1 = plt.axes([0.08, 0.10, 0.30, 0.03])

slider_phi1 = Slider(
    ax_phi1,
    "φ₁(rad)",
    -np.pi,
    np.pi,
    valinit=phi1_0
)


# ============================================================
# ONDA 2 — DIREITA
# ============================================================

# ---------------------------
# Título Onda 2
# ---------------------------
fig.text(
    0.60,
    0.31,
    "Onda 2",
    ha="center",
    fontsize=12,
    fontweight="bold"
)


# ---------------------------
# Slider A2
# ---------------------------
ax_A2 = plt.axes([0.58, 0.25, 0.30, 0.03])

slider_A2 = Slider(
    ax_A2,
    "A₂(m)",
    -10,
    10,
    valinit=A2_0
)


# ---------------------------
# Slider lambda2
# ---------------------------
ax_lambda2 = plt.axes([0.58, 0.20, 0.30, 0.03])

slider_lambda2 = Slider(
    ax_lambda2,
    "λ₂(m)",
    0.5,
    5,
    valinit=lambda2_0
)


# ---------------------------
# Slider f2
# ---------------------------
ax_f2 = plt.axes([0.58, 0.15, 0.30, 0.03])

slider_f2 = Slider(
    ax_f2,
    "f₂(Hz)",
    0,
    5,
    valinit=f2_0
)


# ---------------------------
# Slider phi2
# ---------------------------
ax_phi2 = plt.axes([0.58, 0.10, 0.30, 0.03])

slider_phi2 = Slider(
    ax_phi2,
    "φ₂(rad)",
    -np.pi,
    np.pi,
    valinit=phi2_0
)


# ============================================================
# ATUALIZAÇÃO
# ============================================================

def update(val):

    A1 = slider_A1.val
    A2 = slider_A2.val

    lambda1 = slider_lambda1.val
    lambda2 = slider_lambda2.val

    f1 = slider_f1.val
    f2 = slider_f2.val

    phi1 = slider_phi1.val
    phi2 = slider_phi2.val

    # ---------------------------
    # Calcula ondas
    # ---------------------------
    y1 = onda(
        A1,
        lambda1,
        f1,
        x,
        t,
        phi1
    )

    y2 = onda(
        A2,
        lambda2,
        f2,
        x,
        t,
        phi2
    )

    y_resultante = y1 + y2

    # ---------------------------
    # Atualiza gráficos
    # ---------------------------
    line1.set_ydata(y1)
    line2.set_ydata(y2)
    line3.set_ydata(y_resultante)

    fig.canvas.draw_idle()


# ---------------------------
# Conecta sliders
# ---------------------------
slider_A1.on_changed(update)
slider_lambda1.on_changed(update)
slider_f1.on_changed(update)
slider_phi1.on_changed(update)

slider_A2.on_changed(update)
slider_lambda2.on_changed(update)
slider_f2.on_changed(update)
slider_phi2.on_changed(update)


# ============================================================
# ANIMAÇÃO
# ============================================================

def animar(frame):

    global t

    # Avanço do tempo
    t = frame * 0.02

    # Parâmetros atuais dos sliders
    A1 = slider_A1.val
    A2 = slider_A2.val

    lambda1 = slider_lambda1.val
    lambda2 = slider_lambda2.val

    f1 = slider_f1.val
    f2 = slider_f2.val

    phi1 = slider_phi1.val
    phi2 = slider_phi2.val

    # ---------------------------
    # Calcula ondas
    # ---------------------------
    y1 = onda(
        A1,
        lambda1,
        f1,
        x,
        t,
        phi1
    )

    y2 = onda(
        A2,
        lambda2,
        f2,
        x,
        t,
        phi2
    )

    y_resultante = y1 + y2

    # ---------------------------
    # Atualiza gráficos
    # ---------------------------
    line1.set_ydata(y1)
    line2.set_ydata(y2)
    line3.set_ydata(y_resultante)

    return line1, line2, line3


# ---------------------------
# Cria animação
# ---------------------------
anim = FuncAnimation(
    fig,
    animar,
    frames=1000,
    interval=20,
    blit=False
)


# ---------------------------
# Exibição
# ---------------------------
plt.show()
