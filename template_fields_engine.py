import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# =========================================================
# CONSTANTES (edite conforme o problema)
# =========================================================
C1 = 1.0  # exemplo (k, mu0, etc.)

# =========================================================
# INTEGRADOR (Simpson padrão)
# =========================================================
def integraSimpson(f, a, b, N):

    if N % 2 != 0:
        N += 1

    h = (b - a) / N
    s = f(a) + f(b)

    for i in range(1, N):
        if i % 2 == 0:
            s += 2 * f(a + i*h)
        else:
            s += 4 * f(a + i*h)

    return (h * s) / 3


# =========================================================
# FUNÇÃO FÍSICA (SUBSTITUI AQUI)
# =========================================================
def campo_no_eixo(x, params):

    # EXEMPLO genérico:
    # você vai trocar isso pela sua física real
    def integrando(xp):
        return 1 / (1 + (x - xp)**2)**(3/2)

    a, b = params["limites"]
    N = params["Nint"]

    integral = integraSimpson(integrando, a, b, N)

    return C1 * integral


# =========================================================
# FIGURA BASE (1D padrão)
# =========================================================
fig, ax = plt.subplots(figsize=(7,5))
plt.subplots_adjust(bottom=0.35)


# =========================================================
# UPDATE (núcleo do padrão)
# =========================================================
def update(val):

    ax.clear()

    # -------------------------
    # parâmetros dos sliders
    # -------------------------
    A = slider_A.val
    B = slider_B.val
    C = slider_C.val

    params = {
        "A": A,
        "B": B,
        "C": C,
        "limites": (-B/2, B/2),
        "Nint": 100
    }

    # -------------------------
    # domínio
    # -------------------------
    x_vals = np.linspace(-3, 3, 200)

    y_vals = np.array([
        campo_no_eixo(x, params)
        for x in x_vals
    ])

    # conversão visual (ex: μT, kN/C etc.)
    y_plot = y_vals * 1e6

    ax.plot(x_vals, y_plot, label="Modelo (Simpson)")

    # limites físicos (ex: corpo, fio, região)
    ax.axvline(-B/2, linestyle='--', color='gray')
    ax.axvline(B/2, linestyle='--', color='gray')

    # ponto destaque
    x0 = slider_x.val
    y0 = campo_no_eixo(x0, params) * 1e6

    ax.plot(x0, y0, 'ro')
    ax.axvline(x0, linestyle='--', color='red')

    # HUD
    ax.set_title("Campo ao longo do eixo")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Campo (unidade ajustada)")
    ax.grid()
    ax.legend()

    fig.canvas.draw_idle()


# =========================================================
# SLIDERS (PADRÃO MODULAR)
# =========================================================

ax_A = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_B = plt.axes([0.2, 0.20, 0.65, 0.03])
ax_C = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_x = plt.axes([0.2, 0.10, 0.65, 0.03])

slider_A = Slider(ax_A, 'A', 0.1, 10, valinit=1)
slider_B = Slider(ax_B, 'B (comprimento)', 0.1, 3.0, valinit=1)
slider_C = Slider(ax_C, 'C', 0.1, 5.0, valinit=1)
slider_x = Slider(ax_x, 'x ponto', -3.0, 3.0, valinit=1)

# conecta update
slider_A.on_changed(update)
slider_B.on_changed(update)
slider_C.on_changed(update)
slider_x.on_changed(update)

# inicializa
update(None)

plt.show()
