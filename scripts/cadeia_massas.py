import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# ---------------------------
# PARAMS
# ---------------------------
params = {
    "N": 30,
    "m": 1.0,
    "k": 10.0
}

# ---------------------------
# SISTEMA
# ---------------------------
def f(r, t, params):
    N = params["N"]
    k = params["k"]
    m = params["m"]

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
def RK4(f, a, b, steps, r0, params):
    h = (b - a) / steps
    tp = np.linspace(a, b, steps+1)
    r = np.array(r0, float)

    sol = [r.copy()]

    for i in range(steps):
        t = tp[i]

        k1 = h * f(r, t, params)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h * f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6
        sol.append(r.copy())

    return tp, np.array(sol)

# ---------------------------
# CONDIÇÃO INICIAL
# ---------------------------
def inicial(params):
    N = params["N"]

    x0 = np.zeros(N)
    v0 = np.zeros(N)

    for i in range(N):
        x0[i] = np.exp(-0.1*(i - N/2)**2)

    return np.concatenate([x0, v0])

# ---------------------------
# SOLVER
# ---------------------------
def solve(params):
    r0 = inicial(params)
    tp, sol = RK4(f, 0, 20, 800, r0, params)

    N = params["N"]
    x = sol[:, :N]
    v = sol[:, N:]

    return tp, x, v

tp, x, v = solve(params)

# ---------------------------
# FIGURA
# ---------------------------
fig, ax = plt.subplots(figsize=(10,5))
plt.subplots_adjust(bottom=0.3)

line, = ax.plot([], [], 'o-', lw=2)

ax.set_title("Cadeia de Massas")
ax.set_xlabel("i")
ax.set_ylabel("x_i (m)")

def ajustar_eixos():
    N = params["N"]
    ax.set_xlim(0, N-1)
    ax.set_ylim(-1.5, 1.5)

ajustar_eixos()

# ---------------------------
# INIT
# ---------------------------
def init():
    N = params["N"]
    line.set_data(range(N), x[0])
    return line,

# ---------------------------
# UPDATE
# ---------------------------
def update(frame):
    N = params["N"]
    line.set_data(range(N), x[frame])
    return line,

ani = FuncAnimation(
    fig,
    update,
    frames=len(tp),
    init_func=init,
    interval=20,
    blit=True
)

# ---------------------------
# SLIDERS
# ---------------------------
ax_k = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_m = plt.axes([0.2, 0.10, 0.65, 0.03])
ax_N = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_k = Slider(ax_k, 'k(N/m)', 1, 20, valinit=params["k"])
slider_m = Slider(ax_m, 'm(kg)', 0.5, 5, valinit=params["m"])
slider_N = Slider(ax_N, 'N', 5, 100, valinit=params["N"], valstep=1)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global tp, x, v

    params["k"] = slider_k.val
    params["m"] = slider_m.val
    params["N"] = int(slider_N.val)

    tp, x, v = solve(params)

    ajustar_eixos()

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()

slider_k.on_changed(update_sliders)
slider_m.on_changed(update_sliders)
slider_N.on_changed(update_sliders)

plt.show()
