import numpy as np

def pendulum_equations(r, t, g, L, b):
    theta, omega = r
    return np.array([
        omega,
        -(g/L)*np.sin(theta) - b*omega
    ], float)


def classify_regime(g, L, b):
    if abs(b) < 1e-6:
        return "Pêndulo simples"

    delta = b**2 - 4*(g/L)

    if abs(delta) < 1e-3:
        return "Criticamente amortecido"
    elif delta > 0:
        return "Superamortecido"
    else:
        return "Subamortecido"
