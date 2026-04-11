import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# PARÂMETROS
# ---------------------------
N = 60
m = 1.0
k = 10.0

# ---------------------------
# GAUSSIANA
# ---------------------------
def gauss(i, centro, largura, amplitude):
    return amplitude * np.exp(-((i - centro)**2)/(2*largura**2))

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t, N, k, m):
    x = r[:N]
    v = r[N:]

    a = np.zeros(N)

    for i in range(N):
        if i == 0:
            a[i] = (k/m)*(x[i+1] - x[i])
        elif i == N-1:
            a[i] = (k/m)*(x[i-1] - x[i])
        else:
            a[i] = (k/m)*(x[i+1] + x[i-1] - 2*x[i])

    return np.concatenate([v, a])

# ---------------------------
# RK4
# ---------------------------
def RK4(f, a, b, steps, r0, N, k, m):
    h = (b - a) / steps
    tp = np.linspace(a, b, steps+1)
    r = np.array(r0, float)

    sol = [r.copy()]

    for i in range(steps):
        t = tp[i]

        k1 = h * f(r, t, N, k, m)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, N, k, m)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, N, k, m)
        k4 = h * f(r + k3, t + h, N, k, m)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6
        sol.append(r.copy())

    return tp, np.array(sol)

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_chain, ax_plot) = plt.subplots(1,2, figsize=(12,5))
plt.subplots_adjust(bottom=0.35)

# Cadeia
ax_chain.set_xlim(0, N-1)
ax_chain.set_ylim(-2, 2)
ax_chain.set_title("Interferência em cadeia de massas")
ax_chain.set_xlabel("posição (i)")
ax_chain.set_ylabel("x_i (m)")
line, = ax_chain.plot([], [], 'o-', lw=2)

# gráfico temporal
ax_plot.set_xlim(0, 20)
ax_plot.set_ylim(-2, 2)
ax_plot.set_title("x_i(t) (massa central)")
ax_plot.set_xlabel("t (s)")
ax_plot.set_ylabel("x (m)")
line_plot, = ax_plot.plot([], [], label="massa central")
ax_plot.legend()

# ---------------------------
# SLIDERS
# ---------------------------
ax_c1 = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_c2 = plt.axes([0.2, 0.20, 0.65, 0.03])
ax_l1 = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_l2 = plt.axes([0.2, 0.10, 0.65, 0.03])
ax_A1 = plt.axes([0.2, 0.05, 0.65, 0.03])
ax_A2 = plt.axes([0.2, 0.00, 0.65, 0.03])

slider_c1 = Slider(ax_c1, 'x1 inicial (m)', 0, N-1, valinit=N*0.3)
slider_c2 = Slider(ax_c2, 'x2 inicial (m)', 0, N-1, valinit=N*0.7)
slider_l1 = Slider(ax_l1, 'largura 1 (m)', 1, 10, valinit=3)
slider_l2 = Slider(ax_l2, 'largura 2 (m)', 1, 10, valinit=3)
slider_A1 = Slider(ax_A1, 'A1 (m)', -2, 2, valinit=1)
slider_A2 = Slider(ax_A2, 'A2 (m)', -2, 2, valinit=-1)

# ---------------------------
# CONDIÇÃO INICIAL
# ---------------------------
def inicial():
    x0 = np.zeros(N)
    v0 = np.zeros(N)

    for i in range(N):
        x0[i] += gauss(i, slider_c1.val, slider_l1.val, slider_A1.val)
        x0[i] += gauss(i, slider_c2.val, slider_l2.val, slider_A2.val)

    return np.concatenate([x0, v0])

# ---------------------------
# SOLVER
# ---------------------------
def solve():
    r0 = inicial()
    tp, sol = RK4(f, 0, 20, 800, r0, N, k, m)
    x = sol[:, :N]
    v = sol[:, N:]
    return tp, x, v

# resolve pela primeira vez
tp, x, v = solve()

# ---------------------------
# ANIMAÇÃO
# ---------------------------
def init():
    line.set_data(range(N), x[0])
    line_plot.set_data([], [])
    return line, line_plot

def update(frame):
    line.set_data(range(N), x[frame])
    line_plot.set_data(tp[:frame], x[:frame, N//2])
    return line, line_plot

ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    init_func=init,
    interval=20,
    blit=True
)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global tp, x, v

    tp, x, v = solve()

    line_plot.set_data([], [])  # limpa gráfico

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_c1.on_changed(update_sliders)
slider_c2.on_changed(update_sliders)
slider_l1.on_changed(update_sliders)
slider_l2.on_changed(update_sliders)
slider_A1.on_changed(update_sliders)
slider_A2.on_changed(update_sliders)

plt.show()
