# =========================================================
# 🔷 7. ANIMAÇÃO
# =========================================================
def make_update(line, t, obs, hud, params, ax):

    def update(frame):
        i = frame

        line.set_data(t[:i], obs["x"][:i])

        # ---------------------------
        # ESCALA DINÂMICA (PADRÃO ATUAL)
        # ---------------------------
        if i > 5:
            ymin = np.min(obs["x"][:i])
            ymax = np.max(obs["x"][:i])

            if abs(ymax - ymin) < 1e-6:
                ymin -= 1
                ymax += 1

            margin = 0.2 * (ymax - ymin)
            ax.set_ylim(ymin - margin, ymax + margin)

        info = {
            "x": obs["x"][i],
            "v": obs["v"][i],
        }

        update_hud(hud, info)

        return (line, hud)

    return update
