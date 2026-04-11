# =========================
# ANIMAÇÃO GENÉRICA
# =========================

def init():
    obj.set_data([], [])
    return (obj,)


def update(frame):
    state = sol[frame]

    # EXEMPLO: adaptar para qualquer sistema
    # pêndulo:
    x = L * np.sin(state[0])
    y = -L * np.cos(state[0])

    obj.set_data([0, x], [0, y])

    return (obj,)


ani = FuncAnimation(
    fig,
    update,
    frames=len(t),
    init_func=init,
    interval=20,
    blit=False
)
