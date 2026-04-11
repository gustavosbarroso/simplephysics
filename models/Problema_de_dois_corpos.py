import numpy as np

# Constantes (mesmas que você usou)
G = 4 * np.pi**2
UA_POR_ANO = 0.2108


def two_body_equations(r, t, m1, m2):
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = r

    dx = x2 - x1
    dy = y2 - y1

    r_dist = np.sqrt(dx**2 + dy**2) + 1e-8  # evita divisão por zero

    ax1 = G * m2 * dx / r_dist**3
    ay1 = G * m2 * dy / r_dist**3

    ax2 = -G * m1 * dx / r_dist**3
    ay2 = -G * m1 * dy / r_dist**3

    return np.array([vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2], float)


def initial_conditions(r, v_rel, m1, m2):
    """
    Condição inicial no referencial do centro de massa.
    """
    M = m1 + m2

    # posições
    x1 = - (m2 / M) * r
    x2 =   (m1 / M) * r

    # velocidade relativa convertida
    v = v_rel * UA_POR_ANO

    vx1, vx2 = 0, 0
    vy1 =  v * (m2 / M)
    vy2 = -v * (m1 / M)

    # remover velocidade do centro de massa
    vx_cm = (m1*vx1 + m2*vx2) / M
    vy_cm = (m1*vy1 + m2*vy2) / M

    vx1 -= vx_cm
    vy1 -= vy_cm
    vx2 -= vx_cm
    vy2 -= vy_cm

    return np.array([x1, 0, vx1, vy1, x2, 0, vx2, vy2], float)


def classify_orbit(r, v_rel, m1, m2):
    M = m1 + m2
    v = v_rel * UA_POR_ANO

    v_esc = np.sqrt(2 * G * M / r)
    f = v / v_esc

    if abs(f - 1) < 0.02:
        return "Parabólica"
    elif f < 1:
        return "Elíptica"
    else:
        return "Hiperbólica"
