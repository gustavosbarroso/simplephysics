import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


# ============================================================
# PARÂMETROS
# ============================================================

params = {
    "n1": 1.5,
    "n2": 1.0,
    "theta1": 30.0
}


# ============================================================
# RESOLUÇÃO DA LEI DE SNELL
# ============================================================

def solve(params):

    n1 = params["n1"]
    n2 = params["n2"]
    theta1 = params["theta1"]

    theta1_rad = np.radians(theta1)

    # Lei de Snell
    sin_theta2 = (n1 / n2) * np.sin(theta1_rad)


    # ========================================================
    # ÂNGULO CRÍTICO
    # ========================================================

    if n1 > n2:

        theta_critico = np.degrees(
            np.arcsin(n2 / n1)
        )

    else:

        theta_critico = None


    # ========================================================
    # CLASSIFICAÇÃO DO CASO
    # ========================================================

    if theta_critico is None:

        theta2 = np.degrees(
            np.arcsin(
                np.clip(sin_theta2, -1, 1)
            )
        )

        caso = "refracao"


    else:

        tolerancia = 0.05

        # ----------------------------------------------------
        # REFRAÇÃO
        # ----------------------------------------------------

        if theta1 < theta_critico - tolerancia:

            theta2 = np.degrees(
                np.arcsin(
                    np.clip(sin_theta2, -1, 1)
                )
            )

            caso = "refracao"


        # ----------------------------------------------------
        # ÂNGULO CRÍTICO
        # ----------------------------------------------------

        elif abs(theta1 - theta_critico) <= tolerancia:

            theta2 = 90.0

            caso = "critico"


        # ----------------------------------------------------
        # REFLEXÃO TOTAL INTERNA
        # ----------------------------------------------------

        else:

            theta2 = None

            caso = "rti"


    return (
        theta1,
        theta2,
        theta_critico,
        sin_theta2,
        caso
    )


# ============================================================
# FIGURA
# ============================================================

fig, ax = plt.subplots(figsize=(8, 7))

plt.subplots_adjust(
    left=0.25,
    bottom=0.30
)


# ============================================================
# HUD
# ============================================================

text_info = fig.text(
    0.02,
    0.62,
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
    y2,
    color
):

    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->",
            color=color,
            lw=2
        )
    )


# ============================================================
# DESENHA OS ÂNGULOS
# ============================================================

def draw_angles():

    theta1 = params["theta1"]
    theta1_rad = np.radians(theta1)

    radius = 0.50


    # ========================================================
    # ÂNGULO DE INCIDÊNCIA θ₁
    #
    # Fica ACIMA da interface e à ESQUERDA da normal.
    # ========================================================

    # Direção da normal para cima
    normal_superior = np.pi / 2

    # Direção do raio incidente:
    # π/2 + θ1
    raio_incidente = (
        normal_superior +
        theta1_rad
    )

    angulos = np.linspace(
        normal_superior,
        raio_incidente,
        80
    )

    x_arc = radius * np.cos(angulos)
    y_arc = radius * np.sin(angulos)

    ax.plot(
        x_arc,
        y_arc,
        color="blue",
        lw=2
    )

    # Posição do texto
    ax.text(
        -0.95,
        0.45,
        rf"$\theta_1={theta1:.1f}^\circ$",
        color="blue",
        fontsize=11
    )


    # ========================================================
    # ÂNGULO DE REFRAÇÃO θ₂
    #
    # Fica ABAIXO da interface e à DIREITA da normal.
    # ========================================================

    if caso == "refracao":

        theta2_rad = np.radians(theta2)

        # Normal apontando para baixo
        normal_inferior = -np.pi / 2

        # Raio refratado está à direita da normal
        raio_refratado = (
            normal_inferior +
            theta2_rad
        )

        angulos = np.linspace(
            normal_inferior,
            raio_refratado,
            80
        )

        x_arc = radius * np.cos(angulos)
        y_arc = radius * np.sin(angulos)

        ax.plot(
            x_arc,
            y_arc,
            color="red",
            lw=2
        )

        # Posição do texto
        ax.text(
            0.55,
            -0.55,
            rf"$\theta_2={theta2:.1f}^\circ$",
            color="red",
            fontsize=11
        )


    # ========================================================
    # ÂNGULO CRÍTICO
    #
    # Não desenha arco nem texto no gráfico.
    # O valor aparece somente no HUD.
    # ========================================================

    elif caso == "critico":

        pass


    # ========================================================
    # REFLEXÃO TOTAL INTERNA
    #
    # O raio refletido fica acima da interface,
    # à direita da normal.
    # ========================================================

    elif caso == "rti":

        # Normal apontando para cima
        normal_superior = np.pi / 2

        # Raio refletido
        raio_refletido = (
            normal_superior -
            theta1_rad
        )

        angulos = np.linspace(
            raio_refletido,
            normal_superior,
            80
        )

        x_arc = radius * np.cos(angulos)
        y_arc = radius * np.sin(angulos)

        ax.plot(
            x_arc,
            y_arc,
            color="orange",
            lw=2
        )

        # Posição do texto
        ax.text(
            0.55,
            0.45,
            rf"$\theta_r={theta1:.1f}^\circ$",
            color="orange",
            fontsize=11
        )


# ============================================================
# DESENHO PRINCIPAL
# ============================================================

def draw():

    global theta2
    global theta_critico
    global sin_theta2
    global caso

    ax.clear()


    # ========================================================
    # RESOLVE
    # ========================================================

    (
        theta1,
        theta2,
        theta_critico,
        sin_theta2,
        caso
    ) = solve(params)


    theta1_rad = np.radians(theta1)


    # ========================================================
    # INTERFACE ENTRE OS MEIOS
    # ========================================================

    ax.axhline(
        0,
        color="black",
        lw=2
    )


    # ========================================================
    # NORMAL
    # ========================================================

    ax.axvline(
        0,
        color="gray",
        linestyle="--",
        lw=1.5
    )


    # ========================================================
    # MEIO 1
    # ========================================================

    ax.fill_between(
        [-2, 2],
        0,
        2,
        color="lightblue",
        alpha=0.3
    )


    # ========================================================
    # MEIO 2
    # ========================================================

    ax.fill_between(
        [-2, 2],
        -2,
        0,
        color="lightgreen",
        alpha=0.3
    )


    # ========================================================
    # TEXTOS DOS MEIOS
    # ========================================================

    ax.text(
        -1.85,
        1.75,
        rf"Meio 1: $n_1={params['n1']:.2f}$",
        fontsize=11
    )

    ax.text(
        -1.85,
        -1.75,
        rf"Meio 2: $n_2={params['n2']:.2f}$",
        fontsize=11
    )


    # ========================================================
    # RAIO INCIDENTE
    # ========================================================

    L = 2.0

    x_inc = np.linspace(
        -L * np.sin(theta1_rad),
        0,
        100
    )

    y_inc = np.linspace(
        L * np.cos(theta1_rad),
        0,
        100
    )

    ax.plot(
        x_inc,
        y_inc,
        color="blue",
        lw=2.5,
        label="Incidente"
    )


    # Seta do incidente

    draw_arrow(
        x_inc[20],
        y_inc[20],
        x_inc[40],
        y_inc[40],
        "blue"
    )


    # ========================================================
    # RAIO REFRATADO
    # ========================================================

    if caso == "refracao":

        theta2_rad = np.radians(theta2)

        x_ref = np.linspace(
            0,
            L * np.sin(theta2_rad),
            100
        )

        y_ref = np.linspace(
            0,
            -L * np.cos(theta2_rad),
            100
        )

        ax.plot(
            x_ref,
            y_ref,
            color="red",
            lw=2.5,
            label="Refratado"
        )


        # Seta do refratado

        draw_arrow(
            x_ref[35],
            y_ref[35],
            x_ref[55],
            y_ref[55],
            "red"
        )


    # ========================================================
    # ÂNGULO CRÍTICO
    # ========================================================

    elif caso == "critico":

        # θ₂ = 90°
        # O raio segue pela interface.

        x_ref = np.linspace(
            0,
            L,
            100
        )

        y_ref = np.zeros_like(x_ref)

        ax.plot(
            x_ref,
            y_ref,
            color="red",
            lw=2.5,
            label="Raio crítico"
        )


        # Seta

        draw_arrow(
            x_ref[35],
            y_ref[35],
            x_ref[55],
            y_ref[55],
            "red"
        )


    # ========================================================
    # REFLEXÃO TOTAL INTERNA
    # ========================================================

    elif caso == "rti":

        x_ref = np.linspace(
            0,
            L * np.sin(theta1_rad),
            100
        )

        y_ref = np.linspace(
            0,
            L * np.cos(theta1_rad),
            100
        )

        ax.plot(
            x_ref,
            y_ref,
            color="orange",
            lw=2.5,
            linestyle="--",
            label="Refletido"
        )


        # Seta do refletido

        draw_arrow(
            x_ref[35],
            y_ref[35],
            x_ref[55],
            y_ref[55],
            "orange"
        )


    # ========================================================
    # PONTO DE INCIDÊNCIA
    # ========================================================

    ax.plot(
        0,
        0,
        "ko",
        markersize=5
    )


    # ========================================================
    # ÂNGULOS
    # ========================================================

    draw_angles()


    # ========================================================
    # CONFIGURAÇÕES
    # ========================================================

    ax.set_xlim(
        -2,
        2
    )

    ax.set_ylim(
        -2,
        2
    )

    ax.set_aspect(
        "equal"
    )

    ax.set_xlabel(
        "x"
    )

    ax.set_ylabel(
        "y"
    )

    ax.set_title(
        "Lei de Snell"
    )

    ax.grid(
        alpha=0.3
    )

    ax.legend()


    # ========================================================
    # HUD
    # ========================================================

    if theta_critico is None:

        texto = (
            f"n₁ = {params['n1']:.2f}\n"
            f"n₂ = {params['n2']:.2f}\n"
            f"θ₁ = {theta1:.2f}°\n"
            f"θ₂ = {theta2:.2f}°\n\n"
            "Não existe ângulo crítico\n"
            "para n₁ ≤ n₂."
        )


    elif caso == "refracao":

        texto = (
            f"n₁ = {params['n1']:.2f}\n"
            f"n₂ = {params['n2']:.2f}\n"
            f"θ₁ = {theta1:.2f}°\n"
            f"θ₂ = {theta2:.2f}°\n"
            f"θ crítico = {theta_critico:.2f}°\n\n"
            "Refração"
        )


    elif caso == "critico":

        texto = (
            f"n₁ = {params['n1']:.2f}\n"
            f"n₂ = {params['n2']:.2f}\n"
            f"θ₁ = {theta1:.2f}°\n"
            f"θ crítico = {theta_critico:.2f}°\n\n"
            "ÂNGULO CRÍTICO\n"
            "θ₂ = 90°"
        )


    else:

        texto = (
            f"n₁ = {params['n1']:.2f}\n"
            f"n₂ = {params['n2']:.2f}\n"
            f"θ₁ = {theta1:.2f}°\n"
            f"θ crítico = {theta_critico:.2f}°\n\n"
            "REFLEXÃO TOTAL INTERNA"
        )


    text_info.set_text(
        texto
    )

    fig.canvas.draw_idle()


# ============================================================
# SLIDERS
# ============================================================

ax_n1 = plt.axes(
    [0.25, 0.20, 0.65, 0.03]
)

ax_n2 = plt.axes(
    [0.25, 0.14, 0.65, 0.03]
)

ax_theta = plt.axes(
    [0.25, 0.08, 0.65, 0.03]
)


slider_n1 = Slider(
    ax_n1,
    "n₁",
    1.0,
    2.5,
    valinit=params["n1"],
    valstep=0.1
)


slider_n2 = Slider(
    ax_n2,
    "n₂",
    1.0,
    2.5,
    valinit=params["n2"],
    valstep=0.1
)


slider_theta = Slider(
    ax_theta,
    "θ₁ (°)",
    0,
    89,
    valinit=params["theta1"],
    valstep=0.1
)


# ============================================================
# ATUALIZAÇÃO DOS SLIDERS
# ============================================================

def update_sliders(val):

    params["n1"] = slider_n1.val
    params["n2"] = slider_n2.val
    params["theta1"] = slider_theta.val

    draw()


# ============================================================
# EVENTOS
# ============================================================

slider_n1.on_changed(
    update_sliders
)

slider_n2.on_changed(
    update_sliders
)

slider_theta.on_changed(
    update_sliders
)


# ============================================================
# DESENHO INICIAL
# ============================================================

draw()

plt.show()
