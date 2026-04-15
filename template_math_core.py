import numpy as np
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# =========================================================
# 🔷 1. SISTEMA FÍSICO (SUBSTITUI AQUI)
# =========================================================
def f(r, t, p):
    """
    Sistema genérico:
    r = estado
    p = parâmetros (dict)
    """
    # EXEMPLO (substituir):
    # dr/dt = v
    # dv/dt = -k*x/m

    x = r[0]
    v = r[1]

    k = p["k"]
    m = p["m"]

    a = -(k/m) * x

    return np.array([v, a], float)


# =========================================================
# 🔷 2. RK4 GENÉRICO
# =========================================================
def RK4(f, t0, t1, N, r0, p):
    h = (t1 - t0) / N
    t = np.linspace(t0, t1, N + 1)

    r = np.array(r0, float)
    sol = [r.copy()]

    for i in range(N):
        k1 = h * f(r, t[i], p)
        k2 = h * f(r + 0.5*k1, t[i] + 0.5*h, p)
        k3 = h * f(r + 0.5*k2, t[i] + 0.5*h, p)
        k4 = h * f(r + k3, t[i] + h, p)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6
        sol.append(r.copy())

    return t, np.array(sol)


# =========================================================
# 🔷 3. POSTPROCESS (TRANSFORMA ESTADO → OBSERVÁVEIS)
# =========================================================
def postprocess(sol, p):
    """
    Aqui você transforma r(t) em coisas plotáveis.
    """
    x = sol[:, 0]
    v = sol[:, 1]

    return {
        "x": x,
        "v": v
    }


# =========================================================
# 🔷 4. SOLVER
# =========================================================
def solve(p):
    t, sol = RK4(f, 0, p["t_max"], p["N"], p["r0"], p)
    obs = postprocess(sol, p)
    return t, sol, obs


# =========================================================
# 🔷 5. HUD
# =========================================================
def make_hud(fig):
    return fig.text(
        0.02, 0.6,
        "",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )


def update_hud(hud, info):
    text = "\n".join([f"{k}: {v:.3f}" for k, v in info.items()])
    hud.set_text(text)


# =========================================================
# 🔷 6. FIGURA + ARTISTAS
# =========================================================
def make_figure():
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(bottom=0.3)

    ax.set_title("Simulação Genérica")
    ax.set_xlabel("t ou x")
    ax.set_ylabel("estado")

    line, = ax.plot([], [], lw=2)

    return fig, ax, line


# =========================================================
# 🔷 7. INIT / UPDATE ANIMAÇÃO
# =========================================================
def init(line):
    line.set_data([], [])
    return (line,)


def make_update(line, t, obs, hud, params):

    def update(frame):
        i = frame

        line.set_data(t[:i], obs["x"][:i])

        info = {
            "x": obs["x"][i],
            "v": obs["v"][i],
        }

        update_hud(hud, info)

        return (line, hud)

    return update


# =========================================================
# 🔷 8. SLIDERS
# =========================================================
def make_slider(ax, label, vmin, vmax, valinit):
    return Slider(ax, label, vmin, vmax, valinit=valinit)


def rebuild(val):
    global t, sol, obs, ani

    t, sol, obs = solve(params)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()


# =========================================================
# 🔷 9. MAIN
# =========================================================
if __name__ == "__main__":

    # ---------------------------
    # PARÂMETROS (ALTERA AQUI)
    # ---------------------------
    params = {
        "k": 10.0,
        "m": 1.0,
        "t_max": 20,
        "N": 1000,
        "r0": [1.0, 0.0]
    }

    # ---------------------------
    # SOLUÇÃO INICIAL
    # ---------------------------
    t, sol, obs = solve(params)

    # ---------------------------
    # FIGURA
    # ---------------------------
    fig, ax, line = make_figure()
    hud = make_hud(fig)

    # ---------------------------
    # ANIMAÇÃO
    # ---------------------------
    update = make_update(line, t, obs, hud, params)

    ani = FuncAnimation(
        fig,
        update,
        frames=len(t),
        init_func=lambda: init(line),
        interval=20,
        blit=False
    )

    # ---------------------------
    # SLIDERS (EXEMPLO)
    # ---------------------------
    ax_k = plt.axes([0.25, 0.2, 0.65, 0.03])
    ax_m = plt.axes([0.25, 0.1, 0.65, 0.03])

    slider_k = make_slider(ax_k, "k", 1, 50, params["k"])
    slider_m = make_slider(ax_m, "m", 0.1, 5, params["m"])

    def update_sliders(val):
        params["k"] = slider_k.val
        params["m"] = slider_m.val

        rebuild(val)

    slider_k.on_changed(update_sliders)
    slider_m.on_changed(update_sliders)

    plt.show()
