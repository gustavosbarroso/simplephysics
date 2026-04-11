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
