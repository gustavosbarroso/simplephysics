import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider


# ============================================================
# PARÂMETROS INICIAIS
# ============================================================

m = 1.0
k = 2.0
kc = 1.0

x1_0 = 0.8
x2_0 = -0.8

v1_0 = 0.0
v2_0 = 0.0

t_max = 20.0
N = 400


# ============================================================
# EQUAÇÕES DIFERENCIAIS
# ============================================================

def f(r, t):
    x1, v1, x2, v2 = r

    a1 = (-k * x1 + kc * (x2 - x1)) / m
    a2 = (-k * x2 + kc * (x1 - x2)) / m

    return np.array([v1, a1, v2, a2], dtype=float)


# ============================================================
# MÉTODO RK4
# ============================================================

def RK4(func, a, b, n_steps, r0):
    h = (b - a) / n_steps
    tp = np.linspace(a, b, n_steps + 1)

    r = np.array(r0, dtype=float)

    x1_values = np.empty(n_steps + 1)
    v1_values = np.empty(n_steps + 1)
    x2_values = np.empty(n_steps + 1)
    v2_values = np.empty(n_steps + 1)

    x1_values[0], v1_values[0] = r[0], r[1]
    x2_values[0], v2_values[0] = r[2], r[3]

    for i in range(n_steps):
        t = tp[i]

        k1 = h * func(r, t)
        k2 = h * func(r + 0.5 * k1, t + 0.5 * h)
        k3 = h * func(r + 0.5 * k2, t + 0.5 * h)
        k4 = h * func(r + k3, t + h)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6

        x1_values[i + 1], v1_values[i + 1] = r[0], r[1]
        x2_values[i + 1], v2_values[i + 1] = r[2], r[3]

    return (
        tp,
        x1_values,
        v1_values,
        x2_values,
        v2_values
    )


# ============================================================
# SOLVER
# ============================================================

def solve():
    initial_state = [x1_0, v1_0, x2_0, v2_0]

    return RK4(
        f,
        0.0,
        t_max,
        N,
        initial_state
    )


# ============================================================
# SOLUÇÃO INICIAL
# ============================================================

tp, x1, v1, x2, v2 = solve()


# ============================================================
# ENERGIA MECÂNICA
# ============================================================

def calcular_energia():
    energia_cinetica = 0.5 * m * (v1**2 + v2**2)

    energia_potencial = (
        0.5 * k * (x1**2 + x2**2)
        + 0.5 * kc * (x2 - x1)**2
    )

    return energia_cinetica + energia_potencial


E = calcular_energia()


# ============================================================
# IDENTIFICAÇÃO DO MODO
# ============================================================

def identificar_modo():
    if abs(x1_0 - x2_0) < 1e-2:
        return "Modo simétrico"

    if abs(x1_0 + x2_0) < 1e-2:
        return "Modo antissimétrico"

    return "Batimento"


modo = identificar_modo()


# ============================================================
# FIGURA
# ============================================================

fig, (ax_sistema, ax_grafico) = plt.subplots(
    1,
    2,
    figsize=(12, 6),
    gridspec_kw={"width_ratios": [1.15, 1.0]}
)

fig.subplots_adjust(
    left=0.24,
    right=0.97,
    top=0.90,
    bottom=0.36,
    wspace=0.35
)


# ============================================================
# SISTEMA FÍSICO
# ============================================================

L = 5.0

ax_sistema.set_title("Osciladores Acoplados")
ax_sistema.set_xlabel("Posição no desenho (m)")
ax_sistema.set_yticks([])
ax_sistema.set_xlim(-L, L)
ax_sistema.set_ylim(-1.0, 1.0)
ax_sistema.grid(alpha=0.25)

ax_sistema.plot([-L, -L], [-0.75, 0.75], "k", lw=3)
ax_sistema.plot([L, L], [-0.75, 0.75], "k", lw=3)

# Referências visuais, como no JavaScript
ax_sistema.axvline(-1, color="gray", ls=":", lw=1)
ax_sistema.axvline(+1, color="gray", ls=":", lw=1)

mola_esquerda, = ax_sistema.plot([], [], "g-", lw=2)
mola_central, = ax_sistema.plot([], [], "g-", lw=2)
mola_direita, = ax_sistema.plot([], [], "g-", lw=2)

massa1, = ax_sistema.plot(
    [], [], "ro", ms=13, mec="black"
)

massa2, = ax_sistema.plot(
    [], [], "bo", ms=13, mec="black"
)

label1 = ax_sistema.text(0, 0.35, "m₁", ha="center")
label2 = ax_sistema.text(0, 0.35, "m₂", ha="center")

valor1 = ax_sistema.text(
    0, -0.35, "", ha="center", fontsize=9
)

valor2 = ax_sistema.text(
    0, -0.35, "", ha="center", fontsize=9
)


# ============================================================
# DESENHO DAS MOLAS
# ============================================================

def desenhar_mola(xa, xb, n=18, amplitude=0.09):
    if abs(xb - xa) < 1e-9:
        return np.array([xa, xb]), np.array([0.0, 0.0])

    xs = np.linspace(xa, xb, n + 1)
    ys = np.zeros(n + 1)

    for j in range(1, n):
        ys[j] = amplitude if j % 2 else -amplitude

    return xs, ys


# ============================================================
# GRÁFICO DAS POSIÇÕES
# ============================================================

ax_grafico.set_title("Posições ao longo do tempo")
ax_grafico.set_xlabel("t (s)")
ax_grafico.set_ylabel("x (m)")
ax_grafico.set_xlim(0, t_max)
ax_grafico.grid(alpha=0.3)

line_x1, = ax_grafico.plot(
    [], [], "r-", lw=1.8, label="x₁(t)"
)

line_x2, = ax_grafico.plot(
    [], [], "b-", lw=1.8, label="x₂(t)"
)

ponto_x1, = ax_grafico.plot([], [], "ro", ms=4)
ponto_x2, = ax_grafico.plot([], [], "bo", ms=4)

ax_grafico.legend(loc="upper right")


# ============================================================
# PAINEL DE INFORMAÇÕES
# ============================================================

text_info = fig.text(
    0.025,
    0.83,
    "",
    fontsize=9,
    va="top",
    bbox={
        "boxstyle": "round,pad=0.5",
        "facecolor": "white",
        "alpha": 0.9
    }
)


# ============================================================
# ATUALIZAÇÃO DA ANIMAÇÃO
# ============================================================

def update(frame):
    i = int(frame)

    # Posições visuais: iguais à transformação do JavaScript.
    # x1 e x2 continuam sendo as coordenadas usadas na física.
    X1 = -1.0 + x1[i]
    X2 = +1.0 + x2[i]

    # Mola esquerda
    xs, ys = desenhar_mola(-L, X1)
    mola_esquerda.set_data(xs, ys)

    # Mola central
    xs, ys = desenhar_mola(X1, X2)
    mola_central.set_data(xs, ys)

    # Mola direita
    xs, ys = desenhar_mola(X2, L)
    mola_direita.set_data(xs, ys)

    # Massas
    massa1.set_data([X1], [0])
    massa2.set_data([X2], [0])

    label1.set_position((X1, 0.30))
    label2.set_position((X2, 0.30))

    valor1.set_position((X1, -0.30))
    valor2.set_position((X2, -0.30))

    valor1.set_text(f"{x1[i]:.2f} m")
    valor2.set_text(f"{x2[i]:.2f} m")

    # Gráfico
    line_x1.set_data(tp[:i + 1], x1[:i + 1])
    line_x2.set_data(tp[:i + 1], x2[:i + 1])

    ponto_x1.set_data([tp[i]], [x1[i]])
    ponto_x2.set_data([tp[i]], [x2[i]])

    # Escala vertical dinâmica
    ymin = min(
        float(np.min(x1[:i + 1])),
        float(np.min(x2[:i + 1]))
    )

    ymax = max(
        float(np.max(x1[:i + 1])),
        float(np.max(x2[:i + 1]))
    )

    if abs(ymax - ymin) < 1e-8:
        ymin -= 1.0
        ymax += 1.0
    else:
        margem = 0.15 * (ymax - ymin)
        ymin -= margem
        ymax += margem

    ax_grafico.set_ylim(ymin, ymax)

    # Informações
    text_info.set_text(
        f"m = {m:.2f} kg       k = {k:.2f} N/m\n"
        f"kc = {kc:.2f} N/m\n\n"
        f"x₁ = {x1[i]:.3f} m     x₂ = {x2[i]:.3f} m\n"
        f"v₁ = {v1[i]:.3f} m/s   v₂ = {v2[i]:.3f} m/s\n"
        f"E = {E[i]:.3f} J\n"
        f"t = {tp[i]:.2f} s\n"
        f"{modo}"
    )

    return (
        mola_esquerda,
        mola_central,
        mola_direita,
        massa1,
        massa2,
        label1,
        label2,
        valor1,
        valor2,
        line_x1,
        line_x2,
        ponto_x1,
        ponto_x2,
        text_info
    )


def init():
    return update(0)


# ============================================================
# SLIDERS
# ============================================================

slider_axes = [
    fig.add_axes([0.27, 0.265, 0.64, 0.025]),
    fig.add_axes([0.27, 0.215, 0.64, 0.025]),
    fig.add_axes([0.27, 0.165, 0.64, 0.025]),
    fig.add_axes([0.27, 0.115, 0.64, 0.025]),
    fig.add_axes([0.27, 0.065, 0.64, 0.025])
]

slider_m = Slider(
    slider_axes[0], "m (kg)",
    0.5, 5.0, valinit=m, valstep=0.1
)

slider_k = Slider(
    slider_axes[1], "k (N/m)",
    0.5, 10.0, valinit=k, valstep=0.1
)

slider_kc = Slider(
    slider_axes[2], "kc (N/m)",
    0.1, 10.0, valinit=kc, valstep=0.1
)

slider_x1 = Slider(
    slider_axes[3], "x₁₀ (m)",
    -1.0, 1.0, valinit=x1_0, valstep=0.1
)

slider_x2 = Slider(
    slider_axes[4], "x₂₀ (m)",
    -1.0, 1.0, valinit=x2_0, valstep=0.1
)


# ============================================================
# ATUALIZAÇÃO DOS SLIDERS
# ============================================================

def update_sliders(_):
    global m, k, kc, x1_0, x2_0
    global tp, x1, v1, x2, v2, E, modo

    m = float(slider_m.val)
    k = float(slider_k.val)
    kc = float(slider_kc.val)

    x1_0 = float(slider_x1.val)
    x2_0 = float(slider_x2.val)

    # Recalcula a solução com os valores novos
    tp, x1, v1, x2, v2 = solve()

    E = calcular_energia()
    modo = identificar_modo()

    ax_grafico.set_xlim(tp[0], tp[-1])

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()

    update(0)
    fig.canvas.draw_idle()

    ani.event_source.start()


for slider in (
    slider_m,
    slider_k,
    slider_kc,
    slider_x1,
    slider_x2
):
    slider.on_changed(update_sliders)


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
    repeat=True,
    cache_frame_data=False
)


# ============================================================
# MOSTRAR
# ============================================================

plt.show()
