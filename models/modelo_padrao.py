# =========================================================
# 🔷 1. SISTEMA FÍSICO (SUBSTITUI AQUI)
# =========================================================
def f(r, t, p):
    """
    Sistema genérico:
    r = estado
    p = parâmetros (dict)
    """
    # EXEMPLO (substituir):
    # dr/dt = v
    # dv/dt = -k*x/m

    x = r[0]
    v = r[1]

    k = p["k"]
    m = p["m"]

    a = -(k/m) * x

    return np.array([v, a], float)
