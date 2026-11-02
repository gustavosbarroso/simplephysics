import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import Polygon, Rectangle, Ellipse
from matplotlib import cm, colors

# ============================================================
# PARÂMETROS
# ============================================================

params = {
    "T0": 90.0,
    "Tamb": 25.0,
    "k": 0.08,
    "t_max": 30.0,
    "N": 600
}

# ============================================================
# MODELO FÍSICO
# ============================================================

def derivada(T, t, params):

    Tamb = params["Tamb"]
    k = params["k"]

    return np.array([
        -k * (T[0] - Tamb)
    ])


# ============================================================
# INTEGRADOR RK4
# ============================================================

def rk4(f, T, t, h, params):

    k1 = h * f(T, t, params)

    k2 = h * f(
        T + k1 / 2,
        t + h / 2,
        params
    )

    k3 = h * f(
        T + k2 / 2,
        t + h / 2,
        params
    )

    k4 = h * f(
        T + k3,
        t + h,
        params
    )

    return T + (k1 + 2*k2 + 2*k3 + k4) / 6


# ============================================================
# SOLVER
# ============================================================

def solve(params):

    t_max = params["t_max"]
    N = params["N"]

    h = t_max / N

    t = np.linspace(0, t_max, N + 1)

    T = np.zeros((N + 1, 1))

    T[0] = params["T0"]

    for i in range(N):

        T[i + 1] = rk4(
            derivada,
            T[i],
            t[i],
            h,
            params
        )

    return t, T[:, 0]


# ============================================================
# SOLUÇÃO ANALÍTICA
# ============================================================

def solucao_analitica(t, params):

    T0 = params["T0"]
    Tamb = params["Tamb"]
    k = params["k"]

    return Tamb + (T0 - Tamb) * np.exp(-k * t)


# ============================================================
# FIGURA
# ============================================================

fig, (ax_copo, ax_grafico) = plt.subplots(
    1, 2,
    figsize=(13, 6)
)

plt.subplots_adjust(
    left=0.08,
    right=0.96,
    top=0.88,
    bottom=0.27,
    wspace=0.32
)

fig.suptitle(
    "Lei do Resfriamento de Newton",
    fontsize=17,
    fontweight="bold"
)

# ============================================================
# CORES
# ============================================================

cmap = cm.get_cmap("coolwarm")

norm = colors.Normalize(
    vmin=20,
    vmax=100
)

# ============================================================
# CENA DO COPO
# ============================================================

ax_copo.set_xlim(-2.5, 2.5)
ax_copo.set_ylim(-2.0, 3.0)

ax_copo.set_aspect("equal")
ax_copo.axis("off")

ax_copo.set_title(
    "Resfriamento do líquido",
    fontsize=13
)

# Corpo do copo

copo = Polygon(
    [
        (-0.85, 1.1),
        (0.85, 1.1),
        (0.65, -1.0),
        (-0.65, -1.0)
    ],
    closed=True,
    facecolor="#D9E2EC",
    edgecolor="#34495E",
    linewidth=2.5,
    zorder=3
)

ax_copo.add_patch(copo)

# Líquido

liquido = Rectangle(
    (-0.72, -0.85),
    1.44,
    1.65,
    facecolor=cmap(norm(params["T0"])),
    edgecolor="none",
    alpha=0.95,
    zorder=2
)

ax_copo.add_patch(liquido)

# Superfície do líquido

superficie = Ellipse(
    (0, 0.80),
    1.44,
    0.18,
    facecolor=cmap(norm(params["T0"])),
    edgecolor="#34495E",
    linewidth=1,
    zorder=4
)

ax_copo.add_patch(superficie)

# Alça

alca = Ellipse(
    (0.93, 0.15),
    0.75,
    1.15,
    facecolor="none",
    edgecolor="#34495E",
    linewidth=5,
    zorder=1
)

ax_copo.add_patch(alca)

# Termômetro

ax_copo.add_patch(
    Rectangle(
        (1.65, -0.65),
        0.16,
        2.3,
        facecolor="#ECF0F1",
        edgecolor="#34495E",
        linewidth=1.5
    )
)

ax_copo.add_patch(
    Ellipse(
        (1.73, -0.65),
        0.38,
        0.38,
        facecolor="#ECF0F1",
        edgecolor="#34495E",
        linewidth=1.5
    )
)

termometro = Rectangle(
    (1.69, -0.65),
    0.08,
    2.3,
    facecolor="#E74C3C",
    edgecolor="none"
)

ax_copo.add_patch(termometro)

bulbo = Ellipse(
    (1.73, -0.65),
    0.27,
    0.27,
    facecolor="#E74C3C",
    edgecolor="none"
)

ax_copo.add_patch(bulbo)

# Texto da temperatura

texto_temp = ax_copo.text(
    0,
    -1.55,
    "",
    ha="center",
    fontsize=15,
    fontweight="bold"
)

# Texto auxiliar

texto_amb = ax_copo.text(
    0,
    -1.85,
    "",
    ha="center",
    fontsize=10,
    color="gray"
)

# ============================================================
# VAPOR
# ============================================================

vapor = []

for i in range(3):

    linha, = ax_copo.plot(
        [],
        [],
        color="gray",
        linewidth=2,
        alpha=0.5
    )

    vapor.append(linha)


# ============================================================
# GRÁFICO DE TEMPERATURA
# ============================================================

ax_grafico.set_title(
    "Temperatura × Tempo",
    fontsize=13
)

ax_grafico.set_xlabel("Tempo")
ax_grafico.set_ylabel("Temperatura (°C)")

ax_grafico.grid(alpha=0.3)

ax_grafico.set_xlim(
    0,
    params["t_max"]
)

ax_grafico.set_ylim(
    0,
    110
)

# Dados iniciais

t, T = solve(params)

T_analitica = solucao_analitica(t, params)

linha_rk4, = ax_grafico.plot(
    [],
    [],
    color="#E74C3C",
    linewidth=2.5,
    label="RK4"
)

linha_analitica, = ax_grafico.plot(
    [],
    [],
    "--",
    color="#2980B9",
    linewidth=1.8,
    label="Analítica"
)

ponto, = ax_grafico.plot(
    [],
    [],
    "o",
    color="#E74C3C",
    markersize=7
)

ax_grafico.legend(loc="upper right")

# HUD

hud = fig.text(
    0.52,
    0.92,
    "",
    ha="center",
    fontsize=11
)

# ============================================================
# ESTADO DA ANIMAÇÃO
# ============================================================

estado = {
    "t": t,
    "T": T,
    "indice": 0
}


# ============================================================
# ATUALIZAÇÃO DA ANIMAÇÃO
# ============================================================

def update(frame):

    t = estado["t"]
    T = estado["T"]

    indice = min(frame, len(t) - 1)

    temperatura = T[indice]
    tempo = t[indice]

    Tamb = params["Tamb"]

    # --------------------------------------------------------
    # COR DO LÍQUIDO
    # --------------------------------------------------------

    cor = cmap(norm(temperatura))

    liquido.set_facecolor(cor)
    superficie.set_facecolor(cor)

    # --------------------------------------------------------
    # TERMÔMETRO
    # --------------------------------------------------------

    altura = np.clip(
        (temperatura - Tamb) / (100 - Tamb),
        0.03,
        1
    )

    termometro.set_height(2.3 * altura)

    # --------------------------------------------------------
    # VAPOR
    # --------------------------------------------------------

    intensidade = np.clip(
        (temperatura - Tamb) / 50,
        0,
        1
    )

    for i, linha in enumerate(vapor):

        fase = tempo * 1.8 + i * 2.1

        x = (
            0.30 * np.sin(
                np.linspace(0, 2*np.pi, 30) + fase
            )
            + (i - 1) * 0.22
        )

        y = (
            1.2
            + np.linspace(0, 0.75, 30)
        )

        linha.set_data(x, y)

        linha.set_alpha(
            intensidade * 0.55
        )

    # --------------------------------------------------------
    # TEXTO
    # --------------------------------------------------------

    texto_temp.set_text(
        f"{temperatura:.1f} °C"
    )

    texto_temp.set_color(cor)

    texto_amb.set_text(
        f"Ambiente: {Tamb:.1f} °C"
    )

    hud.set_text(
        f"Tempo: {tempo:.2f} s     "
        f"Temperatura: {temperatura:.2f} °C"
    )

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    linha_rk4.set_data(
        t[:indice + 1],
        T[:indice + 1]
    )

    analitica = solucao_analitica(t, params)

    linha_analitica.set_data(
        t[:indice + 1],
        analitica[:indice + 1]
    )

    ponto.set_data(
        [tempo],
        [temperatura]
    )

    return (
        liquido,
        superficie,
        termometro,
        texto_temp,
        texto_amb,
        hud,
        linha_rk4,
        linha_analitica,
        ponto,
        *vapor
    )


# ============================================================
# SLIDERS
# ============================================================

ax_T0 = plt.axes([0.18, 0.16, 0.65, 0.025])
ax_Tamb = plt.axes([0.18, 0.11, 0.65, 0.025])
ax_k = plt.axes([0.18, 0.06, 0.65, 0.025])

slider_T0 = Slider(
    ax_T0,
    "T inicial (°C)",
    40,
    100,
    valinit=params["T0"],
    valstep=1
)

slider_Tamb = Slider(
    ax_Tamb,
    "T ambiente (°C)",
    10,
    35,
    valinit=params["Tamb"],
    valstep=1
)

slider_k = Slider(
    ax_k,
    "k",
    0.01,
    0.30,
    valinit=params["k"],
    valstep=0.01
)


# ============================================================
# REINICIALIZAÇÃO
# ============================================================

def atualizar(val):

    params["T0"] = slider_T0.val
    params["Tamb"] = slider_Tamb.val
    params["k"] = slider_k.val

    # Novo cálculo numérico

    t, T = solve(params)

    estado["t"] = t
    estado["T"] = T

    # Reinicia a animação

    ani.event_source.stop()

    ani.frame_seq = ani.new_frame_seq()

    update(0)

    fig.canvas.draw_idle()

    ani.event_source.start()


slider_T0.on_changed(atualizar)
slider_Tamb.on_changed(atualizar)
slider_k.on_changed(atualizar)


# ============================================================
# ANIMAÇÃO
# ============================================================

ani = FuncAnimation(
    fig,
    update,
    frames=params["N"] + 1,
    interval=30,
    blit=False,
    repeat=False
)

plt.show()
