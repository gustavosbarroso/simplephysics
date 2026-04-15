# =========================================================
# 🔷 5. FIGURA
# =========================================================
def make_figure():
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(left=0.25, bottom=0.3)

    ax.set_title("Simulação Genérica")
    ax.set_xlabel("t")
    ax.set_ylabel("x")

    line, = ax.plot([], [], lw=2)

    return fig, ax, line
