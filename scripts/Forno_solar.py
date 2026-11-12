
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.patches import (
    Polygon, Ellipse, Circle, Rectangle
)
from matplotlib import cm, colors


# ============================================================
# 1. CONSTANTES FÍSICAS
# ============================================================

sigma = 5.670374419e-8

c1 = 900

tau = 0.95
kappa = 1.0

epsilon = 0.90
h_conv = 2.0

params = {
    "T0": 293.15,
    "G": 1362,
    "m": 0.243,
    "alpha": 0.90,
    "A": 0.0660,
    "t_max": 4*3600,
    "N": 1000
}


# ============================================================
# 2. PARÂMETROS DA SIMULAÇÃO
# ============================================================

a = 0
b = params["t_max"]
N = params["N"]

h = (b-a)/N

tpontos = np.arange(a, b, h)


# ============================================================
# 3. FUNÇÕES DEPENDENTES DO TEMPO
# ============================================================

def Tamb(t):
    return 293.15 + 5*np.sin(2*np.pi*t/86400)


def phi(t):
    return np.pi/6


# ============================================================
# 4. EQUAÇÃO DIFERENCIAL
# ============================================================

def f(T, t):

    m = params["m"]
    A = params["A"]
    alpha = params["alpha"]
    G = params["G"]

    termo_solar = (
        tau*A*alpha*kappa*G*np.cos(phi(t))
    )

    termo_radiacao = (
        -tau*epsilon*A*sigma*(T**4 - Tamb(t)**4)
    )

    termo_conveccao = (
        h_conv*A*(Tamb(t) - T)
    )

    dTdt = (
        termo_solar +
        termo_radiacao +
        termo_conveccao
    )/(m*c1)

    return dTdt


# ============================================================
# 5. INTEGRAÇÃO RK4
# ============================================================

def calcular_temperatura():

    Tpontos = []

    T = params["T0"]

    for t in tpontos:

        Tpontos.append(T)

        k1 = h*f(T, t)

        k2 = h*f(T + 0.5*k1, t + 0.5*h)

        k3 = h*f(T + 0.5*k2, t + 0.5*h)

        k4 = h*f(T + k3, t + h)

        T += (k1 + 2*k2 + 2*k3 + k4)/6

    Tpontos = np.array(Tpontos)

    Tpontos_C = Tpontos - 273.15

    return Tpontos, Tpontos_C


Tpontos, Tpontos_C = calcular_temperatura()


# ============================================================
# 6. CORES
# ============================================================

cmap = cm.get_cmap("coolwarm")

norm = colors.Normalize(
    vmin=20,
    vmax=180
)


# ============================================================
# 7. GEOMETRIA DO REFLETOR PARABÓLICO
# ============================================================

n = np.array([0.35, 0.936])
n = n/np.linalg.norm(n)

v = np.array([-n[1], n[0]])

focal = 1.15

u = np.linspace(-1.45, 1.45, 200)

parabola = (
    np.outer(u, v) +
    np.outer(u**2/(4*focal), n)
)

focus = focal*n

u_raios = np.linspace(-1.2, 1.2, 7)

pontos_impacto = []

for ur in u_raios:

    ponto = (
        ur*v +
        (ur**2/(4*focal))*n
    )

    pontos_impacto.append(ponto)

pontos_impacto = np.array(pontos_impacto)


# ============================================================
# 8. FIGURA
# ============================================================

fig, (ax_forno, ax_grafico) = plt.subplots(
    1, 2,
    figsize=(14, 8)
)

plt.subplots_adjust(
    left=0.07,
    right=0.96,
    top=0.87,
    bottom=0.36,
    wspace=0.30
)

fig.suptitle(
    "Aquecimento de uma panela em um forno solar",
    fontsize=16,
    fontweight="bold"
)


# ============================================================
# 9. CENA DO FORNO SOLAR
# ============================================================

ax_forno.set_xlim(-3.0, 3.0)
ax_forno.set_ylim(-2.2, 4.3)

ax_forno.set_aspect("equal")
ax_forno.axis("off")

ax_forno.set_title(
    "Concentração da radiação solar",
    fontsize=13
)


# ------------------------------------------------------------
# SOL
# ------------------------------------------------------------

sol = Circle(
    (2.15, 3.55),
    0.38,
    facecolor="#FFD700",
    edgecolor="#F39C12",
    linewidth=2,
    zorder=5
)

ax_forno.add_patch(sol)

halo = Circle(
    (2.15, 3.55),
    0.50,
    facecolor="#F9E79F",
    edgecolor="none",
    alpha=0.25,
    zorder=4
)

ax_forno.add_patch(halo)


# ------------------------------------------------------------
# REFLETOR PARABÓLICO
# ------------------------------------------------------------

refletor, = ax_forno.plot(
    parabola[:, 0],
    parabola[:, 1],
    color="#7F8C8D",
    linewidth=7,
    solid_capstyle="round",
    zorder=2
)

ax_forno.plot(
    parabola[:, 0],
    parabola[:, 1],
    color="#D5D8DC",
    linewidth=3,
    zorder=3
)


# ------------------------------------------------------------
# SUPORTE DO REFLETOR
# ------------------------------------------------------------

vertices_suporte = [
    (-0.10, 0.05),
    (-0.60, -1.45),
    (-0.42, -1.45),
    (0.10, -0.05)
]

suporte = Polygon(
    vertices_suporte,
    closed=True,
    facecolor="#566573",
    edgecolor="#34495E",
    linewidth=1.5,
    zorder=1
)

ax_forno.add_patch(suporte)

base = Rectangle(
    (-1.1, -1.55),
    1.3,
    0.13,
    facecolor="#34495E",
    edgecolor="none",
    zorder=1
)

ax_forno.add_patch(base)


# ============================================================
# 10. RAIOS SOLARES
# ============================================================

raios = []
particulas = []

for i, ponto in enumerate(pontos_impacto):

    inicio = ponto + 2.5*n

    ax_forno.plot(
        [inicio[0], ponto[0]],
        [inicio[1], ponto[1]],
        color="#F5B041",
        linewidth=1.2,
        alpha=0.55,
        zorder=2
    )

    ax_forno.plot(
        [ponto[0], focus[0]],
        [ponto[1], focus[1]],
        color="#F39C12",
        linewidth=1.2,
        alpha=0.65,
        zorder=4
    )

    caminho = np.array([
        inicio,
        ponto,
        focus
    ])

    comprimento1 = np.linalg.norm(ponto-inicio)

    comprimento2 = np.linalg.norm(focus-ponto)

    total = comprimento1 + comprimento2

    particula, = ax_forno.plot(
        [],
        [],
        marker="o",
        markersize=4,
        color="#F39C12",
        linestyle="None",
        zorder=6
    )

    raios.append({
        "caminho": caminho,
        "comprimento1": comprimento1,
        "total": total
    })

    particulas.append(particula)


# ============================================================
# 11. PANELA
# ============================================================

panela = Polygon(
    [
        [focus[0]-0.43, focus[1]-0.65],
        [focus[0]+0.43, focus[1]-0.65],
        [focus[0]+0.34, focus[1]-0.05],
        [focus[0]-0.34, focus[1]-0.05]
    ],
    closed=True,
    facecolor=cmap(norm(params["T0"]-273.15)),
    edgecolor="#34495E",
    linewidth=2,
    zorder=7
)

ax_forno.add_patch(panela)

tampa = Ellipse(
    (focus[0], focus[1]-0.05),
    0.68,
    0.17,
    facecolor="#BDC3C7",
    edgecolor="#34495E",
    linewidth=1.5,
    zorder=8
)

ax_forno.add_patch(tampa)

for sinal in [-1, 1]:

    alca = Ellipse(
        (
            focus[0]+sinal*0.45,
            focus[1]-0.18
        ),
        0.30,
        0.15,
        facecolor="none",
        edgecolor="#34495E",
        linewidth=3,
        zorder=6
    )

    ax_forno.add_patch(alca)


# ============================================================
# 12. TERMÔMETRO
# ============================================================

ax_forno.add_patch(
    Rectangle(
        (2.0, -0.55),
        0.16,
        1.85,
        facecolor="#ECF0F1",
        edgecolor="#34495E",
        linewidth=1.5,
        zorder=8
    )
)

ax_forno.add_patch(
    Circle(
        (2.08, -0.55),
        0.14,
        facecolor="#ECF0F1",
        edgecolor="#34495E",
        linewidth=1.5,
        zorder=8
    )
)

termometro = Rectangle(
    (2.045, -0.55),
    0.07,
    1.85,
    facecolor="#E74C3C",
    edgecolor="none",
    zorder=9
)

bulbo = Circle(
    (2.08, -0.55),
    0.10,
    facecolor="#E74C3C",
    edgecolor="none",
    zorder=9
)

ax_forno.add_patch(termometro)
ax_forno.add_patch(bulbo)


# ============================================================
# 13. TEXTOS
# ============================================================

texto_temp = ax_forno.text(
    focus[0],
    focus[1]-1.0,
    "",
    ha="center",
    fontsize=14,
    fontweight="bold"
)

texto_amb = ax_forno.text(
    0,
    -1.9,
    "",
    ha="center",
    fontsize=10,
    color="gray"
)

vapor = []

for i in range(3):

    linha, = ax_forno.plot(
        [],
        [],
        color="gray",
        linewidth=2,
        alpha=0.0,
        zorder=9
    )

    vapor.append(linha)


# ============================================================
# 14. GRÁFICO DE TEMPERATURA
# ============================================================

ax_grafico.set_title(
    "Evolução da temperatura",
    fontsize=13
)

ax_grafico.set_xlabel("Tempo (h)")
ax_grafico.set_ylabel("Temperatura (°C)")

ax_grafico.set_xlim(
    0,
    params["t_max"]/3600
)

ax_grafico.set_ylim(
    min(0, np.min(Tpontos_C)-5),
    max(120, np.max(Tpontos_C)+10)
)

ax_grafico.grid(alpha=0.3)

linha_temp, = ax_grafico.plot(
    [],
    [],
    color="#E74C3C",
    linewidth=2.5,
    label="RK4"
)

ponto_grafico, = ax_grafico.plot(
    [],
    [],
    "o",
    color="#E74C3C",
    markersize=7
)

ax_grafico.axhline(
    60,
    color="#2980B9",
    linestyle="--",
    alpha=0.7,
    label="60 °C"
)

ax_grafico.axhline(
    100,
    color="#27AE60",
    linestyle=":",
    alpha=0.7,
    label="100 °C"
)

ax_grafico.legend(loc="best")


# ============================================================
# 15. HUD
# ============================================================

hud = fig.text(
    0.52,
    0.92,
    "",
    ha="center",
    fontsize=11
)


# ============================================================
# 16. ESTADO DA ANIMAÇÃO
# ============================================================

estado = {
    "T": Tpontos,
    "T_C": Tpontos_C,
    "indice": 0
}


# ============================================================
# 17. ATUALIZAÇÃO DA ANIMAÇÃO
# ============================================================

def update(frame):

    T = estado["T"]
    T_C = estado["T_C"]

    indice = min(frame, len(tpontos)-1)

    temperatura = T[indice]
    temperatura_C = T_C[indice]

    tempo = tpontos[indice]

    temperatura_amb = Tamb(tempo)-273.15

    cor = cmap(norm(temperatura_C))

    # PANELA

    panela.set_facecolor(cor)

    texto_temp.set_text(
        f"{temperatura_C:.1f} °C"
    )

    texto_temp.set_color(cor)

    texto_amb.set_text(
        f"Ambiente: {temperatura_amb:.1f} °C"
    )

    # TERMÔMETRO

    altura = np.clip(
        (temperatura_C-temperatura_amb)/
        (180-temperatura_amb),
        0.03,
        1
    )

    termometro.set_height(1.85*altura)

    # MOVIMENTO DOS RAIOS

    for i, raio in enumerate(raios):

        fase = (
            frame*0.035 + i/len(raios)
        ) % 1.0

        distancia = fase*raio["total"]

        caminho = raio["caminho"]

        if distancia <= raio["comprimento1"]:

            fracao = (
                distancia/raio["comprimento1"]
            )

            posicao = (
                caminho[0] +
                fracao*(caminho[1]-caminho[0])
            )

        else:

            fracao = (
                (distancia-raio["comprimento1"])/
                (raio["total"]-raio["comprimento1"])
            )

            posicao = (
                caminho[1] +
                fracao*(caminho[2]-caminho[1])
            )

        particulas[i].set_data(
            [posicao[0]],
            [posicao[1]]
        )

    # VAPOR

    intensidade = np.clip(
        (temperatura_C-70)/40,
        0,
        1
    )

    for i, linha in enumerate(vapor):

        fase = tempo*0.0018+i*2.1

        x = (
            focus[0] +
            0.15*np.sin(
                np.linspace(0, 2*np.pi, 30)+fase
            ) +
            (i-1)*0.16
        )

        y = (
            focus[1]+
            np.linspace(0.05, 0.75, 30)
        )

        linha.set_data(x, y)

        linha.set_alpha(intensidade*0.55)

    # GRÁFICO

    linha_temp.set_data(
        tpontos[:indice+1]/3600,
        T_C[:indice+1]
    )

    ponto_grafico.set_data(
        [tempo/3600],
        [temperatura_C]
    )

    # HUD

    hud.set_text(
        f"Tempo: {tempo/3600:.2f} h     "
        f"Temperatura: {temperatura_C:.2f} °C"
    )

    return (
        panela,
        termometro,
        bulbo,
        texto_temp,
        texto_amb,
        hud,
        linha_temp,
        ponto_grafico,
        *particulas,
        *vapor
    )


# ============================================================
# 18. SLIDERS
# ============================================================

ax_T0 = plt.axes([0.18, 0.29, 0.65, 0.022])
ax_G = plt.axes([0.18, 0.245, 0.65, 0.022])

ax_m = plt.axes([0.18, 0.20, 0.65, 0.022])
ax_alpha = plt.axes([0.18, 0.155, 0.65, 0.022])
ax_A = plt.axes([0.18, 0.11, 0.65, 0.022])


slider_T0 = Slider(
    ax_T0,
    "T inicial (°C)",
    10,
    60,
    valinit=params["T0"]-273.15,
    valstep=1
)

slider_G = Slider(
    ax_G,
    "Irradiância (W/m²)",
    500,
    1400,
    valinit=params["G"],
    valstep=10
)

slider_m = Slider(
    ax_m,
    "Massa m (kg)",
    0.05,
    1.0,
    valinit=params["m"],
    valstep=0.005
)

slider_alpha = Slider(
    ax_alpha,
    "Absorvidade α",
    0.0,
    1.0,
    valinit=params["alpha"],
    valstep=0.01
)

slider_A = Slider(
    ax_A,
    "Área A (m²)",
    0.01,
    0.15,
    valinit=params["A"],
    valstep=0.001
)


# ============================================================
# 19. REINICIALIZAÇÃO
# ============================================================

def atualizar(val):

    params["T0"] = slider_T0.val + 273.15
    params["G"] = slider_G.val

    params["m"] = slider_m.val
    params["alpha"] = slider_alpha.val
    params["A"] = slider_A.val

    # Recalcula a solução usando RK4

    novo_T, novo_T_C = calcular_temperatura()

    estado["T"] = novo_T
    estado["T_C"] = novo_T_C

    # Atualiza limites do gráfico

    ax_grafico.set_ylim(
        min(0, np.min(novo_T_C)-5),
        max(120, np.max(novo_T_C)+10)
    )

    # Reinicia animação

    ani.event_source.stop()

    ani.frame_seq = ani.new_frame_seq()

    update(0)

    fig.canvas.draw_idle()

    ani.event_source.start()


slider_T0.on_changed(atualizar)
slider_G.on_changed(atualizar)

slider_m.on_changed(atualizar)
slider_alpha.on_changed(atualizar)
slider_A.on_changed(atualizar)


# ============================================================
# 20. ANIMAÇÃO
# ============================================================

ani = FuncAnimation(
    fig,
    update,
    frames=len(tpontos),
    interval=30,
    blit=False,
    repeat=False
)

plt.show()
