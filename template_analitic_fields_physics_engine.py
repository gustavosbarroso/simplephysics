import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# =========================
# CONSTANTE (adaptável)
# =========================
k = 8.99e9

# =========================
# CAMPO GENÉRICO
# =========================
def campo(X, Y, params):
    """
    TROQUE AQUI apenas a física do problema
    Deve retornar: Ex, Ey, |E|
    """

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    # EXEMPLO: carga pontual (modelo base)
    q, x0, y0 = params

    dx = X - x0
    dy = Y - y0

    r = np.sqrt(dx**2 + dy**2) + 1e-12

    Ex = k * q * dx / r**3
    Ey = k * q * dy / r**3

    E = np.sqrt(Ex**2 + Ey**2)

    return Ex, Ey, E

# =========================
# FIGURA
# =========================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(bottom=0.25)

# grid fixo
x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)

# HUD
text_info = fig.text(0.75, 0.75, "",
                     bbox=dict(facecolor='white', alpha=0.8))

# =========================
# UPDATE (Padrão universal)
# =========================
def update(val):

    ax1.clear()
    ax2.clear()

    # parâmetros do sistema
    q = slider_q.val
    x0 = slider_x0.val
    y0 = 0

    Ex, Ey, E = campo(X, Y, (q, x0, y0))

    # normalização para linhas de campo
    mag = np.sqrt(Ex**2 + Ey**2) + 1e-12
    Exn = Ex / mag
    Eyn = Ey / mag

    # =========================
    # 1) LINHAS DE CAMPO
    # =========================
    ax1.streamplot(X, Y, Exn, Eyn, density=1.4)

    ax1.plot(x0, 0, 'ro' if q > 0 else 'bo', markersize=10)

    ax1.set_title("Linhas de campo")
    ax1.set_xlim(-3,3)
    ax1.set_ylim(-3,3)
    ax1.set_aspect('equal')

    # =========================
    # 2) PERFIL 1D DO CAMPO
    # =========================
    r_vals = np.linspace(0.1, 3, 200)

    E_line = []

    for r in r_vals:
        Ex1, Ey1, E1 = campo(np.array([[r]]), np.array([[0]]), (q, x0, y0))
        E_line.append(E1[0,0])

    E_line = np.array(E_line)

    ax2.plot(r_vals, E_line, label="|E|(r)")

    # ponto destacado
    Exp, Eyp, Ep = campo(np.array([[x0+0.5]]), np.array([[0]]), (q, x0, y0))
    Ep_val = Ep[0,0]

    ax2.plot(x0+0.5, Ep_val, 'ro')
    ax2.axvline(x0+0.5, linestyle='--', color='gray')

    ax2.set_title("Campo ao longo de r")
    ax2.set_xlabel("r")
    ax2.set_ylabel("|E|")
    ax2.grid()
    ax2.legend()

    # =========================
    # HUD
    # =========================
    text_info.set_text(
        f"q = {q:.2e} C\n"
        f"x0 = {x0:.2f} m\n\n"
        f"E = {Ep_val:.2e} N/C"
    )

    fig.canvas.draw_idle()

# =========================
# SLIDERS
# =========================
ax_q = plt.axes([0.2, 0.12, 0.65, 0.03])
ax_x0 = plt.axes([0.2, 0.06, 0.65, 0.03])

slider_q = Slider(ax_q, 'q (C)', -2, 2, valinit=1)
slider_x0 = Slider(ax_x0, 'posição', -2, 2, valinit=0)

slider_q.on_changed(update)
slider_x0.on_changed(update)

# inicial
update(None)

plt.show()
