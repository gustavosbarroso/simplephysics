import numpy as np

def double_pendulum_equations(r, t, g, L1, L2, m1, m2):

    theta1, omega1, theta2, omega2 = r
    delta = theta2 - theta1

    den1 = (m1 + m2)*L1 - m2*L1*np.cos(delta)**2

    a1 = (
        m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
        + m2*g*np.sin(theta2)*np.cos(delta)
        + m2*L2*omega2**2*np.sin(delta)
        - (m1 + m2)*g*np.sin(theta1)
    ) / den1

    den2 = (L2/L1)*den1

    a2 = (
        -m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
        + (m1 + m2)*g*np.sin(theta1)*np.cos(delta)
        - (m1 + m2)*L1*omega1**2*np.sin(delta)
        - (m1 + m2)*g*np.sin(theta2)
    ) / den2

    return np.array([omega1, a1, omega2, a2], float)
