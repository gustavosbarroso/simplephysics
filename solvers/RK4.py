import numpy as np

def RK4(f, t0, tf, N, r0, *args):
    h = (tf - t0) / N
    t = np.linspace(t0, tf, N + 1)
    r = np.array(r0, float)

    sol = [r.copy()]

    for i in range(N):
        ti = t[i]

        k1 = h * f(r, ti, *args)
        k2 = h * f(r + 0.5 * k1, ti + 0.5 * h, *args)
        k3 = h * f(r + 0.5 * k2, ti + 0.5 * h, *args)
        k4 = h * f(r + k3, ti + h, *args)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6
        sol.append(r.copy())

    return t, np.array(sol)
