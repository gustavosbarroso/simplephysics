import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, RadioButtons


# ============================================================
# CONSTANTE
# ============================================================

epsilon0 = 8.85e-12


# ============================================================
# PARÂMETROS
# ============================================================

params = {
    "sign1": 1,
    "sign2": -1,
    "sigma_nC": 1.0,
    "A": 1.0,
    "d": 1.0
}


# ============================================================
# RESOLUÇÃO DO CAPACITOR
# ============================================================

def solve(params):

    sign1 = params["sign1"]
    sign2 = params["sign2"]

    sigma_nC = params["sigma_nC"]
    A = params["A"]
    d = params["d"]

    # --------------------------------------------------------
    # Conversão: nC/m² → C/m²
    # --------------------------------------------------------

    sigma = sigma_nC * 1e-9

    # Placa 1 = superior
    # Placa 2 = inferior

    sigma1 = sign1 * sigma
    sigma2 = sign2 * sigma

    # --------------------------------------------------------
    # Campos individuais das placas
    # --------------------------------------------------------

    E1 = sigma1 / (2 * epsilon0)
    E2 = sigma2 / (2 * epsilon0)

    # --------------------------------------------------------
    # Campo resultante entre as placas
    #
    # Placa 1 está em y = +d/2
    # Placa 2 está em y = -d/2
    #
    # Convenção:
    # +y = para cima
    #
    # Entre as placas:
    # campo da placa 1 -> para baixo
    # campo da placa 2 -> para cima
    #
    # Portanto:
    # E = E2 - E1
    # --------------------------------------------------------

    E_between = E2 - E1

    # --------------------------------------------------------
    # CAPACITÂNCIA
    #
    # A configuração só é considerada um capacitor quando
    # as placas possuem sinais opostos.
    # --------------------------------------------------------

    if sign1 != sign2:
        C = epsilon0 * A / d
    else:
        C = 0.0

    # --------------------------------------------------------
    # DIFERENÇA DE POTENCIAL
    #
    # V = V_inferior - V_superior
    #
    # V = E*d
    # --------------------------------------------------------

    V = E_between * d

    # --------------------------------------------------------
    # ENERGIA ARMAZENADA
    # --------------------------------------------------------

    U = 0.5 * C * V**2

    # --------------------------------------------------------
    # Campo para o gráfico
    # --------------------------------------------------------

    y = np.linspace(
        -1.5 * d,
        1.5 * d,
        300
    )

    E_values = np.zeros_like(y)

    dentro = (
        (y > -d / 2) &
        (y < d / 2)
    )

    E_values[dentro] = E_between

    return (
        sigma,
        E1,
        E2,
        E_between,
        C,
        V,
        U,
        y,
        E_values
    )


# ============================================================
# FIGURA
# ============================================================

fig, (ax_field, ax_cap) = plt.subplots(
    1,
    2,
    figsize=(11, 6),
    gridspec_kw={
        "width_ratios": [1.2, 2]
    }
)

plt.subplots_adjust(
    left=0.25,
    bottom=0.32,
    right=0.95,
    wspace=0.35
)


# ============================================================
# HUD
# ============================================================

text_info = fig.text(
    0.02,
    0.70,
    "",
    fontsize=10,
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=0.85
    )
)


# ============================================================
# SETA
# ============================================================

def draw_arrow(
    x1,
    y1,
    x2,
    y2
):

    ax_cap.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->",
            lw=2
        )
    )


# ============================================================
# DESENHO PRINCIPAL
# ============================================================

def draw():

    global sigma
    global E1
    global E2
    global E_between
    global C
    global V
    global U
    global y
    global E_values

    ax_field.clear()
    ax_cap.clear()

    (
        sigma,
        E1,
        E2,
        E_between,
        C,
        V,
        U,
        y,
        E_values
    ) = solve(params)

    d = params["d"]

    # ========================================================
    # CAMPO ELÉTRICO
    # ========================================================

    ax_field.plot(
        y,
        E_values,
        lw=2
    )

    # Posição das placas

    ax_field.axvline(
        -d / 2,
        linestyle="--"
    )

    ax_field.axvline(
        d / 2,
        linestyle="--"
    )

    ax_field.set_xlim(
        -1.5 * d,
        1.5 * d
    )

    E_max = max(
        abs(E_between),
        1
    )

    ax_field.set_ylim(
        -1.2 * E_max,
        1.2 * E_max
    )

    ax_field.set_xlabel(
        "posição (m)"
    )

    ax_field.set_ylabel(
        "E (N/C)"
    )

    ax_field.set_title(
        "Campo Resultante"
    )

    ax_field.grid(
        alpha=0.3
    )

    # ========================================================
    # CAPACITOR
    # ========================================================

    margin = 0.5 * d

    ax_cap.set_xlim(
        -d,
        d
    )

    ax_cap.set_ylim(
        -d / 2 - margin,
        d / 2 + margin
    )

    ax_cap.set_aspect(
        "equal"
    )

    # --------------------------------------------------------
    # Placas
    # --------------------------------------------------------

    ax_cap.axhline(
        d / 2,
        linewidth=4
    )

    ax_cap.axhline(
        -d / 2,
        linewidth=4
    )

    # --------------------------------------------------------
    # Sinais
    # --------------------------------------------------------

    ax_cap.text(
        -0.90 * d,
        d / 2,
        "+" if params["sign1"] > 0 else "−",
        fontsize=20,
        fontweight="bold",
        ha="center",
        va="center"
    )

    ax_cap.text(
        -0.90 * d,
        -d / 2,
        "+" if params["sign2"] > 0 else "−",
        fontsize=20,
        fontweight="bold",
        ha="center",
        va="center"
    )

    # ========================================================
    # LINHAS DE CAMPO
    # ========================================================

    if abs(E_between) > 1e-15:

        x_positions = np.linspace(
            -0.8 * d,
            0.8 * d,
            7
        )

        arrow_len = 0.20 * d

        for x in x_positions:

            # Linha de campo

            ax_cap.plot(
                [x, x],
                [-d / 2, d / 2],
                lw=2
            )

            # Sentido do campo

            if E_between > 0:

                draw_arrow(
                    x,
                    0,
                    x,
                    arrow_len
                )

            else:

                draw_arrow(
                    x,
                    0,
                    x,
                    -arrow_len
                )

    # ========================================================
    # CONFIGURAÇÕES DO GRÁFICO
    # ========================================================

    ax_cap.set_xlabel(
        "x (m)"
    )

    ax_cap.set_ylabel(
        "y (m)"
    )

    ax_cap.set_title(
        "Linhas de Campo"
    )

    ax_cap.grid(
        alpha=0.3
    )

    # ========================================================
    # HUD
    # ========================================================

    C_nF = C * 1e9

    if params["sign1"] == params["sign2"]:

        texto = (
            "Configuração:\n\n"
            "Placas com mesmo sinal\n\n"
            "E = 0 N/C\n\n"
            "C = 0 nF\n\n"
            "ΔV = 0 V\n\n"
            "U = 0 J"
        )

    else:

        texto = (
            "Resultados:\n\n"
            f"σ = {params['sigma_nC']:.2f} nC/m²\n\n"
            f"E = {E_between:.2e} N/C\n\n"
            f"C = {C_nF:.2f} nF\n\n"
            f"ΔV = {V:.2e} V\n\n"
            f"U = {U:.2e} J"
        )

    text_info.set_text(
        texto
    )

    fig.canvas.draw_idle()


# ============================================================
# SLIDERS
# ============================================================

ax_sigma = plt.axes(
    [0.25, 0.20, 0.65, 0.03]
)

ax_A = plt.axes(
    [0.25, 0.14, 0.65, 0.03]
)

ax_d = plt.axes(
    [0.25, 0.08, 0.65, 0.03]
)


slider_sigma = Slider(
    ax_sigma,
    "σ (nC/m²)",
    0.1,
    10.0,
    valinit=params["sigma_nC"],
    valstep=0.1
)


slider_A = Slider(
    ax_A,
    "A (m²)",
    0.1,
    10.0,
    valinit=params["A"],
    valstep=0.1
)


slider_d = Slider(
    ax_d,
    "d (m)",
    0.1,
    5.0,
    valinit=params["d"],
    valstep=0.1
)


# ============================================================
# RADIO BUTTONS — PLACA 1
# ============================================================

ax_radio1 = plt.axes(
    [0.02, 0.16, 0.10, 0.12]
)

radio_sign1 = RadioButtons(
    ax_radio1,
    ("+", "−"),
    active=0
)

ax_radio1.set_title(
    "Placa 1"
)


# ============================================================
# RADIO BUTTONS — PLACA 2
# ============================================================

ax_radio2 = plt.axes(
    [0.02, 0.02, 0.10, 0.12]
)

radio_sign2 = RadioButtons(
    ax_radio2,
    ("+", "−"),
    active=1
)

ax_radio2.set_title(
    "Placa 2"
)


# ============================================================
# ATUALIZAÇÃO
# ============================================================

def update_sliders(val):

    params["sigma_nC"] = slider_sigma.val

    params["A"] = slider_A.val

    params["d"] = slider_d.val

    params["sign1"] = (
        1
        if radio_sign1.value_selected == "+"
        else -1
    )

    params["sign2"] = (
        1
        if radio_sign2.value_selected == "+"
        else -1
    )

    draw()


# ============================================================
# EVENTOS
# ============================================================

slider_sigma.on_changed(
    update_sliders
)

slider_A.on_changed(
    update_sliders
)

slider_d.on_changed(
    update_sliders
)

radio_sign1.on_clicked(
    update_sliders
)

radio_sign2.on_clicked(
    update_sliders
)


# ============================================================
# DESENHO INICIAL
# ============================================================

draw()


# ============================================================
# MOSTRAR
# ============================================================

plt.show()
