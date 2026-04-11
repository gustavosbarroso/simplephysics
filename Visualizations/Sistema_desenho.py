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
