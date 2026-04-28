import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ---------------------------
# CONSTANTES
# ---------------------------
mu0 = 4*np.pi*1e-7

# ---------------------------
# SIMPSON (seu)
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
# CAMPO NO EIXO DO SOLENOIDE
# ---------------------------
def B_solenoide(z_obs, I, L, R, n, Nint=100):

    def integrando(zp):
        return R**2 / (R**2 + (z_obs - zp)**2)**(3/2)

    integral = integraSimpson(integrando, -L/2, L/2, Nint)

    return (mu0 * n * I / 2) * integral

# ---------------------------
# FIGURA
# ---------------------------
fig, ax = plt.subplots(figsize=(7,5))
plt.subplots_adjust(bottom=0.35)

# ---------------------------
# UPDATE
# ---------------------------
def update(val):

    ax.clear()

    I = slider_I.val
    L = slider_L.val
    R = slider_R.val
    n = slider_n.val

    z_vals = np.linspace(-3, 3, 100)

    B_vals = [B_solenoide(z, I, L, R, n)*1e6 for z in z_vals]

    ax.plot(z_vals, B_vals, label="Simpson (μT)")

    ax.axvline(-L/2, linestyle='--', color='gray')
    ax.axvline(L/2, linestyle='--', color='gray')

    ax.set_title("Campo ao longo do eixo (solenoide finito)")
    ax.set_xlabel("z (m)")
    ax.set_ylabel("B (μT)")
    ax.grid()
    ax.legend()

    fig.canvas.draw_idle()

# ---------------------------
# SLIDERS
# ---------------------------
ax_I = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_L = plt.axes([0.2, 0.20, 0.65, 0.03])
ax_R = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_n = plt.axes([0.2, 0.10, 0.65, 0.03])

slider_I = Slider(ax_I, 'I (A)', 0.1, 10, valinit=1)
slider_L = Slider(ax_L, 'L (m)', 0.1, 3.0, valinit=1)
slider_R = Slider(ax_R, 'R (m)', 0.1, 1.0, valinit=0.5)
slider_n = Slider(ax_n, 'n (espiras/m)', 10, 500, valinit=100)

slider_I.on_changed(update)
slider_L.on_changed(update)
slider_R.on_changed(update)
slider_n.on_changed(update)

# inicial
update(None)

plt.show()
