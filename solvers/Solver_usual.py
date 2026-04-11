# =========================================================
# 🔷 2. RK4 GENÉRICO
# =========================================================
def RK4(f, t0, t1, N, r0, p):
    h = (t1 - t0) / N
    t = np.linspace(t0, t1, N + 1)

    r = np.array(r0, float)
    sol = [r.copy()]

    for i in range(N):
        k1 = h * f(r, t[i], p)
        k2 = h * f(r + 0.5*k1, t[i] + 0.5*h, p)
        k3 = h * f(r + 0.5*k2, t[i] + 0.5*h, p)
        k4 = h * f(r + k3, t[i] + h, p)

        r = r + (k1 + 2*k2 + 2*k3 + k4) / 6
        sol.append(r.copy())

    return t, np.array(sol)


# =========================================================
# 🔷 3. POSTPROCESS (TRANSFORMA ESTADO → OBSERVÁVEIS)
# =========================================================
def postprocess(sol, p):
    """
    Aqui você transforma r(t) em coisas plotáveis.
    """
    x = sol[:, 0]
    v = sol[:, 1]

    return {
        "x": x,
        "v": v
    }


# =========================================================
# 🔷 4. SOLVER
# =========================================================
def solve(p):
    t, sol = RK4(f, 0, p["t_max"], p["N"], p["r0"], p)
    obs = postprocess(sol, p)
    return t, sol, obs
