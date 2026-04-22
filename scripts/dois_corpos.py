import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp

# ---------------------------
# CONSTANTES
# ---------------------------
G = 4 * np.pi**2
UA_POR_ANO = 0.2108

# ---------------------------
# EQUAÇÕES
# ---------------------------
def dois_corpos(t, y, params):

    m1 = params["m1"]
    m2 = params["m2"]

    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = y

    dx = x2 - x1
    dy = y2 - y1

    r = np.sqrt(dx**2 + dy**2) + 1e-8

    ax1 = G*m2*dx/r**3
    ay1 = G*m2*dy/r**3

    ax2 = -G*m1*dx/r**3
    ay2 = -G*m1*dy/r**3

    return [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2]

# ---------------------------
# CONDIÇÃO INICIAL
# ---------------------------
def inicial(params):

    r = params["r"]
    v_rel = params["v_rel"]
    m1 = params["m1"]
    m2 = params["m2"]

    M = m1 + m2

    x1 = - (m2/M) * r
    x2 =   (m1/M) * r

    v = v_rel * UA_POR_ANO

    vx1, vx2 = 0, 0
    vy1 =  v * (m2/M)
    vy2 = -v * (m1/M)

    # CM parado
    vx_cm = (m1*vx1 + m2*vx2)/M
    vy_cm = (m1*vy1 + m2*vy2)/M

    vx1 -= vx_cm
    vy1 -= vy_cm
    vx2 -= vx_cm
    vy2 -= vy_cm

    return [x1, 0, vx1, vy1, x2, 0, vx2, vy2]

# ---------------------------
# SOLVER
# ---------------------------
def solve(params):

    y0 = inicial(params)

    t_max = params["t_max"]
    t_eval = np.linspace(0, t_max, 800)

    sol = solve_ivp(
        lambda t, y: dois_corpos(t, y, params),
        (0, t_max),
        y0,
        t_eval=t_eval
    )

    # INFO
    r = params["r"]
    v_rel = params["v_rel"]
    m1 = params["m1"]
    m2 = params["m2"]

    M = m1 + m2
    v = v_rel * UA_POR_ANO
    v_esc = np.sqrt(2 * G * M / r)

    f = v / v_esc

    if abs(f - 1) < 0.02:
        tipo = "Parabólica"
    elif f < 1:
        tipo = "Elíptica"
    else:
        tipo = "Hiperbólica"

    info = (
        f"Parâmetros iniciais\n"
        f"----------------------\n"
        f"r = {r:.2f} UA\n"
        f"v_rel = {v_rel:.1f} km/s\n"
        f"v_esc = {(v_esc/UA_POR_ANO):.1f} km/s\n"
        f"f = {f:.2f}\n\n"
        f"m1 = {m1:.2f} M☉\n"
        f"m2 = {m2:.2f} M☉\n\n"
        f"Órbita: {tipo}"
    )

    return t_eval, sol.y, info

# ---------------------------
# FIGURA
# ---------------------------
fig, (ax_sys, ax_traj, ax_info) = plt.subplots(1,3, figsize=(14,5))
plt.subplots_adjust(bottom=0.35)

ax_sys.set_title("Sistema (CM)")
ax_sys.set_xlabel("x (UA)")
ax_sys.set_ylabel("y (UA)")
ax_sys.set_aspect('equal')
ax_sys.grid(alpha=0.3)

p1, = ax_sys.plot([], [], 'ro', label="m1")
p2, = ax_sys.plot([], [], 'bo', label="m2")
cm_plot, = ax_sys.plot([0], [0], 'k+', markersize=10, label="CM")
ax_sys.legend()

# 🔹 HUD DE TEMPO (AQUI)
text_time = ax_sys.text(
    0.02, 0.95, "",
    transform=ax_sys.transAxes,
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.7)
)

# Trajetória
ax_traj.set_title("Órbitas")
ax_traj.set_xlabel("x (UA)")
ax_traj.set_ylabel("y (UA)")
ax_traj.set_aspect('equal')
ax_traj.grid(alpha=0.3)

traj1, = ax_traj.plot([], [], 'r-')
traj2, = ax_traj.plot([], [], 'b-')

# Info
ax_info.axis('off')
info_text = ax_info.text(
    0.5, 0.5, "",
    ha='center', va='center',
    fontsize=11,
    bbox=dict(boxstyle="round", alpha=0.2)
)

# ---------------------------
# SLIDERS
# ---------------------------
ax_r  = plt.axes([0.2, 0.25, 0.65, 0.03])
ax_v  = plt.axes([0.2, 0.20, 0.65, 0.03])
ax_m1 = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_m2 = plt.axes([0.2, 0.10, 0.65, 0.03])
ax_t  = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_r  = Slider(ax_r,  "r (UA)", 0.5, 5, valinit=2)
slider_v  = Slider(ax_v,  "v_rel (km/s)", 0, 50, valinit=20)
slider_m1 = Slider(ax_m1, "m1 (M☉)", 0.1, 5, valinit=1)
slider_m2 = Slider(ax_m2, "m2 (M☉)", 0.1, 5, valinit=1)
slider_t  = Slider(ax_t,  "tempo (anos)", 1, 20, valinit=5)

def get_params():
    return {
        "r": slider_r.val,
        "v_rel": slider_v.val,
        "m1": slider_m1.val,
        "m2": slider_m2.val,
        "t_max": slider_t.val
    }

t, sol, info = solve(get_params())
info_text.set_text(info)

# ---------------------------
# ANIMAÇÃO
# ---------------------------
def update(frame):

    frame = frame % len(t)

    x1 = sol[0]
    y1 = sol[1]
    x2 = sol[4]
    y2 = sol[5]

    p1.set_data([x1[frame]], [y1[frame]])
    p2.set_data([x2[frame]], [y2[frame]])

    traj1.set_data(x1[:frame], y1[:frame])
    traj2.set_data(x2[:frame], y2[:frame])

    # 🔹 Atualiza tempo
    text_time.set_text(f"t = {t[frame]:.2f} anos")

    lim = max(3, 2*get_params()["r"])

    ax_sys.set_xlim(-lim, lim)
    ax_sys.set_ylim(-lim, lim)
    ax_traj.set_xlim(-lim, lim)
    ax_traj.set_ylim(-lim, lim)

    return p1, p2, traj1, traj2, cm_plot, text_time

ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=False)

# ---------------------------
# UPDATE SLIDERS
# ---------------------------
def update_sliders(val):
    global t, sol, ani

    params = get_params()
    t, sol, info = solve(params)
    info_text.set_text(info)

    traj1.set_data([], [])
    traj2.set_data([], [])

    ani.event_source.stop()
    ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=False)

    fig.canvas.draw_idle()

slider_r.on_changed(update_sliders)
slider_v.on_changed(update_sliders)
slider_m1.on_changed(update_sliders)
slider_m2.on_changed(update_sliders)
slider_t.on_changed(update_sliders)

plt.show()
