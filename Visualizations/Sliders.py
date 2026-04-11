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
