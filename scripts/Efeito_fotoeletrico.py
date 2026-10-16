
# ---------------------------
# Imports
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

# ---------------------------
# Constante de Planck
# ---------------------------
h = 4.15e-15  # eV s

# ---------------------------
# Efeito fotoelétrico
# ---------------------------
def energia_cinetica(f, phi):
    fc = phi / h

    if f <= fc:
        return 0.0

    return h * f - phi


# ---------------------------
# Parâmetros iniciais
# ---------------------------
f0 = 1.2e15
phi0 = 4.1
I0 = 5.0

# ---------------------------
# Figura
# ---------------------------
fig = plt.figure(figsize=(12, 8))

gs = fig.add_gridspec(
    2, 1,
    height_ratios=[3.2, 1.2],
    hspace=0.32
)

ax = fig.add_subplot(gs[0])
axE = fig.add_subplot(gs[1])

fig.subplots_adjust(
    bottom=0.28,
    top=0.90,
    left=0.08,
    right=0.97
)

# ---------------------------
# Cena física
# ---------------------------
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.set_xticks([])
ax.set_yticks([])

ax.set_title(
    "Efeito fotoelétrico",
    fontsize=15
)

# ---------------------------
# Superfície metálica
# ---------------------------
metal = Rectangle(
    (0.5, 0.55),
    9.0, 0.65,
    facecolor="silver",
    edgecolor="dimgray",
    linewidth=1.5
)

ax.add_patch(metal)

ax.text(
    5, 0.28,
    "Superfície metálica",
    ha="center"
)

# ---------------------------
# Elétrons no metal
# ---------------------------
N_METAL = 9

eletrons_metal = []
sinais_metal = []

for ex in np.linspace(1, 9, N_METAL):

    # Elétron no metal
    p = Circle(
        (ex, 0.88),
        0.075,
        facecolor="red",
        edgecolor="darkred",
        linewidth=0.8
    )

    ax.add_patch(p)
    eletrons_metal.append(p)

    # Carga negativa
    sinal = ax.text(
        ex, 0.88,
        "−",
        color="white",
        fontsize=9,
        fontweight="bold",
        ha="center",
        va="center"
    )

    sinais_metal.append(sinal)

# ---------------------------
# Luz incidente
# ---------------------------
light_arrow = FancyArrowPatch(
    (7.6, 4.7),
    (6.5, 1.35),
    arrowstyle="-|>",
    mutation_scale=16,
    color="darkorange",
    linewidth=1.8
)

ax.add_patch(light_arrow)

ax.text(
    7.8, 4.8,
    "Luz incidente",
    color="darkorange"
)

# ---------------------------
# Fotoelétrons ejetados
# ---------------------------
N = 16

eletrons = []
sinais_menos = []

for _ in range(N):

    p = Circle(
        (0, 0),
        0.13,
        facecolor="red",
        edgecolor="darkred",
        linewidth=0.8,
        visible=False
    )

    ax.add_patch(p)
    eletrons.append(p)

    sinal = ax.text(
        0, 0,
        "−",
        color="white",
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        visible=False
    )

    sinais_menos.append(sinal)

# ---------------------------
# Informações
# ---------------------------
status = ax.text(
    0.55, 5.55,
    "",
    fontsize=11,
    fontweight="bold"
)

info = ax.text(
    0.55, 5.15,
    "",
    fontsize=10
)

# ---------------------------
# Gráfico da energia cinética
# ---------------------------
curva, = axE.plot(
    [],
    [],
    linewidth=2,
    label=r"$K_{\max}=hf-\phi$"
)

corte = axE.axvline(
    phi0 / h,
    color="red",
    linestyle="--",
    label="Frequência de corte"
)

axE.set_xlim(0, 2.5e15)
axE.set_ylim(0, 7)

axE.set_xlabel("Frequência (Hz)")
axE.set_ylabel(r"$K_{\max}$ (eV)")

axE.grid(True, alpha=0.3)
axE.legend()

# ---------------------------
# Sliders
# ---------------------------
ax_f = plt.axes([0.16, 0.19, 0.70, 0.025])

slider_f = Slider(
    ax_f,
    "Frequência (10¹⁵ Hz)",
    0, 2.5,
    valinit=f0 / 1e15,
    valstep=0.01
)

ax_phi = plt.axes([0.16, 0.14, 0.70, 0.025])

slider_phi = Slider(
    ax_phi,
    "Função trabalho (eV)",
    1, 6,
    valinit=phi0,
    valstep=0.05
)

ax_I = plt.axes([0.16, 0.09, 0.70, 0.025])

slider_I = Slider(
    ax_I,
    "Intensidade relativa",
    0, 10,
    valinit=I0,
    valstep=0.1
)

# ---------------------------
# Estado da animação
# ---------------------------
rng = np.random.default_rng()

particulas = [
    {
        "ativa": False,
        "x0": 0.0,
        "y0": 1.25,
        "vx": 0.0,
        "vy": 0.0,
        "nascimento": 0.0,
        "vida": 0.0
    }
    for _ in range(N)
]

tempo = 0.0
ultima_emissao = 0.0
indice = 0

# ---------------------------
# Animação
# ---------------------------
def animar(frame):

    global tempo, ultima_emissao, indice

    tempo += 0.04

    # ---------------------------
    # Valores dos sliders
    # ---------------------------
    f = slider_f.val * 1e15
    phi = slider_phi.val
    intensidade = slider_I.val

    fc = phi / h
    Kmax = energia_cinetica(f, phi)

    # Emissão somente acima da frequência de corte
    emissao = (
        f > fc
        and Kmax > 0
        and intensidade > 0
    )

    # ---------------------------
    # Emissão de fotoelétrons
    # ---------------------------
    if emissao:

        taxa = intensidade * 0.22

        if tempo - ultima_emissao >= 1 / max(taxa, 0.05):

            p = particulas[indice]

            p["ativa"] = True

            # Origem na superfície metálica
            p["x0"] = rng.uniform(5.7, 6.8)
            p["y0"] = 1.28

            # Direção para cima e para a esquerda
            angulo = rng.uniform(
                np.deg2rad(115),
                np.deg2rad(155)
            )

            # Velocidade visual ilustrativa
            velocidade = 0.45 + 0.38 * np.sqrt(Kmax)

            p["vx"] = velocidade * np.cos(angulo)
            p["vy"] = velocidade * np.sin(angulo)

            p["nascimento"] = tempo
            p["vida"] = rng.uniform(2.2, 3.6)

            indice = (indice + 1) % N
            ultima_emissao = tempo

    else:

        # Não deixa partículas continuarem visíveis
        # quando a emissão não é permitida.
        for i, p in enumerate(particulas):
            p["ativa"] = False
            eletrons[i].set_visible(False)
            sinais_menos[i].set_visible(False)

    # ---------------------------
    # Movimento retilíneo uniforme
    # ---------------------------
    for i, p in enumerate(particulas):

        if not p["ativa"]:
            eletrons[i].set_visible(False)
            sinais_menos[i].set_visible(False)
            continue

        idade = tempo - p["nascimento"]

        if idade > p["vida"]:

            p["ativa"] = False
            eletrons[i].set_visible(False)
            sinais_menos[i].set_visible(False)

            continue

        # Sem gravidade e sem aceleração:
        # o elétron mantém a direção e a velocidade.
        x = p["x0"] + p["vx"] * idade
        y = p["y0"] + p["vy"] * idade

        # Remove partículas fora da área visível
        if x < 0.2 or y < 1.2 or y > 5.8:

            p["ativa"] = False
            eletrons[i].set_visible(False)
            sinais_menos[i].set_visible(False)

            continue

        # Atualiza círculo e sinal de menos
        eletrons[i].center = (x, y)
        eletrons[i].set_visible(True)

        sinais_menos[i].set_position((x, y))
        sinais_menos[i].set_visible(True)

    # ---------------------------
    # Status da emissão
    # ---------------------------
    if emissao:

        status.set_text("EMISSÃO DE FOTOELÉTRONS")
        status.set_color("darkgreen")

    else:

        status.set_text("SEM EMISSÃO DE FOTOELÉTRONS")
        status.set_color("firebrick")

    info.set_text(
        f"f = {f:.2e} Hz | "
        f"fc = {fc:.2e} Hz | "
        f"Kmax = {Kmax:.2f} eV"
    )

    # ---------------------------
    # Atualiza gráfico
    # ---------------------------
    frequencias = np.linspace(0, 2.5e15, 500)

    energias = np.maximum(
        h * frequencias - phi,
        0
    )

    curva.set_data(frequencias, energias)
    corte.set_xdata([fc, fc])

    return (
        [status, info, curva, corte]
        + eletrons
        + sinais_menos
    )

# ---------------------------
# Cria animação
# ---------------------------
anim = FuncAnimation(
    fig,
    animar,
    interval=40,
    blit=False,
    cache_frame_data=False
)

# ---------------------------
# Exibição
# ---------------------------
plt.show()
