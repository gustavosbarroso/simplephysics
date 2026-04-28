import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTE
# ---------------------------
k = 8.99e9  # N·m²/C²

# ---------------------------
# CAMPO ELÉTRICO
# ---------------------------
def campo_eletrico(X, Y, q):

    r = np.sqrt(X**2 + Y**2)
    r[r == 0] = 1e-9

    Ex = k * q * X / r**3
    Ey = k * q * Y / r**3
    E  = k * q / r**2

    return Ex, Ey, E

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(bottom=0.25)

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

    q = slider_q.val  # já em Coulomb
    r_destaque = slider_r.val

    # =========================
    # CAMPO 2D
    # =========================
    Ex, Ey, E = campo_eletrico(X, Y, q)

    magnitude = np.sqrt(Ex**2 + Ey**2)
    magnitude[magnitude == 0] = 1

    Ex_dir = Ex / magnitude
    Ey_dir = Ey / magnitude

    ax1.streamplot(X, Y, Ex_dir, Ey_dir, density=1.5)

    # carga
    ax1.plot(0, 0, 'o', color='red' if q > 0 else 'blue', markersize=10)

    # ponto
    ax1.plot(r_destaque, 0, 'bo')
    ax1.text(r_destaque, 0, " r", color='blue')

    ax1.set_title("Linhas de campo elétrico")
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect('equal')

    # =========================
    # GRÁFICO E(r)
    # =========================
    r_vals = np.linspace(0.1, 3, 200)

    E_vals = k * q / (r_vals**2) * 1e-3  # kN/C

    ax2.plot(r_vals, E_vals, label="Analítico")

    # valor REAL (N/C)
    E_r_real = k * q / (r_destaque**2)

    # valor para exibição (kN/C)
    E_r_plot = E_r_real * 1e-3

    ax2.plot(r_destaque, E_r_plot, 'ro')
    ax2.axvline(r_destaque, linestyle='--', color='gray')

    ax2.set_xlabel("r (m)")
    ax2.set_ylabel("E (kN/C)")
    ax2.set_title("Campo elétrico E(r)")
    ax2.grid()
    ax2.legend()

    # =========================
    # HUD (kN/C)
    # =========================
    text_info.set_text(
        f"q = {q:.2e} C\n"
        f"r = {r_destaque:.2f} m\n\n"
        f"E = {E_r_plot:.2f} kN/C"
    )

    fig.canvas.draw_idle()

# ---------------------------
# SLIDERS
# ---------------------------
ax_q = plt.axes([0.2, 0.12, 0.65, 0.03])
ax_r = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_q = Slider(ax_q, 'q (C)', -2.0, 2.0, valinit=1)
slider_r = Slider(ax_r, 'r (m)', 0.1, 3.0, valinit=1)

slider_q.on_changed(update)
slider_r.on_changed(update)

# inicial
update(None)

plt.show()
