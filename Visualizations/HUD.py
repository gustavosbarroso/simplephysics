import numpy as np
from matplotlib.widgets import Slider
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
