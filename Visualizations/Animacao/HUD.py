import numpy as np
from matplotlib.widgets import Slider
#Criação de HUD
def make_hud(fig, x=0.02, y=0.6):
    return fig.text(
        x, y,
        "",
        fontsize=10,
        bbox=dict(
            boxstyle="round",
            facecolor="white",
            alpha=0.85
        )
    )
#Atualização de HUD
def update_hud(hud, info: dict):
    """
    info = {"θ": 1.2, "ω": 0.3, "E": 10}
    """
    text = "\n".join(
        f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}"
        for k, v in info.items()
    )
    hud.set_text(text)
