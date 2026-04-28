import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTES
# ---------------------------
mu0 = 4*np.pi*1e-7
km = mu0/(4*np.pi)

# ---------------------------
# SIMPSON
# ---------------------------
def integraSimpson(f, a, b, N):
    if N % 2 != 0:
        N += 1

    h = (b - a)/N
    s = f(a) + f(b)

    for k in range(1, N):
        if k % 2 == 0:
            s += 2*f(a + k*h)
        else:
            s += 4*f(a + k*h)

    return (h*s)/3

# ---------------------------
# CAMPO MAGNÉTICO (módulo)
# ---------------------------
def B_em_r(r_obs, I, L, N):

    def integrando(y):
        rq = np.array([0, y, 0])
        ro = np.array([r_obs, 0, 0])

        dl = np.array([0, 1, 0])  # direção do fio

        r_vec = ro - rq
        r = np.linalg.norm(r_vec)

        cross = np.cross(I*dl, r_vec)

        return cross[2] / r**3  # só componente z

    Bz = km * integraSimpson(integrando, -L/2, L/2, N)

    return abs(Bz)

# ---------------------------
# FIGURA
# ---------------------------
fig, ax = plt.subplots(figsize=(7,5))
plt.subplots_adjust(bottom=0.3)

# ---------------------------
# UPDATE
# ---------------------------
def update(val):

    ax.clear()

    I = slider_I.val
    L = slider_L.val

    r_vals = np.linspace(0.1, 5, 80)

    B_vals = [B_em_r(r, I, L, 100) * 1e6 for r in r_vals]

    ax.plot(r_vals, B_vals, label="Simpson (μT)")

    ax.set_title("Campo magnético de fio finito")
    ax.set_xlabel("r (m)")
    ax.set_ylabel("B (μT)")
    ax.grid()
    ax.legend()

    fig.canvas.draw_idle()

# ---------------------------
# SLIDERS
# ---------------------------
ax_I = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_L = plt.axes([0.2, 0.10, 0.65, 0.03])

slider_I = Slider(ax_I, 'I (A)', -10, 10, valinit=1)
slider_L = Slider(ax_L, 'L (m)', 0.1, 2.0, valinit=0.5)

slider_I.on_changed(update)
slider_L.on_changed(update)

# inicial
update(None)

plt.show()
