#Parâmetros do sistema resolvido com RK4
params = {
    "param1": 1.0,
    "param2": 2.0,
    "param3": 0.5,
    "param4": 1.5,
}
# ---------------------------
# SLIDERS
# ---------------------------
ax_p1 = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_p2 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_p3 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_p4 = plt.axes([0.25, 0.15, 0.65, 0.03])

slider_p1 = Slider(ax_p1, 'param1', 0.1, 10, valinit=params["param1"])
slider_p2 = Slider(ax_p2, 'param2', 0.1, 10, valinit=params["param2"])
slider_p3 = Slider(ax_p3, 'param3', 0.1, 10, valinit=params["param3"])
slider_p4 = Slider(ax_p4, 'param4', 0.1, 10, valinit=params["param4"])
#Update dos sliders
def update_sliders(val):
    global t, sol1, sol2, sol3, sol4, params

    params["param1"] = slider_p1.val
    params["param2"] = slider_p2.val
    params["param3"] = slider_p3.val
    params["param4"] = slider_p4.val

    t, sol1, sol2, sol3, sol4 = solve(params)

    ani.event_source.stop()
    ani.frame_seq = ani.new_frame_seq()
    ani.event_source.start()

    fig.canvas.draw_idle()
