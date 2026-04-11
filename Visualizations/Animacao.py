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
