import numpy as np

def rlc_equations(r, t, R, L, C):
    q, i = r
    dqdt = i
    didt = -(R/L)*i - (1/(L*C))*q
    return np.array([dqdt, didt], float)


def classify_regime(R, L, C):
    delta = (R/L)**2 - 4*(1/(L*C))

    if abs(delta) < 1e-3:
        return "Criticamente amortecido"
    elif delta > 0:
        return "Superamortecido"
    else:
        return "Subamortecido"
