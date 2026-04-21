# ---------------------------
# IMPORTS
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# FUNÇÃO
# ---------------------------
def f(x):
    return x**4 - 2*x + 1
# ---------------------------
# MÉTODO DA BISSECÇÃo
# ---------------------------
def bisseccao(f, a, b, tol=1e-6, max_iter=50):
    if f(a) * f(b) > 0:
        print("Não há raiz no intervalo!")
        return None, []

    xs = []
    for i in range(max_iter):
        c = (a + b) / 2
        xs.append(c)

        if abs(f(c)) < tol or abs(b - a) < tol:
            print(f"Convergiu em {i+1} iterações")
            return c, xs

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
raiz, xs = bisseccao(f, -3, 1)
print("Raiz aproximada:", raiz)
