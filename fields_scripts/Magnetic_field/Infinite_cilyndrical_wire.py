import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

mu0 = 4*np.pi*1e-7

# ---------------------------
# CAMPO DO FIO CILÍNDRICO (ESTILO SOLENOIDE)
# ---------------------------
def campo_fio(X, Y, I, R):

    r = np.sqrt(X**2 + Y**2)
    r_safe = np.where(r == 0, 1e-6, r)

    B = np.zeros_like(r)

    # regiões (igual ao solenoide)
    dentro = r < R
    fora = r >= R

    # campo
    B[dentro] = (mu0 * I / (2*np.pi * R**2)) * r[dentro]
    B[fora] = (mu0 * I / (2*np.pi * r_safe[fora]))

    # componentes
    Bx = -Y / r_safe * B
    By = X / r_safe * B

    return Bx, By, B


# ---------------------------
# FIGURA
# ---------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.30)

# grid
x = np.linspace(-5, 5, 80)
y = np.linspace(-5, 5, 80)
X, Y = np.meshgrid(x, y)

# HUD
text_info = fig.text(0.72, 0.75, "",
                     bbox=dict(facecolor='white', alpha=0.8))

# ---------------------------
# UPDATE
# ---------------------------
def update(val):

    ax1.clear()
    ax2.clear()

    I = slider_I.val
    R = slider_R.val
    r_destaque = slider_r.val

    # =========================
    # CAMPO 2D
    # =========================
    Bx, By, B = campo_fio(X, Y, I, R)

    # normalização (igual ao padrão moderno)
    Bmag = np.sqrt(Bx**2 + By**2)
    Bx_plot = Bx / (Bmag + 1e-12)
    By_plot = By / (Bmag + 1e-12)

    ax1.streamplot(X, Y, Bx_plot, By_plot, density=1.4, color='black')

    # fio (cilindro)
    circle = plt.Circle((0, 0), R, color='red', alpha=0.2)
    ax1.add_artist(circle)

    ax1.plot(0, 0, 'ko')

    # ponto de observação
    ax1.plot(r_destaque, 0, 'bo')
    ax1.text(r_destaque, 0, " r", color='blue')

    ax1.set_title("Campo magnético (fio cilíndrico)")
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal')

    # =========================
    # GRÁFICO B(r)
    # =========================
    r_vals = np.linspace(0.01, 5, 200)

    B_vals = np.where(
        r_vals < R,
        (mu0 * I / (2*np.pi * R**2)) * r_vals,
        (mu0 * I / (2*np.pi * r_vals))
    ) * 1e6

    ax2.plot(r_vals, B_vals, label="Analítico")

    if r_destaque < R:
        B_r = (mu0 * I / (2*np.pi * R**2)) * r_destaque
        regime = "Interior (B ~ r)"
    else:
        B_r = mu0 * I / (2*np.pi * r_destaque)
        regime = "Exterior (B ~ 1/r)"

    ax2.plot(r_destaque, B_r * 1e6, 'ro')
    ax2.axvline(R, linestyle='--', color='red', label='Raio R')

    ax2.set_xlabel("r (m)")
    ax2.set_ylabel("B (μT)")
    ax2.set_title("Perfil radial B(r)")
    ax2.grid()
    ax2.legend()

    # HUD
    text_info.set_text(
        f"I = {I:.2f} A\n"
        f"R = {R:.2f} m\n"
        f"r = {r_destaque:.2f} m\n\n"
        f"{regime}\n"
        f"B = {B_r*1e6:.2f} μT"
    )

    fig.canvas.draw_idle()


# ---------------------------
# SLIDERS
# ---------------------------
ax_I = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_R = plt.axes([0.2, 0.10, 0.65, 0.03])
ax_r = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_I = Slider(ax_I, 'I (A)', -10, 10, valinit=1)
slider_R = Slider(ax_R, 'R (m)', 0.5, 3.0, valinit=1.5)
slider_r = Slider(ax_r, 'r (m)', 0.1, 5.0, valinit=1)

slider_I.on_changed(update)
slider_R.on_changed(update)
slider_r.on_changed(update)

# inicial
update(None)

plt.show()
