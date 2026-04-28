import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

mu0 = 4*np.pi*1e-7

# ---------------------------
# CAMPO MAGNÉTICO (fio infinito)
# ---------------------------
def campo_magnetico(X, Y, I):
    r = np.sqrt(X**2 + Y**2)
    r[r == 0] = 1e-6

    B = mu0 * I / (2*np.pi*r)

    Bx = -Y / r * B
    By = X / r * B

    return Bx, By, B

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.25)

# grid fixo
x = np.linspace(-5, 5, 80)
y = np.linspace(-5, 5, 80)
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

    I = slider_I.val
    r_destaque = slider_r.val

    # =========================
    # CAMPO MAGNÉTICO
    # =========================
    Bx, By, B = campo_magnetico(X, Y, I)

    ax1.streamplot(X, Y, Bx, By, density=1.5, color='black')

    # fio
    ax1.plot(0, 0, 'o', color='red', markersize=10)

    # ponto de observação
    ax1.plot(r_destaque, 0, 'bo')
    ax1.text(r_destaque, 0, " r", color='blue')

    ax1.set_title("Linhas de campo magnético")
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal')

    # =========================
    # GRÁFICO B(r)
    # =========================
    r_vals = np.linspace(0.1, 5, 200)
    B_vals = mu0 * I / (2*np.pi*r_vals) * 1e6

    ax2.plot(r_vals, B_vals, label="Analítico")

    B_r = mu0 * I / (2*np.pi*r_destaque) * 1e6

    ax2.plot(r_destaque, B_r, 'ro')
    ax2.axvline(r_destaque, linestyle='--', color='gray')

    ax2.set_xlabel("r (m)")
    ax2.set_ylabel("B (μT)")
    ax2.set_title("Campo magnético B(r)")
    ax2.grid()
    ax2.legend()

    # HUD
    texto = (
        f"I = {I:.2f} A\n"
        f"r = {r_destaque:.2f} m\n"
        f"B = {B_r:.2f} μT"
    )
    text_info.set_text(texto)

    fig.canvas.draw_idle()

# ---------------------------
# SLIDERS
# ---------------------------
ax_I = plt.axes([0.2, 0.12, 0.65, 0.03])
ax_r = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_I = Slider(ax_I, 'I (A)', -10, 10, valinit=1)
slider_r = Slider(ax_r, 'r (m)', 0.1, 5.0, valinit=1)

slider_I.on_changed(update)
slider_r.on_changed(update)

# inicial
update(None)

plt.show()
