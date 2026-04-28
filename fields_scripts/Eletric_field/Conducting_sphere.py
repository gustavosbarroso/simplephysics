import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTES
# ---------------------------
epsilon0 = 8.85e-12
k = 1 / (4 * np.pi * epsilon0)

# ---------------------------
# CAMPO ELÉTRICO (esfera condutora)
# ---------------------------
def campo_eletrico(X, Y, Q, R):

    r = np.sqrt(X**2 + Y**2)
    r[r == 0] = 1e-12

    # módulo
    E = np.zeros_like(r)

    fora = r >= R
    dentro = r < R

    E[fora] = k * Q / (r[fora]**2)
    E[dentro] = 0

    # componentes
    Ex = np.zeros_like(r)
    Ey = np.zeros_like(r)

    Ex[fora] = k * Q * X[fora] / (r[fora]**3)
    Ey[fora] = k * Q * Y[fora] / (r[fora]**3)

    return Ex, Ey, E

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.25)

# grid fixo
x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)

# HUD
text_info = fig.text(0.75, 0.75, "",
                     bbox=dict(facecolor='white', alpha=0.8))

# ---------------------------
# UPDATE
# ---------------------------
def update(val):

    ax1.clear()
    ax2.clear()

    Q = slider_Q.val * 1e-9  # nC → C
    R = slider_R.val
    r_destaque = slider_r.val

    # =========================
    # CAMPO ELÉTRICO
    # =========================
    Ex, Ey, E = campo_eletrico(X, Y, Q, R)

    # normalização para streamplot
    magnitude = np.sqrt(Ex**2 + Ey**2)
    magnitude[magnitude == 0] = 1

    Ex_dir = Ex / magnitude
    Ey_dir = Ey / magnitude

    ax1.streamplot(X, Y, Ex_dir, Ey_dir, density=1.5)

    # esfera
    circle = plt.Circle((0, 0), R, color='red', alpha=0.2)
    ax1.add_patch(circle)

    # ponto de observação
    ax1.plot(r_destaque, 0, 'bo')
    ax1.text(r_destaque, 0, " r", color='blue')

    ax1.set_title("Linhas de campo elétrico")
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect('equal')

    # =========================
    # GRÁFICO E(r)
    # =========================
    r_vals = np.linspace(0.01, 3, 200)

    E_vals = np.where(r_vals >= R, k*Q/(r_vals**2), 0) * 1e-3  # escala p/ melhor visual

    ax2.plot(r_vals, E_vals, label="Analítico")

    if r_destaque >= R:
        E_r = k * Q / (r_destaque**2) * 1e-3
    else:
        E_r = 0

    ax2.plot(r_destaque, E_r, 'ro')
    ax2.axvline(r_destaque, linestyle='--', color='gray')

    ax2.set_xlabel("r (m)")
    ax2.set_ylabel("E (kN/C)")
    ax2.set_title("Campo elétrico E(r)")
    ax2.grid()
    ax2.legend()

    # HUD
    text_info.set_text(
        f"Q = {slider_Q.val:.2f} nC\n"
        f"R = {R:.2f} m\n"
        f"r = {r_destaque:.2f} m\n\n"
    )

    fig.canvas.draw_idle()

# ---------------------------
# SLIDERS
# ---------------------------
ax_Q = plt.axes([0.2, 0.12, 0.65, 0.03])
ax_R = plt.axes([0.2, 0.07, 0.65, 0.03])
ax_r = plt.axes([0.2, 0.02, 0.65, 0.03])

slider_Q = Slider(ax_Q, 'Q (nC)', -5, 5, valinit=1)
slider_R = Slider(ax_R, 'R (m)', 0.5, 2.0, valinit=1)
slider_r = Slider(ax_r, 'r (m)', 0.01, 3.0, valinit=1.5)

slider_Q.on_changed(update)
slider_R.on_changed(update)
slider_r.on_changed(update)

# inicial
update(None)

plt.show()
